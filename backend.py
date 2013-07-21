from rest import Rest

'''
My attempt at an interface
'''
class Backend(object):
	def new_game(self, name, email):
		return { "width": 2, "height": 1, "id": "base" }

	def guess(self, x, y):
		return "?"

	def end(self, x1, y1, x2, y2):
		return {"success": False, "message": "I have no implementation"}

'''
A game backend using a REST interface
'''
class RestBackend(Backend):
	def __init__(self, rest = Rest("http://totalrecall.99cluster.com/games/")):
		self.rest = rest
		self.game_id = ""

	def new_game(self, name, email):
		data = self.rest.jpost(name = name, email = email)
		assert data["id"] != None
		self.game_id = data["id"]
		return data

	def guess(self, x, y):
		url = "{0}/cards/{1},{2}".format(self.game_id, x, y)
		return self.rest.get(url)

	def end(self, x1, y1, x2, y2):
		url = self.game_id + "/end"
		return self.rest.jpost(url, x1 = x1, y1 = y1, x2 = x2, y2 = y2)
