from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import chk_uptime
import chk_cpuhardware
import chk_diskhardware
import chk_diskutilisation
import chk_memhardware

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
def chkRequest(path, chkval=''):

	# Get system uptime
  if(path.endswith('uptime')):
    if os.name == 'nt':
      print(chk_uptime.uptime_nt())
    else:
      chkval = chk_uptime.uptime_posix()

  # Get cpu hardware information
  if(path.endswith('cpuhardware')):
    if os.name == 'nt':
      print(chk_cpuhardware.cpuhw_nt())
    else:
      chkval = chk_cpuhardware.cpuhw_posix()

  # Get disk hardware information
  if(path.endswith('diskhardware')):
    if os.name == 'nt':
      print(chk_diskhardware.diskhw_nt())
    else:
      chkval = chk_diskhardware.diskhw_posix()

  # Get disk utilisation information
  if(path.endswith('diskutilisation')):
    if os.name == 'nt':
      print(chk_diskutilisation.diskutil_nt())
    else:
      chkval = chk_diskutilisation.diskutil_posix()

  # Get memory hardware information
  if(path.endswith('memhardware')):
    if os.name == 'nt':
      print(chk_memhardware.memhw_nt())
    else:
      chkval = chk_memhardware.memhw_posix()


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
  hostinfo['ip'] = ip

  return hostinfo


def agent(server_class=HTTPServer, handler_class=APIServer, port=999):
  # Get the IP address of this host
  ip = socket.gethostbyname(socket.gethostname())
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