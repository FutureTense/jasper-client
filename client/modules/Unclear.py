from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, mic, config):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """

    messages = ["I'm sorry, could you repeat that?",
                "My apologies, could you try saying that again?",
                "Say that again?", "I beg your pardon?"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    return True
