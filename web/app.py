from twisted.internet.defer import inlineCallbacks, returnValue
from klein import Klein
import json
from twisted.web.static import File
from autobahn.twisted.wamp import Application
from autobahn.wamp.exception import ApplicationError
import pdb

app = Klein()
wampapp = Application()


@app.route("/")
def index(request, branch=True):
	f = File('dist/index.html')
	f.isLeaf = True
	f.type, f.encoding = 'html', None # force MIME type for browser rendering
	return f

@app.route("/main.js")
def main(request, branch=True):
	f = File('dist/main.js')
	return f

@app.route("/switch", methods=['POST'])
@inlineCallbacks
def turnOnPump(request):
	print("tries to turn on pump")
	name = request.args.get(b'name', [b'noname'])[0]
	nameStr = name.decode('utf-8')
	print(nameStr)
	if(nameStr == 'noname'):
		return "error"
	try:
		res = yield wampapp.session.call('ch.device.switch', nameStr, None)
	except ApplicationError as e:
		print("call 2 error: {}".format(e))
		print(e.error_message())
		request.setResponseCode(409)
		returnValue([])

	returnValue(res)

@app.route("/getallnames", methods=['GET'])
@inlineCallbacks
def getAllNames(request):
	print("obtaining all names")
	res = yield wampapp.session.call('ch.db.getallnames')
	returnValue(json.dumps(res))

@app.route("/getstate", methods=['GET'])
@inlineCallbacks
def getState(request):
	print("obtaining the state of a specific object")
	print(request.args)
	name = request.args.get(b'name', [b'noname'])[0]
	nameStr = name.decode('utf-8')

	print("Name is" + nameStr)
	if(nameStr == 'noname'):
		return "error"
	res = yield wampapp.session.call('ch.gpio.getstate', nameStr)
	returnValue(res)

@app.route("/getallprocesses", methods=['GET'])
@inlineCallbacks
def getAllProcesses(request):
	"""Returns all the processes stored in the database
	Clean up the database result by removing the filename column.

	Returns:
		A json dump of all the row of the process database. The column
		containing the filename has been removed.
	"""

	print("obtaining all processes")
	res = yield wampapp.session.call('ch.db.getallprocesses')
	print(res)
	for row in res:
		del row["filename"]
	returnValue(json.dumps(res))

@app.route("/getalltimers", methods=['GET'])
@inlineCallbacks
def getAllTimers(request):
	"""Returns all the timers stored in the database

	Returns:
		A json dump of all the row of the timer table.
	"""

	res = yield wampapp.session.call('ch.db.getalltimers')

	returnValue(json.dumps(res))


@app.route("/launchprocess", methods=['POST'])
@inlineCallbacks
def launchProcess(request):
	print("tries to launch process")
	name = request.args.get(b'name', [b'noname'])[0]
	nameStr = name.decode('utf-8')
	print(nameStr)
	if(nameStr == 'noname'):
		return "error"
	try:
		res = yield wampapp.session.call('ch.process.launchprocess', nameStr)
	except ApplicationError as e:
		print("call 2 error: {}".format(e))
		print(e.error_message())
		request.setResponseCode(409)
		returnValue([])

	returnValue(res)

@app.route("/addtimer", methods=['POST'])
@inlineCallbacks
def addTimer(request):
	print("Adds a new timer")
	time = request.args.get(b'time', [b'notime'])[0]
	timeStr = time.decode('utf-8')
	print(timeStr)
	process = request.args.get(b'process', [b'noprocess'])[0]
	processStr = process.decode('utf-8')
	print(process)
	if(timeStr == 'noprocess' or timeStr == 'notime'):
		return "error"
	try:
		res = yield wampapp.session.call('ch.process.addtimer', timeStr, processStr)
	except ApplicationError as e:
		print("call 2 error: {}".format(e))
		print(e.error_message())
		request.setResponseCode(409)
		returnValue([])

	returnValue(res)

@app.route("/deletetimer", methods=['DELETE'])
@inlineCallbacks
def deleteTimer(request):
	print("Delete a timer")
	time = request.args.get(b'time', [b'notime'])[0]
	timeStr = time.decode('utf-8')
	print(timeStr)
	if(timeStr == 'notime'):
		return "error"
	try:
		res = yield wampapp.session.call('ch.process.deletetimer', timeStr)
	except ApplicationError as e:
		print("call 2 error: {}".format(e))
		print(e.error_message())
		request.setResponseCode(409)
		returnValue([])

	returnValue(res)

if __name__ == "__main__":
	import sys
	from twisted.web.server import Site
	from twisted.internet import reactor
	reactor.listenTCP(5000, Site(app.resource()))
	wampapp.run("ws://localhost:8080/ws", "realm1")

