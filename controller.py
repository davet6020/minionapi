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
import requests
import schedule
import socket
import pymysql
import sys
import time

def database_connection():
  # mysql5.7
  db = pymysql.connect(host='localhost',user='api',password='W3akPa$$word',database='controller')
  # curs = db.cursor()

  return db

def insert(writeval):
  db = database_connection()
  curs = db.cursor()
  
  print(writeval)
  for key in writeval:
    if key == 'hostid':
      hostid = int(writeval[key])

    if key == 'chk_id':
      chk_id = int(writeval[key])

  chk_val = str(writeval)

  now = datetime.now()
  date_recorded = now.strftime('%Y-%m-%d %H:%M:%S')

  data = (hostid, chk_id, chk_val, date_recorded)

  sql = "insert into chk_history (hostid, chk_id, chk_val, date_recorded) values(%s, %s, %s, %s)"

  curs.execute(sql, data)
  db.commit()
  db.close()


def read():
    print(inspect.stack()[0][3])
  

def jobWORKS(curl, hostid, chk_id):
  jobid = {}
  jobid['hostid'] = hostid
  jobid['chk_id'] = chk_id

  url = curl
  d1 = requests.get(url)
  d2 = d1.text
  data = ast.literal_eval(d2)

  retval = {**data, **jobid}

  print(retval)


def job(curl, hostid, chk_id):
  do_insert = False
  jobid = {}
  jobid['hostid'] = hostid
  jobid['chk_id'] = chk_id

  url = curl

  try:
    d1 = requests.get(url)
    d2 = d1.text
    data = ast.literal_eval(d2)
    do_insert = True
  except requests.exceptions.RequestException as e:
    data = {}
    print (e)

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
        schedule.every(cron).seconds.do(job, curl=url, hostid=hid, chk_id=cid)
      elif stype == 'minutes':
        schedule.every(cron).minutes.do(job, curl=url, hostid=hid, chk_id=cid)
      elif stype == 'hours':
        schedule.every(cron).hours.do(job, curl=url, hostid=hid, chk_id=cid)
      elif stype == 'days':
        schedule.every(cron).days.do(job, curl=url, hostid=hid, chk_id=cid)
      else: # weeks
        schedule.every(cron).weeks.do(job, curl=url, hostid=hid, chk_id=cid)


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
