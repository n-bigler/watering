
import time
from os import environ
import pdb

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
import RPi.GPIO as GPIO

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError



class Component(ApplicationSession):
	"""Manages the gpio on the raspberry pi.
	This class handles all the switching and reading from
	the Raspberry pi gpio.

	The word "device" is used for all mechanical devices controlled
	by the raspberry pi (pump, valve...).
	"""
	def initGPIO(self, pins):
		"""Initialize the GPIO system.
		Sets all pins to high (all devices are off)

		Args:
			pins (list): A list of all the gpio pins in use.
		"""
		print("initializing gpio")
		print(pins)
		GPIO.setmode(GPIO.BOARD)
		for chan in pins:
			GPIO.setup(chan, GPIO.OUT, initial=GPIO.HIGH)

	def isRunning(self, pin):
		"""Checks if a device is being powered.

		Args:
			pin: The gpio pin on which the device of interest is connected.

		Returns:
			bool: True if the device is powered. False otherwise
		"""
		print("in gpio.isrunning")
		return not GPIO.input(pin) 

	def turnOn(self, pin):
		"""Start powering a device
		Set the GPIO pin to low to trigger the relay.
		Careful: This depends on the logic of the relay.
		Args:
			pin: The gpio pin on which the device is attached.
		"""
		GPIO.output(pin, GPIO.LOW)

	def turnOff(self, pin):
		"""Sops powering a device
		Set the GPIO pin to high to trigger the relay.
		Careful: This depends on the logic of the relay.
		Args:
			pin: The gpio pin on which the device is attached.
		"""
		GPIO.output(pin, GPIO.HIGH)

	# Defining remote procedures
	def switch(self, pin):
		"""Switches a specific pin (on/off) 

		This function doesn't check for safety. It will switch in
		any case.

		Args:
			name: The name of the device.

		Returns:
			(string): "success" if we could switch the device. "error" otherwise.

		"""
		initial = GPIO.input(pin)
		GPIO.output(pin, not initial)
		if GPIO.input(pin) != initial:
			self.publish(u"ch.watering.logging", {"msg":"switched pin {}".format(pin), "level": "debug"})
			return "success"
		return "error"

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
		yield self.register(self.isRunning, u'ch.gpio.isrunning')


	def onDisconnect(self):
		print("disconnected")
		reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	print("here")
	runner.run(Component)
