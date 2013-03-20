#!/usr/bin/python

import argparse
import codecs
import logging
import socket
import os
from subprocess import call
from os.path import expanduser

#==Command Line Args==
parser = argparse.ArgumentParser(description='Polls a minecraft server and returns some stats. Also sends boxcar notifications. v1.2')
parser.add_argument('localname', type=str, nargs=1, help='name of computer this script is running on')
parser.add_argument('hostname', type=str, nargs=1, help='hostname of server')
args = parser.parse_args()
hostname = args.hostname
hostname = hostname[0]
localname = args.localname
localname = localname[0]
#===Python library from https://github.com/compbrain/SimpleMinecraftStatus===
def GetMCStatus(hostname, port=25565, timeout=8):
  logging.debug('Trying to establish connection to %s:%d with timeout %f',
                hostname, port, timeout)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(hostname)
    s.settimeout(timeout)
    s.connect((ip, port))
    s.send(chr(254))
    data, _ = s.recvfrom(2048)
    if data[0] == chr(255):
      data, _ = codecs.utf_16_be_decode(data[1:])
      data = data[1:]
      p = data.split(u'\xa7')
      return [True] + p
  except socket.error:
    pass
  return [False]

#===End python library===
home = expanduser("~")
rootpath="/.pymc/"
statuspath="%s%s%s" % (home, rootpath, hostname)
dir="%s%s" % (home, rootpath)
if not os.path.exists(dir):
    os.makedirs(dir)
call(["/usr/bin/touch", statuspath])
f = open(statuspath, 'r') #Open status file for reading
data = f.read()


#===Original script from here https://github.com/oneshoturdone/SimpleMinecraftStatus/blob/master/minecraft_status_demo.py===
status = GetMCStatus(hostname)
if len(status) == 4: #Fix for servers with a colored MOTD
  pass
elif len(status) > 0:
  if status[0]:
    status.remove(status[1])
    status[1] = status[1][1:]

if status[0]: #If server is ON
  print hostname,'is online'
  print 'MOTD is: %s' % status[1]
  print 'Currently %s/%s players online' % (status[2], status[3])
  if data in ['1']:#If server is ON and status file shows that the boxcar notifcation HAS been sent
    f.close()
  else: #If the server is ON and the status file show that the boxcar notifcation HAS NOT been sent
    onmessage = "%s is online with %s players" % (hostname, status[2])
    call(["/usr/local/bin/boxcar", localname, onmessage])
    f.close()
    f = open(statuspath, "w")
    f.write("1")
else:#If the server is OFF
  onmessage = "%s is offline" % (hostname)
  print hostname,'is offline'
  if data in ['0']:#If the server is OFF and the boxcar notification HAS been sent
    f.close
  else: #if the server is OFF and the boxcar notifcation HAS NOT been sent
     call(["/usr/local/bin/boxcar", localname, onmessage])
     f.close()
     f = open(statuspath, "w")
     f.write("0")


