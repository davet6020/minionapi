import os
import socket

def diskhw_nt():
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

# [root@koda proc]# df -h
# Filesystem                      Size  Used Avail Use% Mounted on
# devtmpfs                        969M     0  969M   0% /dev
# tmpfs                           990M     0  990M   0% /dev/shm
# tmpfs                           396M  708K  396M   1% /run
# /dev/mapper/fedora_fedora-root  5.0G  3.2G  1.9G  64% /
# tmpfs                           990M     0  990M   0% /tmp
# /dev/sda1                      1014M  199M  816M  20% /boot
# tmpfs                           198M     0  198M   0% /run/user/0
# share                           476G  380G   97G  80% /share




def diskhw_posix():
  diskinfo = {}

  disk = os.statvfs('/')
  diskinfo['Total Size'] = str(round(disk.f_frsize * disk.f_blocks / 1000 / 1000 / 1000, 2)) + ' GB'
  diskinfo['Free Size'] = str(round(disk.f_frsize * disk.f_bfree / 1000 / 1000 / 1000, 2)) + ' GB'

  retval = diskinfo
 
  return retval
