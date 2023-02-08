from bottle import Bottle
import bottle_mysql

app = Bottle()
plugin = bottle_mysql.Plugin(dbuser='api', dbpass='W3akPa$$word', dbname='controller')
app.install(plugin)



app.run(host='192.168.1.50', port=80, debug=True, reloader=True)
