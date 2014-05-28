import datetime
import re
from app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["TIME"]


def handle(text, mic, config):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """

    tz = getTimezone(config)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    mic.say("It is %s right now." % response)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
