import threading
import time
from os import environ
import json
import schedule

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError



class Component(ApplicationSession):
	"""Handles the processes management
	"""
	def testTimer(self):
		print("testing the timer")

	class ScheduleThread(threading.Thread):
		def __init__(self, delay):
			threading.Thread.__init__(self)
			self.cease_running = threading.Event()
			self.delay = delay
		def getStopper(self):
			return self.cease_running
		def run(self):
			while not self.cease_running.is_set():
				print(schedule.jobs)
				schedule.run_pending()
				time.sleep(self.delay)

	def startScheduleThread(self):
		continuous_thread = self.ScheduleThread(20)
		self.cease_running = continuous_thread.getStopper()
		continuous_thread.start()

	def stopScheduleThread(self):
		self.cease_running.set() 


	def setTimer(self, name, t):
		print(time.strftime("%H:%M", t))
		schedule.every().day.at(time.strftime("%H:%M", t)).do(self.launchProcess, name)

	@inlineCallbacks
	def setAllTimers(self):
		allTimers = yield self.call(u"ch.db.getalltimers")
		for timer in allTimers:
			t = time.strptime(timer['time'], "%H:%M:%S")
			print(t)
			self.setTimer(timer['process'], t)

	def removeAllTimers(self):
		for job in schedule.jobs:
			schedule.cancel_job(job)
		print("After deleting jobs: {}".format(schedule.jobs))

	# Defining remote procedures
	@inlineCallbacks
	def launchProcess(self, name):
		if self.sessionID is not None:
			raise ApplicationError(u"ch.process.sessionrunning", "session already running")
		

		processDB = yield self.call(u"ch.db.getprocessdata", name)
		process = None
		with open("processes/"+processDB['filename']) as f:
			filecontent = json.load(f)
		if filecontent == None:
			raise ApplicationError(u"ch.session.fileerror", "could not open process file")

		self.sessionID = yield self.call(u"ch.device.requestsession")
		process = filecontent['process']
		try:
			if self.sessionID is not None:
				print("doing something...")
				for action in process:
					if action['type'] == 'switch':
						yield self.call(u"ch.device.switch", action['name'], self.sessionID)
						time.sleep(0.5)
					elif action['type'] == 'time':
						time.sleep(action['duration'])
				print("done.")
		except ApplicationError as e:
			print("Interrupting process")
			print(e)
		finally:
			print("releasing session")
			res = yield self.call(u"ch.device.releasesession", self.sessionID)
			if res == "success":
				self.sessionID = None
			else:
				raise ApplicationError(u"ch.process.releasesession", "could not release session")

		returnValue("success")

	@inlineCallbacks
	def addTimer(self, theTime, process):
		t = time.strptime(theTime,"%H:%M")
		resDB = yield self.call(u"ch.db.addtimer", time.strftime("%H:%M:%S", t), process)
		if resDB is not None:
			self.removeAllTimers()
			self.setAllTimers()
		return resDB

	@inlineCallbacks
	def deleteTimer(self, theTime):
		t = time.strptime(theTime,"%H:%M:%S")
		resDB = yield self.call(u"ch.db.deletetimer", time.strftime("%H:%M:%S", t))
		if resDB is not None:
			self.removeAllTimers()
			self.setAllTimers()
		return resDB

	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")
		self.sessionID = None;

		def error(e):
			print(e)

		self.startScheduleThread()
		self.setAllTimers()
		yield self.register(self.launchProcess, u"ch.process.launchprocess")	
		yield self.register(self.addTimer, u"ch.process.addtimer")
		yield self.register(self.deleteTimer, u"ch.process.deletetimer")

	def onDisconnect(self):
		print("stopping scheduler")
		self.stopScheduleThread()
		print("disconnected")
		reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	print("here")
	runner.run(Component)
