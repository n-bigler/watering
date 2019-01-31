
import time
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


class Component(ApplicationSession):

	def isRunning(self, devicePin):
		res = self.call(u'ch.gpio.isrunning', devicePin)
		return res

	# Defining remote procedures
	@inlineCallbacks
	def switch(self, name):
		"""Switches a specific device (on/off) if allowed

		If the device is on, it will turn it off, and vice versa.
		Before blindly switching, the function checks if this is
		allowed or if it could be dangerous. The rules are as follow.
		
		If the device is a pump, then we can switch it on only if there
		is at least one open valve in the same group. A pump can always be
		switched off.

		If the device is a valve, then we can switch it on or off only if
		there is no pump running in the same group.

		Args:
			name: The name of the device.

		Returns:
			(string): "success" if we could switch the device.

		Raises:
			ApplicationError: If we were not allowed to switch the device.
		"""
		device = yield self.call(u"ch.db.getobjdata", name)

		shouldSwitch = False
		running = yield self.isRunning(device["id"])

		if device["type"] == "pump":
			print("it's a pump")
			if running == True: #turning off pump: safe
				print("the pump is already running")
				shouldSwitch=True
			else: #need to check if there is a valve open in the group
				print("pump not yet running")
				groupList = yield self.call(u"ch.db.getobjgroup", device["group"])
				for item in groupList:
					res = yield self.isRunning(item["id"])
					print(res)
					if item["type"] == 'valve' and res == True:
						print("found at least one open valve")
						shouldSwitch = True

		else: #it's a valve
			print("it's a valve")
			shouldSwitch=True
			groupList = yield self.call(u"ch.db.getobjgroup", device["group"])
			for item in groupList:
				res = yield self.isRunning(item["id"])
				if item["type"] == "pump" and res == True:
					print("there is a running pump")
					shouldSwitch = False

		if shouldSwitch:
			print("we should switch")
			self.publish(u"ch.watering.logging", 
				{'msg': 'Switching device {}'.format(device["name"]), 'level':'info'})
			res = yield self.call(u"ch.gpio.switch", device["id"])
			return res

			self.publish(u"ch.watering.logging", 
				{'msg': 'Cannot switch device {}'.format(device["name"]), 'level':'info'})

		raise ApplicationError(u"ch.gpio.error1", "dangerous")


	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")

		def error(e):
			print(e)

		yield self.register(self.switch, u"ch.device.switch")	

	def onDisconnect(self):
		print("disconnected")
		reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	print("here")
	runner.run(Component)
