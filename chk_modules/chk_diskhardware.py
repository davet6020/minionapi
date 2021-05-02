import os
import socket
import subprocess
from subprocess import Popen

def run_nt():
  # import wmi

  # c = wmi.WMI()
  # for os in c.Win32_OperatingSystem():
  #   a = os.LastBootUpTime.split('-')[0]
  #   b = os.LocalDateTime.split('-')[0]
  #   c = (float(b) - float(a))
  #   print('LastBootUpTime: {}  -  LocalDateTime: {}  =  uptime_secs: {}'.format(a, b, c))

  #   retval = secs(c)

  retval = " diskhardware for NT not implemented yet"

  return retval


def run_posix():
  diskinfo = {}
  mp = {}

  df = Popen(["df","-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
  output, errors = df.communicate()

  line = output.split('\n')

  cnt = 0
  
  for row in line:
    mp[cnt] = row
    cnt += 1

  diskinfo = {}
  diskinfo['mount_point'] = mp
  
  retval = diskinfo
 
  return retval
