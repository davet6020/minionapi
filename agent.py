from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import chk_uptime
import chk_cpuhardware


class APIServer(BaseHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_response()

    # Ignore favicon but all other requests process
    if self.path.endswith('favicon.ico'):
      return
    else:
    	# chkRequest will return the value of the request if it is valid
      result = chkRequest(str(self.path))
      self.wfile.write('{}'.format(result).encode('utf-8'))


def chkRequest(path, retval=''):
  if(path.endswith('uptime')):
    if os.name == 'nt':
      print(chk_uptime.uptime_nt())
    else:
      retval = chk_uptime.uptime_posix()

  if(path.endswith('cpuhardware')):
    if os.name == 'nt':
      print(chk_cpuhardware.hw_nt())
    else:
      retval = chk_cpuhardware.hw_posix()


  return retval


def run(server_class=HTTPServer, handler_class=APIServer, port=999):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info('Starting httpd...\n')
    
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  
  httpd.server_close()
  logging.info('Stopping httpd...\n')

if __name__ == '__main__':
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()