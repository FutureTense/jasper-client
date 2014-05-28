import feedparser
import app_utils
import re
from semantic.numbers import NumberService

WORDS = ["NEWS", "YES", "NO", "FIRST", "SECOND", "THIRD"]

PRIORITY = 3

URL = 'http://news.ycombinator.com'


class Article:

    def __init__(self, title, URL):
        self.title = title
        self.URL = URL


def getTopArticles(maxResults=None):
    d = feedparser.parse("http://news.google.com/?output=rss")

    count = 0
    articles = []
    for item in d['items']:
        articles.append(Article(item['title'], item['link'].split("&url=")[1]))
        count += 1
        if maxResults and count > maxResults:
            break

    return articles


def handle(text, mic, config):
    """
        Responds to user-input, typically speech text, with a summary of
        the day's top news headlines, sending them to the user over email
        if desired.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """
    mic.say("Pulling up the news")
    articles = getTopArticles(maxResults=3)
    titles = [" ".join(x.title.split(" - ")[:-1]) for x in articles]
    all_titles = "... ".join(str(idx + 1) + ")" +
                             title for idx, title in enumerate(titles))

    def handleResponse(text):

        def extractOrdinals(text):
            output = []
            service = NumberService()
            for w in text.split():
                if w in service.__ordinals__:
                    output.append(service.__ordinals__[w])
            return [service.parse(w) for w in output]

        chosen_articles = extractOrdinals(text)
        send_all = chosen_articles is [] and app_utils.isPositive(text)

        if send_all or chosen_articles:
            mic.say("Sure, just give me a moment")

            if config.get('profile','prefers_email').lower()=="true":
                body = "<ul>"

            def formatArticle(article):
                tiny_url = app_utils.generateTinyURL(article.URL)

                if config.get('profile','prefers_email').lower()=="true":
                    return "<li><a href=\'%s\'>%s</a></li>" % (tiny_url,
                                                               article.title)
                else:
                    return article.title + " -- " + tiny_url

            for idx, article in enumerate(articles):
                if send_all or (idx + 1) in chosen_articles:
                    article_link = formatArticle(article)

                    if config.get('profile','prefers_email').lower()=="true":
                        body += article_link
                    else:
                        if not app_utils.emailUser(config, SUBJECT="", BODY=article_link):
                            mic.say(
                                "I'm having trouble sending you these articles. Please make sure that your phone number and carrier are correct on the dashboard.")
                            return

            # if prefers email, we send once, at the end
            if config.get('profile','prefers_email').lower()=="true":
                body += "</ul>"
                if not app_utils.emailUser(config, SUBJECT="Your Top Headlines", BODY=body):
                    mic.say(
                        "I'm having trouble sending you these articles. Please make sure that your phone number and carrier are correct on the dashboard.")
                    return

            mic.say("All set")

        else:

            mic.say("OK I will not send any articles")

    if config.has_option('profile','phone_number'):
        mic.say("Here are the current top headlines. " + all_titles +
                ". Would you like me to send you these articles? If so, which?")
        handleResponse(mic.activeListen())

    else:
        mic.say(
            "Here are the current top headlines. " + all_titles)


def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(news|headline)\b', text, re.IGNORECASE))
