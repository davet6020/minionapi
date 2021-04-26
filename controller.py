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
import datetime
import inspect
import json
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
  conn = connect('/share/finalapi/db/controller.db', timeout=2)

  return conn


def insert(writeval):
  conn = database_connection()
  curs = conn.cursor()
  # insert into chk_history: hostid, chk_id, chk_val, datetime
    
  print(writeval)
  for key in writeval:
    if key == 'host_id':
      host_id = int(writeval[key])

    if key == 'chk_id':
      chk_id = int(writeval[key])


  chk_val = str(writeval)
  date_recorded = datetime.datetime.now()
  data = (host_id, chk_id, chk_val, date_recorded)
  sql = """insert into chk_history (hostid, chk_id, chk_val, date_recorded) values(?,?,?,?)"""

  curs.execute(sql, data)
  conn.commit()
  conn.close()
  exit()

def read():
    print(inspect.stack()[0][3])
  

def jobWORKS(curl, host_id, chk_id):
  jobid = {}
  jobid['host_id'] = host_id
  jobid['chk_id'] = chk_id

  url = curl
  d1 = requests.get(url)
  d2 = d1.text
  data = ast.literal_eval(d2)

  retval = {**data, **jobid}

  print(retval)


def job(curl, host_id, chk_id):
  do_insert = False
  jobid = {}
  jobid['host_id'] = host_id
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

  conn = database_connection()
  curs = conn.cursor()

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
        schedule.every(1).seconds.do(job, curl=url, host_id=hid, chk_id=cid)
      elif stype == 'minutes':
        schedule.every(cron).minutes.do(job, curl=url, host_id=hid, chk_id=cid)
      elif stype == 'hours':
        schedule.every(cron).hours.do(job, curl=url, host_id=hid, chk_id=cid)
      elif stype == 'days':
        schedule.every(cron).days.do(job, curl=url, host_id=hid, chk_id=cid)
      else: # weeks
        schedule.every(cron).weeks.do(job, curl=url, host_id=hid, chk_id=cid)


  conn.close()

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
