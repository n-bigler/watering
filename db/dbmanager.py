from os import environ
import datetime
import pdb

from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ProtocolError
import sqlalchemy as db

class Component(ApplicationSession):
	"""
	A simple time service application component.
	"""
	def getPinNumber(self, name):
		print("getPinNumber")
		print(name)
		s = db.select([self.gpio.c.id]).where(self.gpio.c.name==name)
		res = self.conn.execute(s)
		row = res.fetchone()
		print(row)
		res.close()
		return row[0] 

	def getDeviceData(self, name):
		try:
			print("getDeviceData")
			s = db.select([self.gpio]).where(self.gpio.c.name==name)
			res = self.conn.execute(s)
			obj_list = res.fetchone()
			res.close()
			return dict(zip(self.gpio.c.keys(), obj_list))
		except ProtocolError as e: 
			print("let's not die...")
			return 0

	def getDeviceGroup(self, group):
		print("getDeviceGroup")
		s = db.select([self.gpio]).where(self.gpio.c.group==group)
		res = self.conn.execute(s)
		objs = []
		for row in res:
			objs.append(dict(zip(self.gpio.c.keys(),row)))
		res.close()
		return objs

	def getAllProcesses(self):
		print("getAllProcesses")
		s = db.select([self.process])
		res = self.conn.execute(s)
		proc = self.queryResultsToList(self.process.c.keys(), res)
		res.close()
		return proc

	def getProcessData(self, name):
		print("getProcessData")
		s=db.select([self.process]).where(self.process.c.name == name)
		res = self.conn.execute(s)
		obj_list = res.fetchone()
		res.close()
		return dict(zip(self.process.c.keys(), obj_list))

	def queryResultsToList(self,tableHeaders, queryResults):
		resultList = []
		for row in queryResults:
			print(row)
			resultList.append(dict(zip(tableHeaders, row)))
		return resultList
		
	def getAllTimers(self):
		print("getAllTimers")
		s=db.select([self.timer])
		res = self.conn.execute(s)
		allTimers = self.queryResultsToList(self.timer.c.keys(), res)
		print(allTimers)
		res.close()
		return allTimers
	
	def addTimer(self, theTime, processName):
		#First, we check if the process exists
		allProcesses = self.getAllProcesses(); 
		found = False
		for process in allProcesses:
			if process['name'] == processName:
				found = True
		if found == False: #if the process does not exist
			print("process does not exist, can't add a timer")
			return None
		
		#if it exists, then we add the timer to the database
		try:
			self.conn.execute(self.timer.insert(), time=theTime, 
				process=processName);
		except db.exc.DBAPIError as e:
			print(e)
			print("could not add to db")
			return None
		return self.getAllTimers()


	def deleteTimer(self, theTime):
		print("deleting timer")
		try:
			self.conn.execute(self.timer.delete().where(self.timer.c.time==theTime))
		except db.exc.DBAPIError as e:
			print(e)
			print("could not delete from db")
			return None
		return "success"

	@inlineCallbacks
	def onJoin(self, details):
		self.engine = db.create_engine("sqlite:///hardware.sqlite")
		self.conn = self.engine.connect()
		self.metadata = db.MetaData()
		self.gpio = db.Table('gpio', self.metadata, autoload=True, autoload_with=self.engine)
		self.process = db.Table('process', self.metadata, autoload=True, autoload_with=self.engine)
		self.timer = db.Table('timer', self.metadata, autoload=True, autoload_with=self.engine)
		print("session attached")

		yield self.register(self.getPinNumber, u'ch.db.getpinnumber')
		yield self.register(self.addTimer, u'ch.db.addtimer')
		yield self.register(self.deleteTimer, u'ch.db.deletetimer')

		def getAllPinouts():
			print("retrieving all pins")
			s = db.select([self.gpio.c.id])
			res = self.conn.execute(s)
			pins = []
			for row in res:
				pins.append(row[0])
			res.close()
			return pins 

		yield self.register(getAllPinouts, u'ch.db.getallpinouts')

		def getAllNames():
			print("retrieving all objects")
			s = db.select([self.gpio.c.name])
			res = self.conn.execute(s)
			names = []
			for row in res:
				names.append(row[0])
			return names
		yield self.register(getAllNames, u'ch.db.getallnames')

		yield self.register(self.getDeviceData, u'ch.db.getdevicedata')
		yield self.register(self.getDeviceGroup, u'ch.db.getdevicegroup')
		yield self.register(self.getAllProcesses, u'ch.db.getallprocesses')
		yield self.register(self.getProcessData, u'ch.db.getprocessdata')
		yield self.register(self.getAllTimers, u'ch.db.getalltimers')

	def onDisconnect(self):
		print("disconnecting cleanly?")

if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	runner.run(Component)
