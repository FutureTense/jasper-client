def main():

      import os,sys,inspect, ConfigParser
      currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
      parentdir = os.path.dirname(currentdir)
      parentdir = os.path.dirname(parentdir)
      sys.path.insert(0,parentdir)
      Config = ConfigParser.ConfigParser()
      cfile = os.path.join(parentdir,"jasper.conf")
      return cfile


if __name__ == "__main__":
    print(main())


