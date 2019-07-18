from sqlalchemy.ext.declarative import declarative_base
import sqlite3

import sqlalchemy as db

def createTables(metadata, engine):
	gpio = db.Table('gpio', metadata,
		db.Column('id', db.Integer, primary_key=True),
		db.Column('name', db.Text, nullable=False),
		db.Column('description', db.Text),
		db.Column('type', db.Text, nullable=False, server_default="valve"),
		db.Column('group', db.Integer, nullable=False, server_default="1")
		)
	proc = db.Table('process', metadata,
		db.Column('name', db.String(200), primary_key=True),
		db.Column('description', db.String(200), nullable=False, server_default="no description"),
		db.Column('filename', db.String(200), nullable=False))
	timer = db.Table('timer', metadata,
		db.Column('time', db.Text, primary_key=True),
		db.Column('process', db.String(200), db.ForeignKey("process.name"), nullable=False))

	metadata.create_all(engine)
	return [gpio, proc, timer]



def populateGPIO(gpio):
	engine.execute(gpio.insert(), id=7, name="pump1", 
		description="pump1", type="pump", group=1)
	engine.execute(gpio.insert(), id=11, name="valve1", 
		description="valve1", type="valve", group=1)
	engine.execute(gpio.insert(), id=13, name="valve2", 
		description="valve2", type="valve", group=1)
	engine.execute(gpio.insert(), id=15, name="valve3", 
		description="valve3", type="valve", group=1)
	engine.execute(gpio.insert(), id=12, name="valve4", 
		description="valve4", type="valve", group=1)
	engine.execute(gpio.insert(), id=16, name="valve5", 
		description="valve5", type="valve", group=1)
	engine.execute(gpio.insert(), id=18, name="valve6", 
		description="valve6", type="valve", group=1)
	engine.execute(gpio.insert(), id=22, name="valve7", 
		description="valve7", type="valve", group=1)
	engine.execute(gpio.insert(), id=29, name="testValve", 
		description="a test valve", type="valve", group=2)


def populateProcess(proc):
	engine.execute(proc.insert(), name="Sur la rambarde", 
		description="Turn valve2 and pump1 for 30 seconds.", filename='rambarde.json')
	engine.execute(proc.insert(), name="Tomates 2", 
		description="Turn valve3 and pump1 for 30 seconds.", filename='tomates2.json')
	engine.execute(proc.insert(), name="Lemongrass", 
		description="Turn valve4 and pump1 for 30 seconds.", filename='lemongrass.json')
	engine.execute(proc.insert(), name="Tomates and Coriandre", 
		description="Turn valve5 and pump1 for 30 seconds.", filename='tomates.json')
	engine.execute(proc.insert(), name="Concombre", 
		description="Turn valve6 and pump1 for 30 seconds.", filename='concombre.json')
	engine.execute(proc.insert(), name="Edamame", 
		description="Turn valve3 and pump1 for 60 seconds.", filename='edamame.json')

	engine.execute(proc.insert(), name="test", 
		description="Turn on testValve for 0.2", filename='test.json')


def populateTimer(timer):
	engine.execute(timer.insert(), time="09:00:00", process="test")
	engine.execute(timer.insert(), time="10:00:00", process="test")

if __name__ == '__main__':
	
	engine = db.create_engine("sqlite:///hardware.sqlite")
	conn = engine.connect()
	metadata = db.MetaData()
	gpio, proc, timer = createTables(metadata, engine)
	populateGPIO(gpio)
	populateProcess(proc)
	populateTimer(timer)

