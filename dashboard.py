import ast
from datetime import datetime
from genshi.template import TemplateLoader
from http.server import BaseHTTPRequestHandler, HTTPServer
import inspect
import json
import os
import pathlib
import pymysql
import schedule
import socket
import sys
import time


# I like this because by itself it is unable to handle GET/POST requests.
#    Instead you have to use sub classes such as do_GET to handle requests.
class APIServer(BaseHTTPRequestHandler):

  # When called it grabs the client header information and sets the pattern
  #   for the return header content type
  def get_Request(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  # When receives an httpd GET request, process it.
  def do_GET(self):
    self.get_Request()

    # favicon is a request that is paired with every other request.
    #   Ignore favicon but process all other requests process
    if self.path.endswith('favicon.ico'):
      return
    else:
      # chkRequest will return the value of the request if it is valid
      path = self.path
    
    # This is the router:

    # if first char is / remove it
    if path[0] == '/':
      path = path[1:]
    # if last char is / remove it
    if path[-1] == '/':
      path = path[:-1]

    # Split path on '/'
    reqSplit = path.split('/')
    # If they just want the main dashboard
    if len(reqSplit) == 1 and reqSplit[0] == 'dashboard':
      dashboard(self)

      return

    # If they requested an individual hostname dashboard
    elif len(reqSplit) == 2 and reqSplit[0] == 'dashboard':
      hostname = reqSplit[1]
      dash_host_summary_display(self, hostname)

      return

    # Not a valid request, go to 404
    else:
      msg =  '<h1 style="color: #5e9ca0;">&nbsp; &nbsp; &nbsp;:-( 404&nbsp; )-:</h1>'
      msg += '<h1 style="color: #5e9ca0;">Page Not Found</h1>'
      self.wfile.write('{}'.format(msg).encode('utf-8'))

      return

    exit()

    # Call the function named after the request value if it is on the safelist
    # Otherwise they can call any global function and break stuff
    safelist = ['querydb', 'dashboard']
    for s in safelist:
      found = False
      
      if path == s:
        found = True
        break

    if found:
      func = globals()[path]()
      self.wfile.write('{}'.format(func).encode('utf-8'))
      return
    else:
      msg =  '<h1 style="color: #5e9ca0;">&nbsp; &nbsp; &nbsp;:-( 404&nbsp; )-:</h1>'
      msg += '<h1 style="color: #5e9ca0;">Page Not Found</h1>'
      self.wfile.write('{}'.format(msg).encode('utf-8'))
      return

def buildHTMLTemplate():
  htmltemplate = {}
  htmltemplate['pageA'] = '<head>'
  htmltemplate['css']   = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">'
  htmltemplate['meta']  = '<meta name="viewport" content="width=device-width, initial-scale=1">'
  htmltemplate['pageZ'] = '</head>'
  htmltemplate['container'] = '<div class="container">'

  return htmltemplate


def dash_host_summary_display(self, hostname):
  # This is called from do_GET if an individual hostname dashboard is requested
  data = dash_host_summary_data(self, hostname)

  loader = TemplateLoader(['templates'])
  tmpl = loader.load('dash_host_summary.html')
  stream = tmpl.generate(title='Summary Dashboard for ' + hostname, hostname=hostname, data=data)
  output = stream.render()
  self.wfile.write('{}'.format(output).encode('utf-8'))

  return


def dash_host_summary_data(self, hostname):
  # maybe call each of the dash values and ensure they are always the latest info
  dup = dash_uptime(self, hostname)
  dch = dash_cpuhardware(self, hostname)
  dcu = dash_cpuutilisation(self, hostname)
  ddh = dash_diskhardware(self, hostname)
  ddu = dash_diskutilisation(self, hostname)
  dmu = dash_memutilisation(self, hostname)

  data = {**dup, **dch, **dcu, **ddh, **ddu, **dmu}

  return data


def dash_cpuhardware(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select date_recorded, cpu_sockets, cpu_cores, model_name, cpu_mhz from data_cpuhardware \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for date_recorded, cpu_sockets, cpu_cores, model_name, cpu_mhz in curs.fetchall():
    data['date_recorded'] = date_recorded
    data['cpu_sockets'] = cpu_sockets
    data['cpu_cores'] = cpu_cores
    data['model_name'] = model_name
    data['cpu_mhz'] = cpu_mhz

  return data


def dash_cpuutilisation(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select cpu_pct from data_cpuutilisation \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for cpu_pct in curs.fetchall():
    data['cpu_pct'] = cpu_pct

  return data


def dash_diskhardware(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select mount_point from data_diskhardware \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for mount_point in curs.fetchall():
    data['mount_point'] = mount_point

  return data


def dash_diskutilisation(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select total_size, free_size, size_type from data_diskutilisation \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for total_size, free_size, size_type in curs.fetchall():
    data['total_size'] = str(total_size) + ' ' + size_type
    data['free_size'] = str(free_size) + ' ' + size_type

  return data


def dash_memutilisation(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select memory_total, memory_free, size_type from data_memutilisation \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for memory_total, memory_free, size_type in curs.fetchall():
    data['memory_total'] = str(memory_total) + ' ' + size_type
    data['memory_free'] = str(memory_free) + ' ' + size_type

  return data


def dash_osinfo(self, hostname):
  data = {}
  return data


def dash_uptime(self, hostname):
  data = {}
  # We have the hostname, return all the data so the template can get it
  db = database_connection()
  curs = db.cursor()

  # Get CPU hardware information
  sql = "select uptime from data_uptime \
   where hostname = '" + hostname + "' order by id desc limit 1"

  try:
    curs.execute(sql)
  except Exception as e:
    # print(traceback.format_exception(*sys.exc_info()))
    print(e)

  for uptime in curs.fetchall():
    data['uptime'] = uptime

  return data


def dashboard(self):
  output = ''
  htmltemplate = buildHTMLTemplate()

  # Build in all the css and basic html headers
  for key in htmltemplate:
    output += htmltemplate[key]

  # Here we need to generate the main dashboard info
  output += '<h1>This is the main dashboard</h1>'
  output += '<h1>This is the main dashboard</h1>'
  output += '<h1>This is the main dashboard</h1>'
  
  self.wfile.write('{}'.format(output).encode('utf-8'))


def database_connection():
  # mysql5.7
  db = pymysql.connect(host='localhost',user='api',password='W3akPa$$word',database='controller')

  return db


def querydb():
  return 'Query the db for data'



# We want this for every agent.  This data will
#   be returned to the Controller so the database
#   will know what host this data belongs to
def hostinfo():
  hostinfo = {}

  hostname = socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.connect(('8.8.8.8', 1))  # Resolve outbound Internet address
  ip = sock.getsockname()[0]

  hostinfo['hostname'] = hostname
  hostinfo['ip'] = ip

  return hostinfo


def webServer(server_class=HTTPServer, handler_class=APIServer, port=80):
  # Get the IP address and hostname of this host
  hostname = hostinfo().get('hostname')
  ip = hostinfo().get('ip')
  server_address = (ip, port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd on {}:{}:{}'.format(hostname, ip, port))

  # A wrapper to run the web server until you quit
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  
  # If you do not do this, even though the agent is halted, the port will be allocated
  httpd.server_close()
  print('Shutting down httpd {}:{}'.format(ip, port))


if __name__ == '__main__':
  from sys import argv

  # The default port to run on is 999 but can be changed with an argument
  if len(argv) == 2:
    webServer(port=int(argv[1]))
  else:
    webServer()
    
