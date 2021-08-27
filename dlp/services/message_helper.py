import re
from django.conf import settings

CARD_REGEX_LIST = [
    "^.*(?:4[0-9]{12}(?:[0-9]{3})?).*$",  # Visa

    # MasterCard
    "^.*(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}.*$",
    "^.*3[47][0-9]{13}.*$",  # American Express
]

RESPONSES = {
    "card": "sending card number was blocked",
    "password": "password sending was blocked"
}


def check_message(message: str):
    if message in RESPONSES.values():
        return None, None

    for regex in CARD_REGEX_LIST:
        if re.search(regex, message):
            return RESPONSES['card'], regex

    for password in settings.BLOCKED_PASSWORDS:
        if password in message:
            return RESPONSES['password'], password

    return None, None


def get_message_info(slack_event):
    if slack_event.get('subtype') == 'message_changed':
        return {
            "text": slack_event['message']['text'],
            "ts": slack_event['message']['ts'],
            "channel": slack_event['channel'],
            "user": slack_event['message']['user']
        }
    elif slack_event.get('type') == 'message':
        return {
            "text": slack_event['text'],
            "ts": slack_event['ts'],
            "channel": slack_event['channel'],
            "user": slack_event['user']
        }

    return None
