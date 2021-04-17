import os

def secs_1(unixtime):
    seconds = unixtime % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def secs(unixtime):
    seconds = unixtime % (24 * 3600)
    day = seconds // 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    retval = "%d:%d:%02d:%02d" % (day, hour, minutes, seconds)
    
    return retval


def hw_nt():
  # import wmi

  # c = wmi.WMI()
  # for os in c.Win32_OperatingSystem():
  #   a = os.LastBootUpTime.split('-')[0]
  #   b = os.LocalDateTime.split('-')[0]
  #   c = (float(b) - float(a))
  #   print('LastBootUpTime: {}  -  LocalDateTime: {}  =  uptime_secs: {}'.format(a, b, c))

  #   retval = secs(c)

  retval = "check nt hardware"

  return retval


def hw_posix():
  retval = "check posix hardware"
 
  return retval
