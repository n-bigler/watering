from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as db

#Base = declarative_base()
#
#class gpio(Base):
#	__tablename__='gpio'
#	id = db.Column(db.Integer, primary_key=True)
#	name = db.Column(db.String(50), nullable=False)
#	description = db.Column(db.String(200))
#	type = db.Column(db.String(50), nullable=False, default="pump")
#	group = db.Column(db.Integer, nullable=False, default=1) 
#	
#	def __repr__(self):
#		return 'id: {}, name: {}, desc: {}, type: {}, group: {}'.format(self.id, self.name, description, type, group)


def populate(table):
	engine.execute(gpio.insert(), id=7, name="pump1", 
		description="pump1", type="pump", group=1)
	engine.execute(gpio.insert(), id=11, name="valve1", 
		description="pump1", type="valve", group=1)
	engine.execute(gpio.insert(), id=13, name="valve2", 
		description="pump1", type="valve", group=2)
	engine.execute(gpio.insert(), id=15, name="pump2", 
		description="pump2", type="pump", group=2)



if __name__ == '__main__':
	engine = db.create_engine("sqlite:///hardware.sqlite")
	conn = engine.connect()
	metadata = db.MetaData()
	gpio = db.Table('gpio', metadata, autoload=True, autoload_with=engine)
	populate(gpio)
	
