import random
import re

WORDS = ["MEANING", "OF", "LIFE"]


def handle(text, mic, config):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """
    messages = ["It's 42, you idiot.",
                "It's 42. How many times do I have to tell you?"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmeaning of life\b', text, re.IGNORECASE))
