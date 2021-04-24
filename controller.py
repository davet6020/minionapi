__author__      = "Richard D. Twiggs"
__student_id__  = "1131828"
__license__     = "MIT"
__version__     = "1.0"
__email__       = "richard.twiggs@maine.edu"
__status__      = "Final"
__module__      = "Controller"

import inspect
import os
import pathlib
import requests
import schedule
import socket
import sqlite3
import sys
import time
from sqlite3 import connect


def database_connection():
  koda = "select i.hostname, i.ip, s.cron, ct.chk_key \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where i.hostname = 'koda';"

  minutes = "select i.hostname, i.ip, s.cron, ct.chk_key \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'M' \
                  order by i.hostname;"

  hours = "select i.hostname, i.ip, s.cron, ct.chk_key \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'H' \
                  order by i.hostname;"

  days = "select i.hostname, i.ip, s.cron, ct.chk_key \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'D' \
                  order by i.hostname;"

  test = "select i.hostname, i.ip, s.cron, ct.chk_key \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'D' \
                  order by i.hostname;"

  print(inspect.stack()[0][3])
  conn = connect('/share/finalapi/db/controller.db')
  curs = conn.cursor()
  curs.execute(days)

  for hostname, ip, cron, chk_key in curs.fetchall():
    print(hostname, ip, cron, chk_key)

  conn.close()


  def insert():
    print(inspect.stack()[0][3])


  def read():
    print(inspect.stack()[0][3])


def job():
    # url = "http://192.168.1.144:999/diskutilisation"
    url = "http://192.168.1.31:999/diskutilisation"
    # data = requests.get(url).json
    data = requests.get(url)
    print(data.text)
    


'''This is the main function. It gets things started.'''
def main():

  # database_connection()
  schedule.every(3).seconds.do(job)

  while True:
    schedule.run_pending()
    time.sleep(1)




"""
Things that happen in here:
- Connect to db
- Get from db what jobs need to run eg list of IPs, request names and how often to run them.
- Batch all requests into time blocks
- As each request is run, store the values into the appropriate db->table

"""


main()

"""
HOW THIS WORKS:
http://192.168.1.150:999/diskhardware

The Controller will always run.  When it first runs, it queries the scheduler table three times.
1st: Query for Jobs that run in number of minutes.
2nd: Query for Jobs that run in number of hours.
3rd: Query for Jobs that run in number of days.

For each batch (1st, 2nd or 3rd), for each them and build jobs using the schedule module which 
will pass the job to the event() function.

example:
import schedule

def greet(name):
    print('Hello', name)

schedule.every(2).seconds.do(greet, name='Alice')
schedule.every(4).seconds.do(greet, name='Bob')

from schedule import every, repeat

@repeat(every().second, "World")
@repeat(every().day, "Mars")
def hello(planet):
    print("Hello", planet)




"""



"""
sqlite> select i.hostname, i.ip, i.port, s.cron, s.chk_id, ct.chk_key from inventory i join scheduler s on i.id=s.hostid join chk_type ct on s.chk_id=ct.chk_id where i.hostname = 'koda' order by cron;
hostname         ip                  port  cron  chk_id  chk_key
---------------  ------------------  ----  ----  ------  -------------------
koda             192.168.1.151       999   1D    2       chk_cpuhardware
koda             192.168.1.151       999   1H    3       chk_diskhardware
koda             192.168.1.151       999   1M    4       chk_diskutilisation
koda             192.168.1.151       999   1M    5       chk_memutilisation
koda             192.168.1.151       999   2M    1       chk_uptime


sqlite> select i.hostname, i.ip, i.port, s.cron, s.chk_id, ct.chk_key from inventory i join scheduler s on i.id=s.hostid join chk_type ct on s.chk_id=ct.chk_id where substr(cron, -1) = 'M' order by cron;
hostname         ip                  port  cron  chk_id  chk_key
---------------  ------------------  ----  ----  ------  -------------------
koda             192.168.1.151       999   1M    4       chk_diskutilisation
samantha         192.168.1.149       999   1M    4       chk_diskutilisation
rizzo            192.168.1.148       999   1M    4       chk_diskutilisation
sofia            192.168.1.150       999   1M    4       chk_diskutilisation
koda             192.168.1.151       999   1M    5       chk_memutilisation
samantha         192.168.1.149       999   1M    5       chk_memutilisation
rizzo            192.168.1.148       999   1M    5       chk_memutilisation
sofia            192.168.1.150       999   1M    5       chk_memutilisation
koda             192.168.1.151       999   2M    1       chk_uptime
samantha         192.168.1.149       999   2M    1       chk_uptime
rizzo            192.168.1.148       999   2M    1       chk_uptime
sofia            192.168.1.150       999   2M    1       chk_uptime


sqlite> select i.hostname, i.ip, i.port, s.cron, s.chk_id, ct.chk_key from inventory i join scheduler s on i.id=s.hostid join chk_type ct on s.chk_id=ct.chk_id where substr(cron, -1) = 'H' order by cron;
hostname         ip                  port  cron  chk_id  chk_key
---------------  ------------------  ----  ----  ------  ----------------
koda             192.168.1.151       999   1H    3       chk_diskhardware
samantha         192.168.1.149       999   1H    3       chk_diskhardware
rizzo            192.168.1.148       999   1H    3       chk_diskhardware
sofia            192.168.1.150       999   1H    3       chk_diskhardware


sqlite> select i.hostname, i.ip, i.port, s.cron, s.chk_id, ct.chk_key from inventory i join scheduler s on i.id=s.hostid join chk_type ct on s.chk_id=ct.chk_id where substr(cron, -1) = 'D' order by cron;
hostname         ip                  port  cron  chk_id  chk_key
---------------  ------------------  ----  ----  ------  ---------------
koda             192.168.1.151       999   1D    2       chk_cpuhardware
samantha         192.168.1.149       999   1D    2       chk_cpuhardware
rizzo            192.168.1.148       999   1D    2       chk_cpuhardware
sofia            192.168.1.150       999   1D    2       chk_cpuhardware

"""
