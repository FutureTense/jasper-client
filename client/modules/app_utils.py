import smtplib
from email.MIMEText import MIMEText
import urllib2
import re
import requests
from pytz import timezone


def sendEmail(SUBJECT, BODY, TO, FROM, SENDER, PASSWORD, SMTP_SERVER):
    """Sends an HTML email."""
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            BODY.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break
    msg = MIMEText(BODY.encode(body_charset), 'html', body_charset)
    msg['From'] = SENDER
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    SMTP_PORT = 587
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.starttls()
    session.login(FROM, PASSWORD)
    session.sendmail(SENDER, TO, msg.as_string())
    session.quit()


def emailUser(config, SUBJECT="", BODY=""):
    """
        Sends an email.

        Arguments:
        config -- contains a ConfigParser object loaded with information from jasper.conf
        SUBJECT -- subject line of the email
        BODY -- body text of the email
    """
    def generateSMSEmail(config):
        """Generates an email from a user's phone number based on their carrier."""
        if not config.has_option('profile','carrier') or not config.has_option('profile','phone_number'):
            return None

        return str(config.get('profile','phone_number')) + "@" + config.get('profile','carrier')

    if config.get('profile','prefers_email').lower()=="true" and config.has_option('profile','gmail_address'):
        # add footer
        if BODY:
            BODY = config.get('profile','first_name') + \
                ",<br><br>Here are your top headlines:" + BODY
            BODY += "<br>Sent from your Jasper"

        recipient = config.get('profile','gmail_address')
        if config.has_option('profile','first_name') and config.has_option('profile','last_name'):
            recipient = config.get('profile','first_name') + " " + \
                config.get('profile','last_name') + " <%s>" % recipient
    else:
        recipient = generateSMSEmail(config)

    if not recipient:
        return False

    try:
        if 'mailgun' in config.sections():
            user = config.get('mailgun','username')
            password = config.get('mailgun','password')
            server = 'smtp.mailgun.org'
        else:
            user = config.get('profile','gmail_address')
            password = config.get('profile','gmail_password')
            server = 'smtp.gmail.com'
        sendEmail(SUBJECT, BODY, recipient, user,
                  "Jasper <jasper>", password, server)

        return True
    except:
        return False


def getTimezone(config):
    """
        Returns the pytz timezone for a given config value.

        Arguments:
        config -- contains a ConfigParser object loaded with information from jasper.conf
    """
    try:
        return timezone(config.get('profile','timezone'))
    except:
        return None


def generateTinyURL(URL):
    """
        Generates a compressed URL.

        Arguments:
        URL -- the original URL to-be compressed
    """
    target = "http://tinyurl.com/api-create.php?url=" + URL
    response = urllib2.urlopen(target)
    return response.read()


def isNegative(phrase):
    """
        Returns True if the input phrase has a negative sentiment.

        Arguments:
        phrase -- the input phrase to-be evaluated
    """
    return bool(re.search(r'\b(no(t)?|don\'t|stop|end)\b', phrase, re.IGNORECASE))


def isPositive(phrase):
    """
        Returns True if the input phrase has a positive sentiment.

        Arguments:
        phrase -- the input phrase to-be evaluated
    """
    return re.search(r'\b(sure|yes|yeah|go)\b', phrase, re.IGNORECASE)
