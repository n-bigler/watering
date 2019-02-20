from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as db


def populateGPIO(gpio):
	engine.execute(gpio.insert(), id=7, name="pump1", 
		description="pump1", type="pump", group=1)
	engine.execute(gpio.insert(), id=11, name="valve1", 
		description="pump1", type="valve", group=1)
	engine.execute(gpio.insert(), id=13, name="valve2", 
		description="pump1", type="valve", group=2)
	engine.execute(gpio.insert(), id=15, name="pump2", 
		description="pump2", type="pump", group=2)

def populateProcess(proc):
	engine.execute(proc.insert(), name="test", 
		description="this is a test process", filename='test.json')



if __name__ == '__main__':
	engine = db.create_engine("sqlite:///hardware.sqlite")
	conn = engine.connect()
	metadata = db.MetaData()
	gpio = db.Table('gpio', metadata, autoload=True, autoload_with=engine)
	populateGPIO(gpio)
	
	proc = db.Table('process', metadata, autoload=True, autoload_with=engine)
	populateProcess(proc)

