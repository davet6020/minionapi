import os
import socket
import subprocess
from subprocess import Popen

def diskutil_nt():
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


def diskutil_posix():
  diskinfo = {}

  df = Popen(["df","-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
  output, errors = df.communicate()

  line = output.split('\n')

  cnt = 0
  

  for row in line:
    if cnt == 1:
      col = row.split()
      ccnt = 0
      for c in col:
        if ccnt == 5:
          print('c: ', c)
        ccnt += 1
    cnt += 1
    




  retval = diskinfo
 
  return retval
