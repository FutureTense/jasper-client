import ConfigParser,os.path,os

def load():
    configFile = ConfigParser.ConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    file = os.path.join(path,"jasper.conf")
    configParser = ConfigParser.ConfigParser()
    configParser.read(file)
    return configParser

