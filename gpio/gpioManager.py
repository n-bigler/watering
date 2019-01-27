
import time
from os import environ
import pdb

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
import RPi.GPIO as GPIO

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


class Component(ApplicationSession):

	"""
	Manages the gpio on the raspberry pi
	"""
	def initGPIO(self, pins):
		print("initializing gpio")
		print(pins)
		GPIO.setmode(GPIO.BOARD)
		for chan in pins:
			GPIO.setup(chan, GPIO.OUT, initial=GPIO.HIGH)

	def isRunning(self, pin):
		return not GPIO.input(pin) 

	def turnOn(self, pin):
		GPIO.output(pin, GPIO.LOW)

	def turnOff(self, pin):
		GPIO.output(pin, GPIO.HIGH)

	# Defining remote procedures
	@inlineCallbacks
	def switch(self, name):

		obj = yield self.call(u"ch.db.getobjdata", name)

		shouldSwitch = False
		if obj["type"] == "pump":
			if self.isRunning(obj["id"]): #turning off pump: safe
				shouldSwitch=True
			else: #need to check if there is a valve open in the group
				groupList = yield self.call(u"ch.db.getobjgroup", obj["group"])
				for item in groupList:
					if item["type"] == 'valve' and self.isRunning(item["id"]): #we are good
						print("found at least one open valve")
						shouldSwitch = True

		else: #it's a valve
			shouldSwitch=True
			groupList = yield self.call(u"ch.db.getobjgroup", obj["group"])
			for item in groupList:
				if item["type"] == "pump" and self.isRunning(item["id"]):
					shouldSwitch = False

		if shouldSwitch:
			GPIO.output(obj["id"], not GPIO.input(obj["id"]))
			returnValue("success")
		raise ApplicationError(u"ch.gpio.error1", "dangerous")

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
