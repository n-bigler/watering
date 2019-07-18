import schedule
import time
import threading

class ScheduleThread(threading.Thread):
	def __init__(self, delay):
		threading.Thread.__init__(self)
		self.cease_running = threading.Event()
		self.delay = delay
	def getStopper(self):
		return self.cease_running
	def run(self):
		while not self.cease_running.is_set():
			print("running")
			schedule.run_pending()
			time.sleep(self.delay)

def job():
	print("I'm working...")

class test:
	def __init__(self):
		self.schThread = ScheduleThread(1)
		self.stopper = schThread.getStopper()
		self.schThread.start()

	

if __name__ == "__main__":
	schedule.every(5).seconds.do(job)
	for it in range(0, 10):
		print("main loop")
		time.sleep(1)
	stopper.set()

