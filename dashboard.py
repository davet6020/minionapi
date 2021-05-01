import ast
from datetime import datetime
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
       
    # if first char is / remove it
    if path[0] == '/':
      path = path[1:]

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

def get_uptime():
  output = ''
  output += '<div class="row">'
  output += '<div>uptime stuff</div></div>'
  return output


def get_cpuhardware():
  output = ''
  db = database_connection()
  curs = db.cursor()

  sql = "select hostname, cpu_sockets, cpu_cores, model_name, cpu_mhz from data_cpuhardware where hostname='captainamerica' limit 1"
  sql = "select distinct hostname, cpu_sockets, cpu_cores, model_name, cpu_mhz from data_cpuhardware"
  curs.execute(sql)

  for hostname, cpu_sockets, cpu_cores, model_name, cpu_mhz in curs.fetchall():
    output += '<h3>Hostname: ' + hostname + '</h3>'
    output += '<div class="row">'
    output += '<div class="col-sm-1">Model:</div>'
    output += '<div class="col-sm-11">' + model_name + '</div>'
    output += '</div>'
    
    output += '<div class="row">'
    output += '<div class="col-sm-1">Sockets:</div>'
    output += '<div class="col-sm-11">' + str(cpu_sockets) + '</div>'
    output += '</div>'

    output += '<div class="row">'
    output += '<div class="col-sm-1">Cores:</div>'
    output += '<div class="col-sm-11">' + str(cpu_cores) + '</div>'
    output += '</div>'

    output += '<div class="row">'
    output += '<div class="col-sm-1">Speed:</div>'
    output += '<div class="col-sm-11">' + str(cpu_mhz) + ' MHz</div>'
    output += '</div></div>'

  return output

def dashboard():
  output = ''
  htmltemplate = buildHTMLTemplate()

  for key in htmltemplate:
    output += htmltemplate[key]

  output += get_cpuhardware()
  output += get_uptime()

  retval = output

  return retval


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
    
