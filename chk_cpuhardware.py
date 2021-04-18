import os
import socket

def cpuhw_nt():
  # import wmi

  # c = wmi.WMI()
  # for os in c.Win32_OperatingSystem():
  #   a = os.LastBootUpTime.split('-')[0]
  #   b = os.LocalDateTime.split('-')[0]
  #   c = (float(b) - float(a))
  #   print('LastBootUpTime: {}  -  LocalDateTime: {}  =  uptime_secs: {}'.format(a, b, c))

  #   retval = secs(c)

  retval = "cpuhardware for NT not implemented yet"

  return retval


def cpuhw_posix():
  cpuinfo = {}

  with open('/proc/cpuinfo', 'r') as f:
    for line in f:
      key, val = line.partition(':')[::2]
      
      if key.strip() == 'model name':
        cpuinfo[key.strip()] = val.strip()

      if key.strip() == 'cpu cores':
        cpuinfo[key.strip()] = val.strip()
  
  retval = cpuinfo
 
  return retval
