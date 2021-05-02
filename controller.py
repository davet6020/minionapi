__author__      = "Richard D. Twiggs"
__student_id__  = "1131828"
__license__     = "MIT"
__version__     = "1.0"
__email__       = "richard.twiggs@maine.edu"
__status__      = "Final"
__module__      = "Controller"
__mysqluser__   = "api"
__mysqlpass__   = "W3akPa$$word"

import ast
from datetime import datetime
import inspect
import json
import os
import pathlib
import pymysql
import requests
import schedule
import socket
import sys
import time

def database_connection():
  # mysql5.7
  db = pymysql.connect(host='localhost',user='api',password='W3akPa$$word',database='controller')
  # curs = db.cursor()

  return db

def insert(writeval):
  data = {}
  q = ''

  db = database_connection()
  curs = db.cursor()
  
  print('writeval:', writeval)
  for key in writeval:
    # size_type = 'GB'
    now = datetime.now()
    date_recorded = now.strftime('%Y-%m-%d %H:%M:%S')

    if key == 'chk_key':
      table = 'data_' + writeval[key]

    if key == 'hostid':
      hostid = int(writeval[key])

    if key == 'hostname':
      hostname = str(writeval[key])

    if key == 'ip':
      ip = str(writeval[key])

    if key == 'chk_id':
      chk_id = int(writeval[key])

    if key == 'cpu_pct':
      cpu_pct = writeval[key]

    if key == 'cpu sockets':
      cpu_sockets = writeval[key]

    if key == 'cpu cores':
      cpu_cores = writeval[key]

    if key == 'model name':
      model_name = writeval[key]

    if key == 'cpu MHz':
      cpu_mhz = writeval[key]

    if key == 'Total Size':
      total_size = writeval[key]

    if key == 'Memory Total':
      memory_total = writeval[key]

    if key == 'Memory Free':
      memory_free = writeval[key]

    if key == 'Free Size':
      free_size = writeval[key]

    if key == 'size_type':
      size_type = writeval[key]

    if key == 'name':
      name = writeval[key]

    if key == 'uname':
      uname = writeval[key]

    if key == 'platform':
      platform = writeval[key]

    if key == 'architecture':
      architecture = writeval[key]

    if key == 'release':
      release = writeval[key]

    if key == 'version':
      version = writeval[key]

    if key == 'uptime':
      uptime = writeval[key]

    # Depending on the chk type, update the data value and insert sql
    if writeval[key] == 'cpuhardware':
      data = (hostid, chk_id, cpu_sockets, cpu_cores, model_name, cpu_mhz, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, cpu_sockets, cpu_cores, model_name, cpu_mhz, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)']

    if writeval[key] == 'cpuutilisation':
      data = (hostid, chk_id, cpu_pct, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, cpu_pct, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s)']

    if writeval[key] == 'diskutilisation':
      data = (hostid, chk_id, total_size, free_size, size_type, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, total_size, free_size, size_type, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s, %s, %s)']

    if writeval[key] == 'memutilisation':
      data = (hostid, chk_id, memory_total, memory_free, size_type, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, memory_total, memory_free, size_type, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s, %s, %s)']

    if writeval[key] == 'uptime':
      data = (hostid, chk_id, uptime, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, uptime, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s)']

    if writeval[key] == 'osinfo':
      return
      data = (hostid, chk_id, name, uname, platform, architecture, version, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, name, uname, platform, architecture, version, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)']


  # Build the final insert sql
  sql = ' '.join(q)

  try:
    curs.execute(sql, data)
  except Exception as e:
    print(e)


  db.commit()
  db.close()


def read():
    print(inspect.stack()[0][3])
  

def job(curl, hostid, chk_id, chk_key):
  do_insert = False
  jobid = {}
  data = {}
  jobid['hostid'] = hostid
  jobid['chk_id'] = chk_id
  jobid['chk_key'] = chk_key

  url = curl

  try:
    d1 = requests.get(url)
    d2 = d1.text
    data = ast.literal_eval(d2)
    do_insert = True
  except requests.exceptions.RequestException as e:
    print('could not connect to host: {} for check: {}'.format(hostid, chk_key))

  retval = {**data, **jobid}

  if do_insert:
    insert(retval)
    # print(retval)


'''This is the main function. It gets things started.'''
def main():
  db = database_connection()
  curs = db.cursor()

  schedule_types = {
        'seconds',
        'minutes',
        'hours',
        'days',
        'weeks'
  }

  seconds = "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'S' \
                  order by i.hostname;"

  minutes = "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'M' \
                  order by i.hostname;"

  hours = "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'H' \
                  order by i.hostname;"

  days = "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'D' \
                  order by i.hostname;"

  weeks = "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = 'W' \
                  order by i.hostname;"

  for stype in schedule_types:
    if stype == 'seconds':
      curs.execute(seconds)
    elif stype == 'minutes':
      curs.execute(minutes)
    elif stype == 'hours':
      curs.execute(hours)
    elif stype == 'days':
      curs.execute(days)
    else: # weeks
      curs.execute(weeks)

    for ip, port, chk_key, cid, hid, cron in curs.fetchall():
      cron = int(cron[:-1])  # Remove the M tag.
      url = 'http://' + ip + ':' + str(port) + '/' + chk_key

      if stype == 'seconds':
        schedule.every(cron).seconds.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif stype == 'minutes':
        schedule.every(cron).minutes.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif stype == 'hours':
        schedule.every(cron).hours.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif stype == 'days':
        schedule.every(cron).days.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      else: # weeks
        schedule.every(cron).weeks.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)


  curs.close()

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

"""
TODOs
- Write output to the database
- Put in try catch so if it does not connect to an agent, skip/continue
- Write the cpuutilisation chk

"""

main()
