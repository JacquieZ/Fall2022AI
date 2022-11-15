# Fall2022AI
## School Coursework 1 - Artificial Intelligence
### 8-puzzle game
**Goal**: Take random start board to the board [[0,1,2],[3,4,5],[6,7,8]] <br />
<br />
**Algorithms**: Breadth-First Search, Depth-First Search, A-star Search <br />
<br />
**Cost**: 
- The search space is the set of all possible boards reachable from the initial state. Each move consists of swapping the empty space with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}. Give each move a cost of one. Thus, the total cost of a path will
be equal to the number of moves made. <br />
- For A_star Search, the heuristic cost function is specified by the manhattan distance.
