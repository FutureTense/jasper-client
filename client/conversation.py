from brain import Brain
from mpd import MPDClient

class Conversation(object):

    def __init__(self, persona, mic, config):
        self.persona = persona
        self.mic = mic
        self.config = config
        self.brain = Brain(mic, config)

    def delegateInput(self, text):
        """A wrapper for querying brain."""

        self.brain.query(text)

    def handleForever(self):
        """Delegates user input to the handling function when activated."""
        while True:

            try:
                threshold, transcribed = self.mic.passiveListen(self.persona)
            except:
                continue

            if threshold:
                input = self.mic.activeListen(threshold)
                if input:
                    self.delegateInput(input)
                else:
                    self.mic.say("Pardon?")
