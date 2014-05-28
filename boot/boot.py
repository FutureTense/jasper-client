#!/usr/bin/env python

import os, json
import urllib2

import vocabcompiler

def say(phrase, OPTIONS = " -vdefault+m3 -p 40 -s 160 --stdout > say.wav"):

    os.system("espeak " + json.dumps(phrase) + OPTIONS)
    os.system("aplay -D hw:1,0 say.wav")


# check if there is network connection
def configure():
    try:

        urllib2.urlopen("http://www.google.com").getcode()

        print "CONNECTED TO INTERNET"
        print "COMPILING DICTIONARY"
        vocabcompiler.compile()

        print "STARTING CLIENT PROGRAM"

        try:
            os.system("/home/pi/jasper/client/start.sh &")
        except:
            os.system("/home/pi/jasper/backup/start.sh &")
        finally:
            return

    except:
        say("Hello.... I could not connect to a network... Please log in with your computer to help me")

if __name__ == "__main__":
    print "==========STARTING JASPER CLIENT=========="
    print "=========================================="
    print "COPYRIGHT 2013 SHUBHRO SAHA, CHARLIE MARSH"
    print "=========================================="
    say("Hello.... I am Jasper... Please wait one moment.")
    configure()
