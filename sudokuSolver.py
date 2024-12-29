"""

Total Run time (seconds) 
Very Easy: 0.0486
Easy:      0.0317
Medium:    0.1218
Hard:      72.024
Overall:   1080.6

Average Run time (seconds)
Very Easy: 0.0032
Easy:      0.0021
Medium:    0.0081
Hard:      72.024

"""


from collections import defaultdict
from copy import deepcopy
import numpy as np

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
                    for k in range(9):
                        self.possible_moves[i, k].discard(num)
                        self.possible_moves[k, j].discard(num)
                    block_x, block_y = 3 * (i // 3), 3 * (j // 3)
                    for x in range(block_x, block_x + 3):
                        for y in range(block_y, block_y + 3):
                            self.possible_moves[x, y].discard(num)

    def solve(self) -> bool:
        """Attempt to solve the sudoku."""
        if self.is_solved():
            return True
        
        for i in range(9):
            for j in range(9):
                if self.board[i, j] == 0: 
                    for val in self.possible_moves[i, j]:
                        temp_board = deepcopy(self)
                        temp_board.board[i, j] = val
                        temp_board.update_possible_moves()
                        if temp_board.is_valid_sudoku() and \
                           temp_board.solve() and \
                           all(len(temp_board.possible_moves[x, y]) > 0 for x in range(9) for y in range(9) if temp_board.board[x, y] == 0):
                            self.board = temp_board.board
                            return True
                    return False  # Backtrack if no valid move found.
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
    return np.array([[-1 for _ in range(9)] for _ in range(9)])