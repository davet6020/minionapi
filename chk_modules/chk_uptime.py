import os

def secs_1(unixtime):
    seconds = unixtime % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def secsGOOD(unixtime):
    seconds = unixtime % (24 * 3600)
    day = seconds // 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    retval = "%d:%d:%02d:%02d" % (day, hour, minutes, seconds)
    
    return retval

def secs(unixtime):
    totsecs = unixtime
    day = totsecs // 86400
    hour = totsecs - (day * 86400)
    srm  = totsecs - (day * 86400)
    hour = srm // 3600
    srm = srm - (hour * 3600)
    minutes = srm // 60
    srm = srm - (minutes * 60)
    seconds = srm

    retval = "%d:%d:%02d:%02d" % (day, hour, minutes, seconds)

    return retval


def run_nt():
  import wmi

  c = wmi.WMI()
  for os in c.Win32_OperatingSystem():
    a = os.LastBootUpTime.split('-')[0]
    b = os.LocalDateTime.split('-')[0]
    c = (float(b) - float(a))
    print('LastBootUpTime: {}  -  LocalDateTime: {}  =  uptime_secs: {}'.format(a, b, c))

    retval = secs(c)

  return retval


def run_posix():
  uptime = {}

  with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])

    uptime['uptime'] = secs(uptime_seconds)
    retval = uptime

  return retval
