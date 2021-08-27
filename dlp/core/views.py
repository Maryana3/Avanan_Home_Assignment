from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from dlp.services.slack import SlackService
from dlp.services.message_helper import get_message_info, check_message
from dlp.models import Message


class SlackMessageView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get('token', '') != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse(status=403)
        # return the challenge code here
        if request.data.get('type', '') == 'url_verification':
            return JsonResponse({"challenge": request.data.get('challenge')})

        slack_service = SlackService()
        message_event = request.data.get('event')
        message = get_message_info(message_event)
        if message:
            response_text, caught_by = check_message(message['text'])
            if response_text:
                slack_service.update_message(
                    message['channel'], message['ts'], response_text)
                Message(
                    text=message['text'], user_id=message['user'], caught_pattern=caught_by).save()
                return JsonResponse(request.data['event'])
            return HttpResponse(status=200)

        return HttpResponse(status=404)


class FileCheckerView(APIView):
    def post(self, request, *args, **kwargs):
        leaks = []
        for line in request.FILES['test']:
            response_text = check_message(str(line))
            if response_text:
                leaks.append(response_text)

        if len(leaks):
            return HttpResponse(leaks, status=400)

        return HttpResponse(status=200)
