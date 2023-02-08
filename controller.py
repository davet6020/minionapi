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
  db = pymysql.connect(host='localhost',user='api',password='W3akPa$$word',database='controller')
  return db


def insert(writeval):
  data = {}
  q = ''

  db = database_connection()
  curs = db.cursor()

  # Out put the result of the chk_ job to the console
  print(writeval)

  # This should really be a better way but it works
  # It pieces together the results and inserts them into the appropriate table/columns
  for key in writeval:
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

    if key == 'linux':
      linux = writeval[key]

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
      data = (hostid, chk_id, platform, linux, hostname, ip, date_recorded)
      q = ['insert into', table, '(hostid, chk_id, platform, os, hostname, ip, date_recorded) values(%s, %s, %s, %s, %s, %s, %s)']
      
  # Build the final insert sql by converting the list into a single string
  sql = ' '.join(q)

  try:
    curs.execute(sql, data)
  except Exception as e:
    print(e)

  db.commit()
  db.close()


def job(curl, hostid, chk_id, chk_key):
  do_insert = False
  jobid = {}
  data = {}
  jobid['hostid'] = hostid
  jobid['chk_id'] = chk_id
  jobid['chk_key'] = chk_key

  url = curl

  try:
    # The Response [200] object
    data = ast.literal_eval(requests.get(url).text)
    do_insert = True
  except requests.exceptions.RequestException as e:
    print('could not connect to host: {} for check: {}'.format(hostid, chk_key))

  retval = {**data, **jobid}

  if do_insert:
    insert(retval)


## Time time is a character string.
## Options are: S - Seconds, M - Minutes, H - Hours, D - Days, W - Weeks
def schedule_query_builder(time_type):
  return "select i.ip, i.port, ct.chk_key, ct.chk_id, i.id, s.cron \
                  from inventory i \
                  join scheduler s on i.id=s.hostid \
                  join chk_type ct on s.chk_id=ct.chk_id \
                  where substr(s.cron, -1) = '" + time_type + \
                  "' order by i.hostname;"

def main():
  db = database_connection()
  curs = db.cursor()

  schedule_types = {
        'S',
        'M',
        'H',
        'D',
        'W'
  }

  # Loop through the scheduler table looking for jobs we want to run
  # Place those jobs on the schedule library stack
  for s_type in schedule_types:
    s = schedule_query_builder(s_type)
    curs.execute(s)

    for ip, port, chk_key, cid, hid, cron in curs.fetchall():
      cron = int(cron[:-1])  # Remove the M tag.
      # Build connection string eg.
      # http://10.0.0.200:999/osinfo
      # http://10.0.0.200:999/cpuhardware
      # http://10.0.0.200:999/diskhardware
      # http://10.0.0.200:999/diskutilisation
      # http://10.0.0.200:999/memutilisation
      # http://10.0.0.200:999/uptime
      url = 'http://' + ip + ':' + str(port) + '/' + chk_key
      if s_type == 'S':
        schedule.every(cron).seconds.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif s_type == 'M':
        schedule.every(cron).minutes.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif s_type == 'H':
        schedule.every(cron).hours.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      elif s_type == 'D':
        schedule.every(cron).days.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)
      else: # weeks
        schedule.every(cron).weeks.do(job, curl=url, hostid=hid, chk_id=cid, chk_key=chk_key)

  curs.close()

  while True:
    schedule.run_pending()
    time.sleep(1)


main()
