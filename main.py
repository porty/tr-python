#!/bin/python

'''
Runs the game, prints stuff to the screen

@author: Robert McNeil
'''

import settings
from backend import RestBackend
from solver import Solver

if __name__ == '__main__':
	backend = RestBackend()
	print 'Starting new game...'
	game_info = backend.new_game(settings.name, settings.email)
	solver = Solver(backend, game_info)
	end = solver.go()
	print end['message']
	if end['success']:
		print ":)"
	else:
		print ":("
