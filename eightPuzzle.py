'''
CS 170 - Artificial Interlligence
Project 1 - Eight Puzzle
Sungho Ahn, 862026328
sahn025@ucr.edu
Nov 02, 2019
'''

import sys
import copy
from heapq import heappush, heappop, heapify


default_puzzle = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]
goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class Node:
	def __init__(self, puzzle, heuristic, depth):
		self.puzzle = puzzle
		self.heuristic = heuristic
		self.depth = depth
		self.cost = heuristic + depth

	def __cmp__(self, other):
		return cmp(self.cost, other.cost)

	def __lt__(self, other):
		return self.cost < other.cost


def main():
	puzzle_option = input("\n   ::: Eight-Puzzle Solver :::\n\n" +
				"Please choose an option from the following:\n" +
				"Type '1' to use a default puzzle\n" +
				"Type '2' to create a new puzzle\n>> ")

	if puzzle_option == '1':
		puzzle = default_puzzle

	if puzzle_option == '2':
		print("\nYou choose to create your own puzzle\n" +
			"- Enter the numbers for each row\n"
			"- Numbers separated by a space\n"
			"- Replace the blank with a zero\n")

		row1 = input("Enter the first row: ")
		row2 = input("Enter the second row: ")
		row3 = input("Enter the third row: ")

		row1 = row1.split()
		row2 = row2.split()
		row3 = row3.split()

		for col in range(0, 3):
			row1[col] = int(row1[col])
			row2[col] = int(row2[col])
			row3[col] = int(row3[col])

		puzzle = [row1, row2, row3]

	algorithm = input("\nPlease choose an option from the following:\n" +
			"Type '1' to use Uniform Cost Search algorithm\n" +
			"Type '2' to use A* with the Misplaced Tile heuristic algorithm\n" +
			"Type '3' to use A* with the Manhattan Distance heuristic algorithm\n>> ")

	searchAlgorithm(puzzle, algorithm)

	return


def searchAlgorithm(puzzle, algorithm):
	expanded = max_nodes = 0

	if algorithm == '1':
		starting_node = Node(puzzle, 0, 0)

	if algorithm == '2':
		heuristic = misplacedTile(puzzle)
		starting_node = Node(puzzle, heuristic, 0)

	if algorithm == '3':
		heuristic = manhattanDistance(puzzle)
		starting_node = Node(puzzle, heuristic, 0)

	q = []
	heappush(q, starting_node)

	print('\nExpanding state:')
	printState(starting_node)


	while True:
		if len(q) == 0:
			print("Error: Empty Nodes")
			break

		heapify(q)
		temp = heappop(q)
		printBestState(temp)

		if temp.puzzle == goal_puzzle:
			print('')
			print('Goal!!\n')
			print('To solve this problem the search algorithm expanded a total of', expanded, 'nodes')
			print('The maximum number of nodes in the queue at any one time was', max_nodes)
			print('The depth of the goal node was', temp.depth)
			break

		else:
			temp_list, expanded = expandNodes(temp, expanded)

			for n in range(len(temp_list)):
				if algorithm == '1':
					temp_list[n].heuristic = 0
				if algorithm == '2':
					temp_list[n].heuristic = misplacedTile(temp_list[n].puzzle)
					temp_list[n].cost = temp_list[n].heuristic + temp_list[n].depth
				if algorithm == '3':
					temp_list[n].heuristic = manhattanDistance(temp_list[n].puzzle)
					temp_list[n].cost = temp_list[n].heuristic + temp_list[n].depth

				heappush(q, temp_list[n])

			if max_nodes < len(q):
				max_nodes = len(q)


def misplacedTile(puzzle):
	heuristic = 0
	for i in range(0, 3):
		for j in range(0, 3):
			if puzzle[i][j] != 0:
				if puzzle[i][j] != goal_puzzle[i][j]:
					heuristic += 1

	return heuristic


def manhattanDistance(puzzle):
	heuristic = 0
	for number in range(1,9):
		for i in range(0, 3):
			for j in range(0, 3):
				if number == puzzle[i][j]:
					row = i
					col = j
				if number == goal_puzzle[i][j]:
					goal_row = i
					goal_col = j
		heuristic += (abs(row - goal_row) + abs(col - goal_col))

	return heuristic


def expandNodes(temp, expanded):
	lst = []
	depth = temp.depth + 1
	blank_in_row = blacnk_in_col = 0

	for i in range(0, 3):
		for j in range(0, 3):
			if temp.puzzle[i][j] == 0:
				blank_in_row = i
				blank_in_col = j

	if blank_in_row != 0:
		top_cp = copy.deepcopy(temp.puzzle)
		top_cp[blank_in_row][blank_in_col] = top_cp[blank_in_row - 1][blank_in_col]
		top_cp[blank_in_row - 1][blank_in_col] = 0
		top_node = Node(top_cp, 0, depth)
		lst.append(top_node)
		expanded += 1

	if blank_in_row != 2:
		bot_cp = copy.deepcopy(temp.puzzle)
		bot_cp[blank_in_row][blank_in_col] = bot_cp[blank_in_row + 1][blank_in_col]
		bot_cp[blank_in_row + 1][blank_in_col] = 0
		bot_node = Node(bot_cp, 0, depth)
		lst.append(bot_node)
		expanded += 1

	if blank_in_col != 0:
		left_cp = copy.deepcopy(temp.puzzle)
		left_cp[blank_in_row][blank_in_col] = left_cp[blank_in_row][blank_in_col - 1]
		left_cp[blank_in_row][blank_in_col - 1] = 0
		left_node = Node(left_cp, 0, depth)
		lst.append(left_node)
		expanded += 1

	if blank_in_col != 2:
		right_cp = copy.deepcopy(temp.puzzle)
		right_cp[blank_in_row][blank_in_col] = right_cp[blank_in_row][blank_in_col + 1]
		right_cp[blank_in_row][blank_in_col + 1] = 0
		right_node = Node(right_cp, 0, depth)
		lst.append(right_node)
		expanded += 1

	return lst, expanded


def printState(puzzle):
	print(puzzle.puzzle[0][0], puzzle.puzzle[0][1], puzzle.puzzle[0][2])
	print(puzzle.puzzle[1][0], puzzle.puzzle[1][1], puzzle.puzzle[1][2])
	print(puzzle.puzzle[2][0], puzzle.puzzle[2][1], puzzle.puzzle[2][2])


def printBestState(puzzle):
	print('\nThe best state to expand with a g(n) =', puzzle.depth, 'and h(n) =', puzzle.heuristic, 'is...')
	printState(puzzle)
	print('Expanding this node...')


if __name__ == "__main__":
	main()
