import os
import platform
import socket
import sys

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
  osinfo = {}

  # Get linux type eg Fedora, CentOS etc
  file = open('/etc/os-release', 'r')
  linux = ''
  for f in file:
    # info = f.readline().split('=')
    data = f.split('=')
    if data[0] == 'NAME':
      linux += data[1].strip()

    if data[0] == 'VERSION':
      vers = data[1]
      linux += ' ' + vers

  osinfo['linux'] = linux
  osinfo['name'] = os.name
  osinfo['uname'] = sys.platform
  osinfo['platform'] = platform.machine()

  architecture = platform.architecture()
  arch = ''
  for a in architecture:
    arch += ' ' + a

  osinfo['architecture'] = arch.strip()
  osinfo['version'] = platform.version()

  retval = osinfo
 
  return retval
