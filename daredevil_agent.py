from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import sys
# insert chk_modules in path so they can be dynamically loaded.
sys.path.insert(1, 'chk_modules/')

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
      result = chkRequest(str(self.path))
      self.wfile.write('{}'.format(result).encode('utf-8'))


# Whatever is the main request in the GET header, 
#   this looks for a matching value and if found, 
#   runs the request asked for
def chkRequest(path, chkval={}):

  # if first char is / remove it
  if path[0] == '/':
    path = path[1:]

  # What module did they request from
  chk_module = 'chk_' + path

  # import the module
  try:
    module = __import__(chk_module)
  except ImportError:
    chkval['Error'] = 'Module ' + chk_module + ' does not exist'
    retval = {**chkval, **hostinfo()}
    return retval

  if os.name == 'nt':
    func = getattr(module, 'run_nt')
  else:
    func = getattr(module, 'run_posix')

  # Run the pre-fabbed function
  chkval = func()

  # chkval and what is returned from hostinfo() are both dictionaries
  #   In python >= 3.9.0 join dictionaries together with a |
  #   In python >= 3.5.0 join dictionaries together with z = {**x, **y}
  # retval = chkval | hostinfo()
  retval = {**chkval, **hostinfo()}

  return retval


# We want this for every agent.  This data will
#   be returned to the Controller so the database
#   will know what host this data belongs to
def hostinfo():
  hostinfo = {}

  hostname = socket.gethostname()
  ip = socket.gethostbyname(hostname)

  hostinfo['hostname'] = hostname
  hostinfo['ip'] = '192.168.1.196'

  return hostinfo


def agent(server_class=HTTPServer, handler_class=APIServer, port=999):
  # Get the IP address of this host
  # ip = socket.gethostbyname(socket.gethostname())
  ip = '192.168.1.196'
  server_address = (ip, port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd on {}:{}'.format(ip, port))

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
    agent(port=int(argv[1]))
  else:
    agent()
