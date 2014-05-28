import ConfigParser,os.path,os
import sys
from conversation import Conversation
import jasperConfig 

def isLocal():
    return len(sys.argv) > 1 and sys.argv[1] == "--local"

if isLocal():
    from local_mic import Mic
else:
    from mic import Mic

if __name__ == "__main__":

    print "==========================================================="
    print " JASPER The Talking Computer                               "
    print " Copyright 2013 Shubhro Saha & Charlie Marsh               "
    print "==========================================================="

    configParser = jasperConfig.load() 

    mic = Mic("languagemodel.lm", "dictionary.dic",
              "languagemodel_persona.lm", "dictionary_persona.dic")

    mic.say("How can I be of service?")

    conversation = Conversation("JASPER", mic, configParser)

    conversation.handleForever()
