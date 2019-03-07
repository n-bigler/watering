

class Device:
	def __init__(self, id, name, description, type, group):
		self.id =  id
		self.name = name
		self.description = description
		self.type=type
		self.group=group

	@staticmethod
	def fromDict(dic):
		return Device(dic['id'], dic['name'], dic['description'], dic['type'], dic['group'])


