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

  retval = "cpuutilisation for NT not implemented yet"

  return retval


def run_posix():
  cpuinfo = {}
  cpuinfo['cpuutilisation'] = 'Not implemented yet'
  cpuinfo['chk_id'] = 7
  retval = cpuinfo
  return retval

  with open('/proc/cpuinfo', 'r') as f:
    core_cnt = 1

    for line in f:
      key, val = line.partition(':')[::2]

      if key.strip() == 'cpu MHz':
        cpuinfo[key.strip()] = val.strip()

      if key.strip() == 'cpu cores':
        core_cnt = val.strip()
        cpuinfo[key.strip()] = core_cnt
  
      if key.strip() == 'processor':
        cnt = int(val.strip()) + 1
        cpu_cnt = cnt / int(core_cnt)
        cpuinfo['cpu sockets'] = str(int(cpu_cnt))

      if key.strip() == 'model name':
        cpuinfo[key.strip()] = val.strip()

  retval = cpuinfo
 
  return retval
