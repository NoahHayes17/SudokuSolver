# History of Optimisations

## Version 1
I initially made a basic constraint propagation, backtracking algorithm with no optimisations. The motivation behind this was to become more familiar with the problems I would have to overcome and to give myself a foundation to iterate. This solution would go through every cell on the board and every value it could take, check whether the board was valid for each (using constraint propagation), and backtrack if not. 

## Version 2
I then built upon my initial solver by implementing heuristics to explore the path of the cell that was the most constraining, choosing the value for that cell that was the least constraining, and forward checking, which provided a significant improvement in runtime.

## Version 3
I tinkered with the previous solver and realised that choosing the least constraining value created more overhead (when counting and sorting by this constraint) than benefit. The benefit is a reduction in the likelihood of reaching dead ends by keeping choices as open as possible for future assignments.

## Version 4
The final version sees significant change because, to reduce the runtime, I needed to avoid deep copies. I also improved forward checking to check affected cells only, rather than looping through the entire board. This led to a more efficient way of updating the possible moves since I now only update the affected cells. I also put the check for a valid board outside the solve function (so it is only called once) and backtracked using a valid flag. This significantly improved the runtime.

# Table for Total Runtime for Each Section

| Difficulty | Very Easy (s) | Easy (s) | Medium (s) | Hard (s) | Overall (s) |
|------------|---------------|----------|------------|----------|-------------|
| **Version 1** | 0.0486        | 0.1218   | 0.1218     | 72.024   | 1080.6      |
| **Version 2** | 0.0447        | 0.0338   | 0.1036     | 20.215   | 20.397      |
| **Version 3** | 0.0071        | 0.0045   | 0.0154     | 1.3713   | 1.3983      |
| **Version 4** | 0.0037        | 0.0026   | 0.0062     | 0.4575   | 0.4701      |

# Description of Algorithm

The algorithm starts with the identification of possible moves for each empty cell based on sudoku rules (row, column, and 3x3 block constraints). The solving process involves using a depth-first search with constraint propagation and backtracking, selecting the most constrained cell (the one with the fewest possible moves) to prioritise decisions that reduce the search space, and using forward checking to prune invalid states early.

To remove the need for deep copies, I did the following: when investigating a possible value assignment, I stored all the possible values of affected cells before I filled/assigned them during the exploration of states. Then, if the move was valid, these affected cells would be removed from the dictionary of possible moves. In the case of backtracking, I would go through these affected cells and repopulate their values. Hence, if a chosen value leads to no valid moves, the algorithm backtracks, restoring the prior state. This works because each call of `solve()` has its own scope, so I do not need to worry about conflicts in memory between calls. Additionally, dictionaries are immutable, so with each assignment of `affected_cells_moves`, a new dictionary is created in memory. Hence, at each recursion level, I have an isolated `affected_cells_moves` which can be used to backtrack at that call of `solve()`. 

The recursion and backtracking continue until the puzzle is solved or all possibilities are exhausted. The function which checks if the board is valid iterates over all cells. If a conflict occurs, it returns false; otherwise, it adds that cell to a dictionary, which is used in future iterations to check for conflict.

# Optimisations and Complexity

The improvements mentioned above drastically lowered the runtime complexity. Initially, the algorithm had a time complexity of $O(9^k)$ for k empty cells. This is because each cell can take values 1 through 9, and if a chosen value is invalid, then we can choose from the set `{x | 0 < x < 10, x ≠ invalid value}`, and this can happen up to 9 times. This is driven by the backtracking nature of the algorithm and dominates the algorithm's complexity. 

The optimised version reduced this significantly by prioritising constrained cells and limiting updates to directly affected cells. This reduced the effective branching factor and pruned the search space earlier, resulting in a runtime closer to $O(b^k)$, where b is the reduced branching factor (reduced from 9), even if the theoretical complexity is the same. The space complexity is $O(1)$ due to the fixed nature of the board; there is a maximum recursion depth of 81 with a fixed amount of data stored at each level (namely the current cell, the affected cells, and the possible values).

# Reflections and Suggestions for Further Work

My improvements garnered significant decreases in runtime, as shown in the timeline of my approach. However, upon further research, I discovered more complex methods which led to an almost 10x further reduction in runtime. Despite this, I was satisfied my current runtime had surpassed the desired goal of the assignment and concluded the benefits from further optimisations were unnecessary. However, in the future, I would like to implement better pruning strategies, such as Naked Pairs/Triples and Hidden Singles, use specific data structures like Dancing Links, and apply arc consistency to improve my look-ahead.

# References 

- Wikipedia contributors, 2024. [Look-ahead (backtracking)](https://en.wikipedia.org/wiki/Look-ahead_(backtracking)) [Online]. Available from: https://en.wikipedia.org/wiki/Look-ahead_(backtracking) [Accessed 24 December 2024]
- Barton, R., 2009. [Optimizing the backtracking algorithm solving Sudoku](https://stackoverflow.com/questions/1518346/optimizing-the-backtracking-algorithm-solving-sudoku) [Online]. Available from: https://stackoverflow.com/questions/1518346/optimizing-the-backtracking-algorithm-solving-sudoku [Accessed 30 December 2024]
