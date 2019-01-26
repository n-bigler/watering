from os import environ
import datetime

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

	@inlineCallbacks
	def onJoin(self, details):
		self.engine = db.create_engine("sqlite:///hardware.sqlite")
		self.conn = self.engine.connect()
		self.metadata = db.MetaData()
		self.gpio = db.Table('gpio', self.metadata, autoload=True, autoload_with=self.engine)
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

if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws"
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	runner.run(Component)
