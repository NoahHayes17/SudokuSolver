"""

Total Run time per category of sudoku (seconds) 
Very Easy: 0.0447
Easy:      0.0338
Medium:    0.1036
Hard:      20.215
Overall:   20.397

Average Run Time Per Category of sudoku (seconds)
Very Easy: 0.0030
Easy:      0.0023
Medium:    0.0069
Hard:      1.3477

"""


import numpy as np
from collections import defaultdict
from copy import deepcopy

class Sudoku:
    def __init__(self, board: np.ndarray):
        self.board = board
        self.possible_moves = np.array([[set(range(1, 10)) if board[i, j] == 0 else set() for j in range(9)] for i in range(9)])
        self.update_possible_moves()

    def update_possible_moves(self):
        """Update possible moves for all cells based on current board state."""
        for i in range(9):
            for j in range(9):
                if self.board[i, j] != 0:
                    num = self.board[i, j]
                    self.possible_moves[i, j].clear()
                    # Eliminate the number from the corresponding row, column, and block
                    for k in range(9):
                        self.possible_moves[i, k].discard(num)
                        self.possible_moves[k, j].discard(num)
                    block_x, block_y = 3 * (i // 3), 3 * (j // 3)
                    for x in range(block_x, block_x + 3):
                        for y in range(block_y, block_y + 3):
                            self.possible_moves[x, y].discard(num)

    def find_most_constrained_cell(self) -> tuple:
        """Find the cell with the least number of possible values."""
        min_possibilities = float('inf')
        most_constrained_cell = None
        for i in range(9):
            for j in range(9):
                if self.board[i, j] == 0:
                    num_possibilities = len(self.possible_moves[i, j])
                    if 0 < num_possibilities < min_possibilities:
                        min_possibilities = num_possibilities
                        most_constrained_cell = (i, j)
        return most_constrained_cell
        
    def least_constraining_value(self, i: int, j: int) -> list[int]: 
        """Find the values for a cell sorted by least constraining (that value affects the least amount of cells)."""
        if self.board[i, j] != 0:
            return []

        possible_values = list(self.possible_moves[i, j])
        value_scores = {}
        
        for val in possible_values:
            affected_cells = set()
            # Find cells that would be affected by placing val here
            for row in range(9):
                if val in self.possible_moves[row, j]:
                    affected_cells.add((row, j))
            for col in range(9):
                if val in self.possible_moves[i, col]:
                    affected_cells.add((i, col))
            block_x, block_y = 3 * (i // 3), 3 * (j // 3)
            for x in range(block_x, block_x + 3):
                for y in range(block_y, block_y + 3):
                    if val in self.possible_moves[x, y]:
                        affected_cells.add((x, y))

            # Score: how many values would be removed from other cells if val is chosen
            value_scores[val] = len(affected_cells)

        # Return the values sorted by the least constraining value (the least affected cells)
        sorted_values = sorted(value_scores, key=value_scores.get)
        return sorted_values
        
    def solve(self) -> bool:
        """"Attempt to solve the sudoku."""
        if self.is_solved():
            return True
        
        cell = self.find_most_constrained_cell()
        if not cell:  # No empty cells left
            return False
        
        i, j = cell
        values_to_try = self.least_constraining_value(i, j)
    
        for val in values_to_try:
            temp_board = deepcopy(self)
            temp_board.board[i, j] = val
            temp_board.update_possible_moves()
    
            # Perform forward checking: If any affected cell has no possible moves, backtrack
            if all(len(temp_board.possible_moves[x, y]) > 0 for x in range(9) for y in range(9) if temp_board.board[x, y] == 0):
                if temp_board.solve():
                    self.board = temp_board.board
                    return True
    
        return False

    def is_filled(self) -> bool:
        """Check if the board is completely filled."""
        return np.all(self.board > 0)

    def is_valid_sudoku(self) -> bool:
        """Check if the current board's arrangement of numbers is valid."""
        cols = defaultdict(set)
        rows = defaultdict(set)
        squares = defaultdict(set)

        for row in range(9):
            for col in range(9):
                num = self.board[row, col]
                if num == 0:
                    continue
                if (num in rows[row] or 
                    num in cols[col] or 
                    num in squares[(row // 3, col // 3)]):
                    return False
                rows[row].add(num)
                cols[col].add(num)
                squares[(row // 3, col // 3)].add(num)
        return True

    def is_solved(self) -> bool:
        """Check if the board is both filled and valid."""
        return self.is_filled() and self.is_valid_sudoku()

def sudoku_solver(board: np.ndarray) -> np.ndarray:
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        board : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    sudoku = Sudoku(board)
    if sudoku.solve():
        return sudoku.board
    return np.full((9, 9), -1)
