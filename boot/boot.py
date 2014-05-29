#!/usr/bin/env python

import os, json
import urllib2
import sys

import vocabcompiler

def say(phrase, OPTIONS = " -vdefault+m3 -p 40 -s 160 --stdout > say.wav"):
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import playSound
    playSound.play("say.wav")

def configure():
    try:
        urllib2.urlopen("http://www.google.com").getcode()

        print "CONNECTED TO INTERNET"
        print "COMPILING DICTIONARY"
        vocabcompiler.compile("../client/sentences.txt", "../client/dictionary.dic", "../client/languagemodel.lm")

        print "STARTING CLIENT PROGRAM"
        os.system("/home/pi/jasper/client/start.sh &")
        
    except:
        
        print "COULD NOT CONNECT TO NETWORK"
        say("Hello, I could not connect to a network. Please read the documentation to configure your Raspberry Pi.")
        os.system("sudo shutdown -r now")

if __name__ == "__main__":
    print "==========STARTING JASPER CLIENT=========="
    print "=========================================="
    print "COPYRIGHT 2013 SHUBHRO SAHA, CHARLIE MARSH"
    print "=========================================="
    say("Hello.... I am Jasper... Please wait one moment.")
    configure()
