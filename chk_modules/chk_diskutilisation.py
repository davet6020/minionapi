import os
import socket

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

  s = os.statvfs('/')
  GB = float(1024**3)
  diskinfo['Total Size'] = str(round(float(s.f_blocks) * float(s.f_frsize) / GB, 2))
  diskinfo['Free Size'] = str(round(float(s.f_bavail) * float(s.f_frsize) / GB, 2))
  diskinfo['size_type'] = 'GB'

  retval = diskinfo
 
  return retval
