
import time
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
import RPi.GPIO as GPIO

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

	"""
	An application component using the time service.
	"""
	def initGPIO(self, pins):
		print("initializing gpio")
		print(pins)
		GPIO.setmode(GPIO.BOARD)
		for chan in pins:
			GPIO.setup(chan, GPIO.OUT, initial=GPIO.HIGH)

	# Defining remote procedures
	@inlineCallbacks
	def switch(self, name):
		print("switching")
		def switchPin(pin):
			GPIO.output(pin, not GPIO.input(pin))
			if(GPIO.input(pin)):
				print("pump off")
				return "pump off"
			print("pump on")
			return "pump on"
		print(name)
		res = yield self.call(u"ch.db.getpinnumber", name)
		returnValue(switchPin(res))

	@inlineCallbacks
	def getState(self, name):
		print("getting current state")
		def getPinState(pin):
			if(GPIO.input(pin)):
				print("pump off")
				return "off"
			print("pump on")
			return "on"

		res = yield self.call(u"ch.db.getpinnumber", name)
		returnValue(getPinState(res))


	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")

		def error(e):
			print(e)


		d1 = self.call(u"ch.db.getallpinouts")
		d1.addErrback(error)
		d1.addCallback(self.initGPIO)


		yield self.register(self.switch, u"ch.gpio.switch")	
		yield self.register(self.getState, u'ch.gpio.getstate')


	def onDisconnect(self):
		print("disconnected")
		reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	print("here")
	runner.run(Component)
