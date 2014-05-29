import sys
import os
import ConfigParser
import jasperConfig
import string
import os,sys,inspect

def play(file):
    config = jasperConfig.load()
    speakervolume = config.get('audio','speaker-volume')
    speakermute = config.get('audio','speaker-mute')
    micvolume = config.get('audio','mic-volume')
    micmute = config.get('audio','mic-mute')
    cmd = config.get('audio','target')
    os.system("amixer set PCM " + speakervolume + "% >/dev/null")
    if speakermute=="1":
       os.system("amixer set PCM mute >/dev/null")
    else:
       os.system("amixer set PCM unmute >/dev/null")

    os.system("amixer set Mic " + micvolume + "% >/dev/null")
    if micmute=="1":
       os.system("amixer set Mic nocap >/dev/null")
    else:
       os.system("amixer set Mic cap >/dev/null")
    os.system(cmd + " " + file)

if __name__ == "__main__":
    play(sys.argv[1])

