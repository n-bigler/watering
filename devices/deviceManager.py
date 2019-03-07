import uuid
import time
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from device import Device

class DeviceManager(ApplicationSession):
	"""Handles the device management

		A device is defined as any hardware connected on the GPIO
		pins of the raspberry pi.
	"""
	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")
		self.sessionID = None;

		def error(e):
			print(e)

		yield self.register(self.switchIfAllowed, u"ch.device.switch")
		yield self.register(self.requestSession, u"ch.device.requestsession")
		yield self.register(self.releaseSession, u"ch.device.releasesession")


	@inlineCallbacks
	def switchIfAllowed(self, name, sessionID):
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
		if(sessionID != self.sessionID):
			raise ApplicationError(u"ch.device.wrongSession", "wrong session")

		device = yield self.getDeviceFromName(name)
		switchAllowed = yield self.isSwitchAllowed(device)
		if switchAllowed == True:
			switched = yield self.switch(device)
			return switched

		self.publish(u"ch.watering.logging", 
			{'msg': 'Cannot switch device {}'.format(device.name), 'level':'info'})
		raise ApplicationError(u"ch.gpio.error1", "dangerous")

	@inlineCallbacks
	def getDeviceFromName(self, name):
		deviceQuery = yield self.call(u"ch.db.getdevicedata", name)
		return Device.fromDict(deviceQuery)

	@inlineCallbacks
	def isSwitchAllowed(self, device):
		running = self.isRunning(device)
		if device.type == "pump":
			if running == True: #turning off pump: safe
				return True
			else: #need to check if there is a valve open in the group
				hasOpenedValve = yield self.groupHasOpenedValve(device.group)
				return hasOpenedValve
		else: #it's a valve
			hasRunningPump = yield self.groupHasRunningPump(device.group)
			if(hasRunningPump == True):
				return False
			return True
		return False

	@inlineCallbacks
	def groupHasOpenedValve(self, group):
		groupList = yield self.call(u"ch.db.getdevicegroup", group)
		for item in groupList:
			currDevice = Device.fromDict(item)
			currDeviceRunning = yield self.isRunning(currDevice)
			if currDevice.type == 'valve' and currDeviceRunning == True:
				return True
		return False
	
	@inlineCallbacks
	def groupHasRunningPump(self, group):
		groupList = yield self.call(u"ch.db.getdevicegroup", group)
		for item in groupList:
			currDevice = Device.fromDict(item)
			currDeviceRunning = yield self.isRunning(currDevice)
			if currDevice.type == 'pump' and currDeviceRunning == True:
				return True
		return False


	@inlineCallbacks
	def switch(self, device):
		running = yield self.isRunning(device)
		self.publish(u"ch.watering.logging", 
			{'type': 'switchingDevice', 'device': device.name, 
			'isOn': ("false" if running else "true"),
			'msg': 'Switching device {}'.format(device.name), 
			'level':'info'})
		res = yield self.call(u"ch.gpio.switch", device.id)
		return res

	def isRunning(self, device):
		"""Query if a specific device is running

		Args:
			device: The device which should be queried.

		Returns:
			A Deffered. 
			Will resolve to True if the device is powered, false otherwise.
		"""
		res = self.call(u'ch.gpio.isrunning', device.id)
		return res

	def requestSession(self):
		if self.sessionID == None:
			self.sessionID = str(uuid.uuid4())
			return self.sessionID
		return None

	def releaseSession(self, sessionID):
		if self.sessionID == sessionID:
			self.sessionID = None
			return "success"
		return "failure"



	def onDisconnect(self):
		print("disconnected")
		reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	print("here")
	runner.run(DeviceManager)
