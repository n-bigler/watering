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
		description="pump1", type="valve", group=1)
	engine.execute(gpio.insert(), id=13, name="valve2", 
		description="pump1", type="valve", group=1)
	engine.execute(gpio.insert(), id=15, name="testValve", 
		description="a test valve", type="valve", group=2)


def populateProcess(proc):
	engine.execute(proc.insert(), name="amaryllis", 
		description="Turn valve1 and pump1 for 10 seconds.", filename='amaryllis.json')
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

