import datetime
import re
from facebook import *
from app_utils import getTimezone

WORDS = ["BIRTHDAY"]


def handle(text, mic, config):
    """
        Responds to user-input, typically speech text, by listing the user's
        Facebook friends with birthdays today.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """
    oauth_access_token = config.get('facebook','token')

    graph = GraphAPI(oauth_access_token)

    try:
        results = graph.request(
            "me/friends", args={'fields': 'id,name,birthday'})
    except GraphAPIError:
        mic.say(
            "I have not been authorized to query your Facebook. If you would like to check birthdays in the future, please visit the Jasper dashboard.")
        return
    except:
        mic.say(
            "I apologize, there's a problem with that service at the moment.")
        return

    needle = datetime.datetime.now(tz=getTimezone(config)).strftime("%m/%d")

    people = []
    for person in results['data']:
        try:
            if needle in person['birthday']:
                people.append(person['name'])
        except:
            continue

    if len(people) > 0:
        if len(people) == 1:
            output = people[0] + " has a birthday today."
        else:
            output = "Your friends with birthdays today are " + \
                ", ".join(people[:-1]) + " and " + people[-1] + "."
    else:
        output = "None of your friends have birthdays today."

    mic.say(output)


def isValid(text):
    """
        Returns True if the input is related to birthdays.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'birthday', text, re.IGNORECASE))
