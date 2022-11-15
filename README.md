# Fall2022AI
### 8-puzzle game
**Goal**: Take random start board to the board [[0,1,2],[3,4,5],[6,7,8]] <br />
<br />
**Algorithms**: Breadth-First Search, Depth-First Search, A-star Search <br />
<br />
**Cost**: 
- The search space is the set of all possible boards reachable from the initial state. Each move consists of swapping the empty space with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}. Give each move a cost of one. Thus, the total cost of a path will
be equal to the number of moves made. <br />
- For A_star Search, the heuristic cost function is specified by the manhattan distance.

### Sudoku
**Goal**: Finish 9*9 sudoku game <br /> where rows denoted as A through I and columns denoted as 1 through 9
<br />
**Algorithms**: Backtracking Search using the minimum remaining value (MRV) heuristic and Forward Checking (FC) to reduce variables domains<br />
<br />

### 2048
**Introduction**: Treat 2048 as a two-player game in which Computer AI places tiles with a 90% probability of a 2 and 10% for a 4 and the Intelligent Player moves them. 
**Goal**: Reach as large number as possible before the board is full
<br />
**Algorithms**: Expectminimax, Alpha-Beta Pruning <br />
- GameManager.py: driver program that loads Computer AI and Player AI and
begins a game where they compete with each other.
- Grid.py: module defines the Grid object.
- BaseAI.py: This is the base class for any AI component. All AIs inherit from this module, and
implement the getMove() function, which takes a Grid object as parameter and returns a move.
- ComputerAI.py: This inherits from BaseAI. The getMove() function returns a computer
action that is a tuple (x, y) indicating the place you want to place a tile.
- **IntelligentAgent.py**: inherit from BaseAI where the getMove() function returns a number that indicates the player’s action. In particular, 0 stands for ”Up”, 1 stands for ”Down”, 2 stands for ”Left”, and 3 stands for ”Right”. 
- BaseDisplayer.py and Displayer.py: print the grid.
<br />
In expectminimax algorithm, if it takes too long to reach the utility value, it will change to use heuristic function as utility of the node in the middle. The heuristic function used in **IntelligentAgent.py** includes Empty Value Heuristic, Monotonicity Heuristic, Max Value Heuristic, Large number on corner Heuristic, Smoothness Heuristic. Some of the interpretations of the heuristics used can be found [here](https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048).
