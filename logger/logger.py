from __future__ import print_function
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
import datetime

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


import logging


class Component(ApplicationSession):
	"""
	An application component that subscribes and receives events, and
	stop after having received 5 events.
	"""

	@inlineCallbacks
	def onJoin(self, details):
		print("session attached")
		sub = yield self.subscribe(self.on_event, u'ch.watering.logging')
		print("Subscribed to com.myapp.topic1 with {}".format(sub.id))
		logging.basicConfig(filename='watering.log', filemode='w', level=logging.DEBUG)


	def on_event(self, received):
		print("Got event: {}".format(received))
		timeStr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if received['level'] == 'debug':
			logging.debug(timeStr+" -- " + received['msg'])
		else:
			logging.info(timeStr+ " -- " + received['msg'])	

	def onDisconnect(self):
		print("disconnected")
		if reactor.running:
			reactor.stop()


if __name__ == '__main__':
	url = u"ws://127.0.0.1:8080/ws" 
	realm = u"realm1"
	runner = ApplicationRunner(url, realm)
	runner.run(Component)
