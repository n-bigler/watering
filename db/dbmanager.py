from os import environ
import datetime
import pdb

from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
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

	def getObjData(self, name):
		print("getObjData")
		s = db.select([self.gpio]).where(self.gpio.c.name==name)
		res = self.conn.execute(s)
		obj_list = res.fetchone()
		return dict(zip(self.gpio.c.keys(), obj_list))

	def getObjGroup(self, group):
		print("getObjGroup")
		s = db.select([self.gpio]).where(self.gpio.c.group==group)
		res = self.conn.execute(s)
		objs = []
		for row in res:
			objs.append(dict(zip(self.gpio.c.keys(),row)))
		return objs

	def getAllProcesses(self):
		print("getAllProcesses")
		s = db.select([self.process])
		res = self.conn.execute(s)
		proc = []
		for row in res:
			proc.append(dict(zip(self.process.c.keys(),row)))
		return proc

	@inlineCallbacks
	def onJoin(self, details):
		self.engine = db.create_engine("sqlite:///hardware.sqlite")
		self.conn = self.engine.connect()
		self.metadata = db.MetaData()
		self.gpio = db.Table('gpio', self.metadata, autoload=True, autoload_with=self.engine)
		self.process = db.Table('process', self.metadata, autoload=True, autoload_with=self.engine)
		print("session attached")

		yield self.register(self.getPinNumber, u'ch.db.getpinnumber')

		def getAllPinouts():
			print("retrieving all pins")
			s = db.select([self.gpio.c.id])
			res = self.conn.execute(s)
			pins = []
			for row in res:
				pins.append(row[0])
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

		yield self.register(self.getObjData, u'ch.db.getobjdata')
		yield self.register(self.getObjGroup, u'ch.db.getobjgroup')
		yield self.register(self.getAllProcesses, u'ch.db.getallprocesses')


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	runner.run(Component)
