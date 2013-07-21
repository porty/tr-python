#!/bin/python

import unittest
from solver import Solver

def print_nothing(card, message):
	pass

'''
Runs through a hard-coded game, and faults when a given move isn't what the
test is expecting

@author Robert McNeil
'''
class Test(unittest.TestCase):

	class Story:
		def __init__(self, width, height, test):
			self.test = test
			self.guesses = []
			self.end = None
			self.width = width
			self.height = height

		def add_guess(self, x, y, v):
			self.guesses.append((x, y, v))

		def add_end(self, a, b):
			self.end = (a, b)

		def do_guess(self, x, y):
			self.test.assertTrue(len(self.guesses) > 0, "Should not still be guessing")
			expected = self.guesses.pop(0)
			self.test.assertEquals(expected[0], x, "Wrong x in guess {0},{1}".format(x, y))
			self.test.assertEquals(expected[1], y, "Wrong y in guess {0},{1}".format(x, y))
			print ">> GUESS {0},{1} OK".format(x, y)
			return expected[2]

		def do_end(self, x1, y1, x2, y2):
			self.test.assertTrue(len(self.guesses) == 0, "Finished too early")
			actual = ((x1, y1), (x2, y2))
			self.test.assertEquals(self.end, actual, "Wrong end move (expected " + str(self.end) + ", got " + str(actual))
			print ">> END {0}, {1} OK".format(actual[0], actual[1])

		def get_info(self):
			return {'width': self.width, 'height': self.height, 'id': 'test'}

	def setUp(self):
		self.stories = []
		self.setUpStory1()

	def setUpStory1(self):
		#  0123
		# 0abbc
		# 1addc
		story = self.Story(4, 2, self)
		story.add_guess(0, 0, "a")
		story.add_guess(1, 0, "b")
		story.add_guess(2, 0, "b")
		story.add_guess(1, 0, "b")
		story.add_guess(3, 0, "c")
		story.add_guess(0, 1, "a")
		story.add_guess(0, 0, "a")
		story.add_guess(0, 1, "a")
		story.add_guess(1, 1, "d")
		story.add_guess(2, 1, "d")
		story.add_end((3, 0), (3, 1))
		self.stories.append(story)

	def tearDown(self):
		pass


	def testStories(self):
		for story in self.stories:
			self.playStory(story)

	def playStory(self, story):
		#o = Optimal(self.StoryPlayer(story), story.get_info())
		#o.go()
		class MockBackend:
			def __init__(self, story):
				self.story = story

			def guess(self, x, y):
				return self.story.do_guess(x, y)

			def end(self, x1, y1, x2, y2):
				return self.story.do_end(x1, y1, x2, y2)

		tr = MockBackend(story)
		solver = Solver(tr, story.get_info(), print_nothing, print_nothing)
		solver.go()

if __name__ == "__main__":
	# import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
