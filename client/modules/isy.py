import requests
import os
import sys
import ConfigParser
import string
import configFile
from requests.auth import HTTPBasicAuth

cfile = configFile.main()
Config = ConfigParser.ConfigParser()
Config.read(cfile)
address = Config.get('isy','server')
username = Config.get('isy','username')
password = Config.get('isy','password')

def command(device, state):

   try:
      item = string.split(Config.get('devices',device),",")

      if state == "on":
         command = "DON"
      elif state == "off":
         command = "DOF"
      elif state.startswith('-'):
         state = 0
      elif state.isdigit():
         stateval = int(state)
         if stateval > 255:
            stateval = 255
         state = str(stateval)
         command = state


      node = item[0]
      if len(item) > 1:
         control=item[1]
      else:
         control=node

      cmd = 'http://' + address + '/rest/nodes/' + node + '/cmd/' + command

      r = requests.get(cmd, auth=(username, password))

      from xml.dom import minidom
      xmldoc = minidom.parseString(r.text)
      result = xmldoc.getElementsByTagName('RestResponse')
      status = result[0].attributes['succeeded'].value

      if status == "true":
         return "success"
      else:
         return "fail"

   except:
      return "fail"

def toggle(device):
      item = string.split(Config.get('devices',device),",")
      node = item[0]
      if len(item) > 1:
         control=item[1]
      else:
         control=node
       
      devstatus = status(device).lower()

      statusval = -1
      if devstatus.isdigit():
        statusval = int(float(devstatus))

      if devstatus != "off" or statusval > 0:
         command = "DOF"
      else:
         command = "DON"
      cmd = 'http://' + address + '/rest/nodes/' + node + '/cmd/' + command
      r = requests.get(cmd, auth=(username, password))
      from xml.dom import minidom
      xmldoc = minidom.parseString(r.text)
      result = xmldoc.getElementsByTagName('RestResponse')
      devstatus = result[0].attributes['succeeded'].value
      if devstatus == "true":
         if command == "DOF":
             return "Off"
         else:
             return "On"
      else:
         return "fail"


def status(device):
   try:
      item = string.split(Config.get('devices',device),",")

      if len(item) > 1:
         node=item[1]
      else:
         node = item[0]

      cmd = 'http://' + address + '/rest/nodes/' + node + '/ST'
      r = requests.get(cmd, auth=(username, password))
      from xml.dom import minidom
      xmldoc = minidom.parseString(r.text)
      status = xmldoc.getElementsByTagName('property')[0].attributes['formatted'].value
      

      return status

   except:
      return "fail"
   

if __name__ == "__command__":
    print(command(sys.argv[1],sys.argv[2]))
elif __name__ == "__status__":
    print(status(sys.argv[1]))
elif __name__ == "__toggle__":
    print(toggle(sys.argv[1]))
