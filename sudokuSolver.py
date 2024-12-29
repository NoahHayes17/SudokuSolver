"""

Total Run time (seconds) 
Overall:   0.4701
Very Easy: 0.0037
Easy:      0.0026
Medium:    0.0062
Hard:      0.4575

Average Run time (seconds)
Very Easy: 0.0002
Easy:      0.0002
Medium:    0.0004
Hard:      0.0305

"""

import numpy as np
from collections import defaultdict
from typing import Dict, Set, Tuple


class Sudoku:
    def __init__(self, board: np.ndarray) -> None:
        """Initialize Sudoku solver with a board.
        
        Args:
            board: 9x9 numpy array representing the Sudoku puzzle
        """
        self.board = board.copy()
        self.possible_moves = {}
        self.initialize_possible_moves()

    def get_valid_moves(self, row: int, col: int) -> Set[int]:
        """Get all valid moves for a cell.
        
        Args:
            row: Row index of the cell
            col: Column index of the cell
            
        Returns:
            Set of valid values that can be placed in the cell
        """
        if self.board[row][col] != 0:
            return set()
            
        conflicting_values = set()

        for i in range(9):
            if self.board[i][col] != 0:
                conflicting_values.add(self.board[i][col])
            if self.board[row][i] != 0:
                conflicting_values.add(self.board[row][i])

        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] != 0:
                    conflicting_values.add(self.board[i][j])
        return set(range(1, 10)) - conflicting_values

    def initialize_possible_moves(self) -> None:
        """Initialize possible moves for all empty cells."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    moves = self.get_valid_moves(i, j)
                    if moves:
                        self.possible_moves[(i, j)] = set(moves)

    def find_most_constrained_cell(self) -> tuple[int, int] | None:
        """Find the cell with the least number of possible values.
        
        Returns:
            Tuple of (row, col) for the most constrained cell, or None if no moves possible
        """
        if not self.possible_moves:
            return None
        return min(self.possible_moves.items(), key=lambda x: len(x[1]))[0]

    def is_valid_board(self) -> bool:
        """Check if the current board's arrangement of numbers is valid.
        
        Returns:
            Boolean indicating if the current board state is valid
        """
        cols = defaultdict(set)
        rows = defaultdict(set)
        boxes = defaultdict(set)

        for row in range(9):
            for col in range(9):
                num = self.board[row, col]
                if num == 0:
                    continue
                if (num in rows[row] or 
                    num in cols[col] or 
                    num in boxes[(row // 3, col // 3)]):
                    return False
                rows[row].add(num)
                cols[col].add(num)
                boxes[(row // 3, col // 3)].add(num)
        return True
    
    def store_state(self, row: int, col: int, affected_cells: Dict[Tuple[int, int], Set[int]]) -> None:
        """Store current state of affected cells for backtracking.
        
        Args:
            row: Row index of the current cell
            col: Column index of the current cell
            affected_cells: Dictionary to store the affected cells' moves
        """
        for i in range(9):
            for j in range(9):
                if (i == row or j == col or 
                   (i//3 == row//3 and j//3 == col//3)) and (i, j) in self.possible_moves:
                    affected_cells[(i, j)] = self.possible_moves[(i, j)].copy()
                    
    def forward_checking(self, affected_cells: Dict[Tuple[int, int], Set[int]], value: int) -> bool:
        """Perform forward checking: If any affected cell has no possible moves, backtrack.
        
        Args:
            affected_cells: Dictionary of cells affected by the current move
            value: Value being placed in the current cell
            
        Returns:
            Boolean indicating if the move is valid
        """
        valid = True
        for pos in affected_cells:
            if pos in self.possible_moves:
                self.possible_moves[pos].discard(value)
                if not self.possible_moves[pos]:
                    valid = False
                    break
        return valid

    def backtrack(self, row: int, col: int, stored_moves: Dict[Tuple[int, int], Set[int]]) -> None:
        """Restores the previous state before an invalid move was made.
        
        Args:
            row: Row index of the cell to backtrack
            col: Column index of the cell to backtrack
            stored_moves: Dictionary of stored moves to restore
        """
        self.board[row, col] = 0
        for pos, moves in stored_moves.items():
            if pos in self.possible_moves:
                self.possible_moves[pos] = moves
    
    def solve(self) -> bool:
        """Attempt to solve the sudoku.
        
        Returns:
            Boolean indicating if a solution was found
        """
        if not self.possible_moves: 
            return all(0 not in row for row in self.board)

        row, col = self.find_most_constrained_cell()
        possible_values = list(self.possible_moves[(row, col)])  
        
        del self.possible_moves[(row, col)]
        
        for value in possible_values:
            self.board[row, col] = value
            affected_cells_moves = {}
            self.store_state(row, col, affected_cells_moves)
            valid_move = self.forward_checking(affected_cells_moves, value)
            if valid_move and self.solve():
                return True
            self.backtrack(row, col, affected_cells_moves)
            
        self.possible_moves[(row, col)] = set(possible_values)
        return False

def sudoku_solver(board: np.ndarray) -> np.ndarray:
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Args
        board : 9x9 numpy array
            Empty cells are designated by 0.

    Returns
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    sudoku = Sudoku(board)
    if not sudoku.is_valid_board():
        return np.full((9, 9), -1)
    elif sudoku.solve():
        return sudoku.board
    return np.full((9, 9), -1)
