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

  # disk = os.statvfs('/')
  # diskinfo['Total Size'] = str(round(disk.f_bsize * disk.f_blocks / 1000 / 1000 / 1000, 2)) + ' GB'
  # diskinfo['Free Size'] = str(round(disk.f_bsize * disk.f_bfree / 1000 / 1000 / 1000, 2)) + ' GB'

  # retval = diskinfo
 
  # return retval


  s = os.statvfs('/')
  GB = float(1024**3)
  diskinfo['Total Size'] = str(round(float(s.f_blocks) * float(s.f_frsize) / GB, 2)) + ' GB'
  diskinfo['Free Size'] = str(round(float(s.f_bavail) * float(s.f_frsize) / GB, 2)) + ' GB'

  retval = diskinfo
 
  return retval

