import os
import socket

def memhw_nt():
  # import wmi

  # c = wmi.WMI()
  # for os in c.Win32_OperatingSystem():
  #   a = os.LastBootUpTime.split('-')[0]
  #   b = os.LocalDateTime.split('-')[0]
  #   c = (float(b) - float(a))
  #   print('LastBootUpTime: {}  -  LocalDateTime: {}  =  uptime_secs: {}'.format(a, b, c))

  #   retval = secs(c)

  retval = "memhardware for NT not implemented yet"

  return retval

# MemTotal:        2027440 kB
# MemFree:         1404460 kB
# MemAvailable:    1709532 kB



def memhw_posix():
  meminfo = {}

  with open('/proc/meminfo', 'r') as f:
    for line in f:
      key, val = line.partition(':')[::2]
      
      if key.strip() == 'MemTotal':
        v = val.strip().split(' ')[0]
        meminfo['Memory Total'] = str(int((int(v) / 1000))) + ' GB'

      if key.strip() == 'MemFree':
        v = val.strip().split(' ')[0]
        meminfo['Memory Free'] = str(int((int(v) / 1000))) + ' GB'

  retval = meminfo
 
  return retval
