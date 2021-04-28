import os
import psutil
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

  retval = "cpuutilisation for NT not implemented yet"

  return retval


def run_posix():
  data = {}

  data['cpu_pct'] = psutil.cpu_percent()
  
  retval = data

  return retval
