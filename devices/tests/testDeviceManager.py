# users_test/test_users.py
import sys
sys.path.append('../')
from deviceManager import DeviceManager
from twisted.trial import unittest
from unittest.mock import patch, Mock, MagicMock
from autobahn.wamp.exception import ApplicationError


class BasicTests(unittest.TestCase):
	@patch('deviceManager.DeviceManager.call')  # Mock 'requests' module 'get' method.
	def test_is_running(self, mock_call):
		"""isRunning with mock False"""
		mock_call.return_value = False 
		dm = DeviceManager()
		response = dm.isRunning(1) 
		self.assertEqual(response, False)

	def test_requestSession_None(self):
		"""RequestSession with session initialized to None"""
		dm = DeviceManager()
		dm.sessionID=None
		self.assertEqual(dm.requestSession(), dm.sessionID)
		self.assertNotEqual(dm.sessionID, None)

	def test_requestSession_NotNone(self):
		"""RequestSession with session initialized to None"""
		dm = DeviceManager()
		dm.sessionID="random session"
		self.assertEqual(dm.requestSession(), None)
	
	def test_releaseSession_success_and_failure(self):
		"""ReleaseSession with correct and incorrect sessionID"""
		dm = DeviceManager()
		dm.sessionID="random session"
		self.assertEqual(dm.releaseSession("random session"), "success")
		self.assertEqual(dm.releaseSession("other session"), "failure")



class SwitchTests(unittest.TestCase):
	"""Testing the switching procedure"""

		
	def test_notRunning_pump_noValve(self):
		"""Pump not running no valve"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testPump', 'type':'pump', 'group':-1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				return False
			elif(uri == u"ch.db.getdevicegroup"):
				return([])
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))

		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)

		self.failureResultOf(dm.switch('testPump', None), ApplicationError)

	def test_notRunning_pump_valveClosed(self):
		"""Pump not running one valve closed"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testPump', 'type':'pump', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return False
				elif(args[0] == 2):
					return False
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.db.getdevicegroup"):
				return([{'name':'testValve', 'type':'valve', 'group':1, 'id':2}])
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)
		self.failureResultOf(dm.switch('testPump', None), ApplicationError)

	def test_notRunning_pump_valveOpen(self):
		"""Pump not running one valve open"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testPump', 'type':'pump', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return False
				elif(args[0] == 2):
					return True
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.db.getdevicegroup"):
				return([{'name':'testValve', 'type':'valve', 'group':1, 'id':2}])
			elif(uri == u"ch.gpio.switch"):
				return "success"
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)
		dm.publish = MagicMock()
		self.assertEqual(self.successResultOf(dm.switch('testPump', None)), "success")
		
	def test_running_pump(self):
		"""Pump running"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testPump', 'type':'pump', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return True
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.gpio.switch"):
				return "success"
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)
		dm.publish = MagicMock()
		self.assertEqual(self.successResultOf(dm.switch('testPump', None)), "success")

	def test_wrongID(self):
		"""Different sessionID"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testPump', 'type':'pump', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return True
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.gpio.switch"):
				return "success"
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = "sessionid"
		dm.call=MagicMock(side_effect=mock_def)
		self.failureResultOf(dm.switch('testPump', "session2"), ApplicationError)
		
	def test_isRunning_valve_noPump(self):
		"""Valve is running but no pump in the group"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testValve', 'type':'valve', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return True
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.gpio.switch"):
				return "success"
			elif(uri == u"ch.db.getdevicegroup"):
				return []
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)
		dm.publish = MagicMock()
		self.assertEqual(self.successResultOf(dm.switch('testValve', None)), "success")

	def test_isRunning_valve_pumpRunning(self):
		"""Valve is running and pump is running"""
		def mock_def(uri, *args):
			if(uri == u"ch.db.getdevicedata"):
				return {'name':'testValve', 'type':'valve', 'group':1, 'id':1}
			elif(uri == u"ch.gpio.isrunning"):
				if(args[0] == 1):
					return True
				elif(args[0] == 2):
					return True
				else:
					raise ValueError("Given device id does not exist ({})".format(args[0]))
			elif(uri == u"ch.gpio.switch"):
				return "success"
			elif(uri == u"ch.db.getdevicegroup"):
				return [{'name':'testPump', 'type':'pump', 'group':1, 'id':2}]
			else:
				raise ValueError("Given URI does not exist ({})".format(uri))
		dm = DeviceManager()
		dm.sessionID = None
		dm.call=MagicMock(side_effect=mock_def)
		dm.publish = MagicMock()
		self.failureResultOf(dm.switch('testValve', None), ApplicationError)

