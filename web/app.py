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
		res = yield wampapp.session.call('ch.device.switch', nameStr)
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



if __name__ == "__main__":
	import sys
	from twisted.web.server import Site
	from twisted.internet import reactor
	reactor.listenTCP(5000, Site(app.resource()))
	wampapp.run("ws://localhost:8080/ws", "realm1")

