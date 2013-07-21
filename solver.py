
def print_to_screen(card, message):
	print message
	print '  Card {0} at {1}, {2}'.format(card[0], card[1][0], card[1][1])

'''
Solves a given Total Recall game.
'''
class Solver():
	def __init__(self, backend, game_info, on_view = print_to_screen, on_match = print_to_screen):
		self.api = backend
		self.on_view = on_view
		self.on_match = on_match

		self.game = game_info['id']
		self.width = game_info['width']
		self.height = game_info['height']

		self.memory = {}

		self.current_card = 0


	def go(self):
		# cardN = (card_value, (x, y))
		# cardN_coord = (x, y)

		unused = None

		while self.cards_left() > 2:
			card1 = self.get_next_card()
			self.on_view(card1, 'Looking at next card (1)')
			if card1[0] in self.memory:
				#card2_coord = self.memory[card1[0]]
				#del self.memory[card1[0]]
				card2_coord = self.memory.pop(card1[0])
				self.on_match((card1[0], card2_coord), 'Matching with known card')
				guess = self.api.guess(card2_coord[0], card2_coord[1])
				assert guess == card1[0]
			else:
				card2 = self.get_next_card()
				self.on_view(card2, 'Looking at next card (2)')
				if card1[0] == card2[0]:
					# luck!
					self.on_match(card2, 'Lucky match')
				elif card2[0] in self.memory:
					## re-do the last card, but with the known card from memory
					## get rid of the old card 1
					#self.memory[card1[0]] = card1[1]
					## pick up the known card from the deck again
					#card1_coord = self.get_next_card_coord(-1)
					#card1_value = self.api.guess(card1_coord[0], card1_coord[1])
					#card1 = (card1_value, card1_coord)
					#self.on_match(card1, 'Picking up last card once again')
					#card2_coord = self.memory.pop(card1[0])
					#card2 = (card1[0], card2_coord)
					#self.on_match(card2, 'Matching with known card')
					#assert card1[0] == card2[0]

					# first, put away the card1
					self.memory[card1[0]] = card1[1]

					value = card2[0]
					card1_coord = self.memory.pop(value)
					card1_value = self.api.guess(card1_coord[0], card1_coord[1])
					card1 = (card1_value, card1_coord)
					self.on_match(card1, 'Picking up earlier known card')
					card2_coord = card2[1]
					card2_value = self.api.guess(card2_coord[0], card2_coord[1])
					card2 = (card2_value, card2_coord)
					self.on_match(card2, 'To match with this guy')
				else:
					# no luck, put both back
					self.memory[card1[0]] = card1[1]
					self.memory[card2[0]] = card2[1]

		#assert len(self.memory) + self.cards_left() == 2, 'There should be two cards left'
		#assert 0 <= len(self.memory) <= 1, 'Bad number of cards in memory'

		print self.memory
		end_value = None
		if len(self.memory) == 0:
			card1_coord = self.get_next_card_coord()
			card2_coord = self.get_next_card_coord(1)
			end_value = self.api.end(	card1_coord[0],
										card1_coord[1],
										card2_coord[0],
										card2_coord[1])
		else:
			(unused, card1_coord) = self.memory.popitem()
			card2_coord = self.get_next_card_coord()
			end_value = self.api.end(	card1_coord[0],
										card1_coord[1],
										card2_coord[0],
										card2_coord[1])
		return end_value

	def get_next_card(self):
		'''
		Get (by guessing) the next card

		:returns: (card_value, (x, y))
		'''
		coord = self.get_next_card_coord()
		card_value = self.api.guess(coord[0], coord[1])
		self.current_card += 1
		return (card_value, coord)

	def get_next_card_coord(self, add = 0):
		return self.index_to_coord(self.current_card + add)

	def index_to_coord(self, index):
		'''
		Gets the coordinates that correspond to a card index (taking in to
		account the width/height of the field)

		:param index: number from 0 to number of cards - 1
		:returns: (x, y)
		'''
		mod = index % self.width
		div = index / self.width
		return (mod, div)

	def cards_left(self):
		'''
		The number of cards left to be picked
		'''
		return self.width * self.height - self.current_card + len(self.memory)

