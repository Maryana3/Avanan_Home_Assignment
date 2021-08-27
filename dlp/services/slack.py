from django.conf import settings
from slack import WebClient, errors
from dlp.models import Message


class SlackService:

    def __init__(self):
        self.client = WebClient(token=settings.SLACK_USER_OAUTH_TOKEN)

    def update_message(self, channel, timestamp, response):
        try:
            response = self.client.chat_update(
                channel=channel, ts=timestamp, text=response)

        except errors.SlackApiError as e:
            print(e)
