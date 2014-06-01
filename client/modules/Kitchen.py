import feedparser
import app_utils
import isy
import re

WORDS = ["TOGGLE","KITCHEN"]

def handle(text, mic, profile):
    """
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    print "--------------------------"

    try:
       result = isy.toggle("kitchen")
       print result
       mic.say(result)
    except Exception, e:
       print e

    print "--------------------------"

def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btoggle kitchen\b', text, re.IGNORECASE))
