import unittest
from mock import patch
from urllib2 import URLError, urlopen
from test_mic import Mic
import modules
import brain
import jasperConfig

def activeInternet():
    try:
        urlopen('http://www.google.com', timeout=1)
        return True
    except URLError:
        return False


class TestModules(unittest.TestCase):

    def setUp(self):
        self.config = jasperConfig.load()
        self.send = False

    def runConversation(self, query, inputs, module):
        """Generic method for spoofing conversation.

        Arguments:
        query -- The initial input to the server.
        inputs -- Additional input, if conversation is extended.

        Returns:
        The server's responses, in a list.
        """
        self.assertTrue(module.isValid(query))
        mic = Mic(inputs)
        module.handle(query, mic, self.config)
        return mic.outputs

    def testLife(self):
        query = "What is the meaning of life?"
        inputs = []
        outputs = self.runConversation(query, inputs, modules.Life)
        self.assertEqual(len(outputs), 1)
        self.assertTrue("42" in outputs[0])

    def testJoke(self):
        query = "Tell me a joke."
        inputs = ["Who's there?", "Random response"]
        outputs = self.runConversation(query, inputs, modules.Joke)
        self.assertEqual(len(outputs), 3)
        allJokes = open("JOKES.txt", "r").read()
        self.assertTrue(outputs[2] in allJokes)

    def testTime(self):
        query = "What time is it?"
        inputs = []
        self.runConversation(query, inputs, modules.Time)

    @unittest.skipIf(not activeInternet(), "No internet connection")
    def testGmail(self):
        if not self.config.has_option('profile','gmail_password'):
            return

        query = "Check my email"
        inputs = []
        self.runConversation(query, inputs, modules.Gmail)

    @unittest.skipIf(not activeInternet(), "No internet connection")
    def testHN(self):
        query = "find me some of the top hacker news stories"
        if self.send:
            inputs = ["the first and third"]
        else:
            inputs = ["no"]
        outputs = self.runConversation(query, inputs, modules.HN)
        self.assertTrue("front-page articles" in outputs[1])

    @unittest.skipIf(not activeInternet(), "No internet connection")
    def testNews(self):
        query = "find me some of the top news stories"
        if self.send:
            inputs = ["the first"]
        else:
            inputs = ["no"]
        outputs = self.runConversation(query, inputs, modules.News)
        self.assertTrue("top headlines" in outputs[1])

    @unittest.skipIf(not activeInternet(), "No internet connection")
    def testWeather(self):
        query = "what's the weather like tomorrow"
        inputs = []
        outputs = self.runConversation(query, inputs, modules.Weather)
        self.assertTrue(
            "can't see that far ahead" in outputs[0]
            or "Tomorrow" in outputs[0])


class TestBrain(unittest.TestCase):

    @staticmethod
    def _emptyBrain():
        mic = Mic([])
        config = jasperConfig.load()
        return brain.Brain(mic, config)

    @patch.object(brain, 'logError')
    def testLog(self, logError):
        """Does Brain correctly log errors when raised by modules?"""
        my_brain = TestBrain._emptyBrain()
        unclear = my_brain.modules[-1]
        with patch.object(unclear, 'handle') as mocked_handle:
            mocked_handle.side_effect = KeyError('foo')
            my_brain.query("zzz gibberish zzz")
            logError.assert_called_with()

    def testSortByPriority(self):
        """Does Brain sort modules by priority?"""
        my_brain = TestBrain._emptyBrain()
        priorities = filter(lambda m: hasattr(m, 'PRIORITY'), my_brain.modules)
        target = sorted(priorities, key=lambda m: m.PRIORITY, reverse=True)
        self.assertEqual(target, priorities)

    def testPriority(self):
        """Does Brain correctly send query to higher-priority module?"""
        my_brain = TestBrain._emptyBrain()
        hn_module = 'modules.HN'
        hn = filter(lambda m: m.__name__ == hn_module, my_brain.modules)[0]

        with patch.object(hn, 'handle') as mocked_handle:
            my_brain.query("hacker news")
            self.assertTrue(mocked_handle.called)


if __name__ == '__main__':
    unittest.main()
