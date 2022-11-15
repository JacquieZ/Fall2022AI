from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource
import heapq


class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def __lt__(self, other_state):
        self_cost = self.cost + calculate_total_cost(self)
        other_state_cost = other_state.cost + calculate_total_cost(other_state)
        return self_cost < other_state_cost

    def __eq__(self, other_state):
        self_cost = self.cost + calculate_total_cost(self)
        other_state_cost = other_state.cost + calculate_total_cost(other_state)
        return self_cost == other_state_cost

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None
        else:
            new_config = self.config.copy()
            old_index = self.blank_index
            new_index = self.blank_index - self.n
            num = new_config[new_index]
            new_config[new_index] = 0
            new_config[old_index] = num


        return PuzzleState(new_config, self.n, self, "Up", self.cost + 1)

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index > self.n * self.n - 1 - self.n:
            return None
        else:
            new_config = self.config.copy()
            old_index = self.blank_index
            new_index = self.blank_index + self.n
            num = new_config[new_index]
            new_config[new_index] = 0
            new_config[old_index] = num

        return PuzzleState(new_config, self.n, self, "Down", self.cost + 1)

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None
        else:
            new_config = self.config.copy()
            old_index = self.blank_index
            new_index = self.blank_index - 1
            num = new_config[new_index]
            new_config[new_index] = 0
            new_config[old_index] = num

        return PuzzleState(new_config, self.n, self, "Left", self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == self.n - 1:
            return None
        else:
            new_config = self.config.copy()
            old_index = self.blank_index
            new_index = self.blank_index + 1
            num = new_config[new_index]
            new_config[new_index] = 0
            new_config[old_index] = num

        return PuzzleState(new_config, self.n, self, "Right", self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(actions, cost_of_path,nodes_expanded, max_search_depth, running_time, max_memory_used):
    with open('output.txt', 'a') as f:
        f.write('path_to_goal: ' + str(actions) + '\n')
        f.write('cost_of_path: ' + cost_of_path + '\n')
        f.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
        f.write('search_depth: ' + cost_of_path + '\n')
        f.write('max_search_depth: ' + str(max_search_depth) + '\n')
        f.write('running_time: ' + str(round(running_time, 8)) + '\n')
        f.write('max_ram_usage: ' + str(round(max_memory_used, 8)) + '\n')

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Q.Queue()
    frontier.put(initial_state)
    frontier_configs = set() # prepared to find the appearance of neighbors' config is in the frontier
    frontier_configs.add(tuple(initial_state.config))
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.get()
        frontier_configs.remove(tuple(state.config))
        explored.add(tuple(state.config))

        if test_goal(state):
            actions = list()
            cost_of_path = str(state.cost)
            while state.action: # find all actions starting from the goal_state
                if state.action =='Initial':
                    break
                actions.append(state.action)
                state = state.parent
            actions.reverse() # we need the path starting from the initial node
            return actions, cost_of_path, nodes_expanded, max_search_depth

        neighbors = state.expand()
        nodes_expanded += 1

        for neighbor in neighbors:
            max_search_depth = max(neighbor.cost, max_search_depth)
            if (tuple(neighbor.config) not in explored) and (tuple(neighbor.config) not in frontier_configs):
                frontier.put(neighbor)
                frontier_configs.add(tuple(neighbor.config))

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = [initial_state]
    frontier_configs= set() # prepared to find the appearance of neighbors' config is in the frontier
    frontier_configs.add(tuple(initial_state.config))
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while len(frontier):
        state = frontier.pop()
        frontier_configs.remove(tuple(state.config))
        explored.add(tuple(state.config))

        if test_goal(state):
            actions = list()
            cost_of_path = str(state.cost)
            while state.action: # find all actions starting from the goal_state
                if state.action =='Initial':
                    break
                actions.append(state.action)
                state = state.parent
            actions.reverse() # we need the path starting from the initial node
            return actions, cost_of_path, nodes_expanded, max_search_depth

        neighbors = state.expand()
        neighbors.reverse()
        nodes_expanded += 1

        for neighbor in neighbors:
            max_search_depth = max(neighbor.cost, max_search_depth)
            if (tuple(neighbor.config) not in explored) and (tuple(neighbor.config) not in frontier_configs):
                frontier.append(neighbor)
                frontier_configs.add(tuple(neighbor.config))
    return False

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = list()
    heapq.heappush(frontier, (calculate_total_cost(initial_state), initial_state)) # (priority,state); g(initial)=0
    frontier_configs = set() # prepared to find the appearance of neighbors' config is in the frontier
    frontier_configs.add(tuple(initial_state.config))
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while len(frontier):
        state_ttl_cost, state = heapq.heappop(frontier)
        frontier_configs.remove(tuple(state.config))
        explored.add(tuple(state.config))

        if test_goal(state):
            actions = list()
            cost_of_path = str(state_ttl_cost)
            while state.action: # find all actions starting from the goal_state
                if state.action =='Initial':
                    break
                actions.append(state.action)
                state = state.parent
            actions.reverse() # we need the path starting from the initial node
            return actions, cost_of_path, nodes_expanded, max_search_depth

        neighbors = state.expand()
        nodes_expanded+=1

        for neighbor in neighbors:
            neighbor_ttl_cost = neighbor.cost + calculate_total_cost(neighbor) # f(n)=g(n)+h(n)
            max_search_depth = max(neighbor.cost, max_search_depth)
            if (tuple(neighbor.config) not in explored) and (tuple(neighbor.config) not in frontier_configs):
                heapq.heappush(frontier, (neighbor_ttl_cost, neighbor))
                frontier_configs.add(tuple(neighbor.config))
            elif tuple(neighbor.config) in frontier_configs:
                for i in range(len(frontier)):
                    # the following condition locates the neighbor in the frontier and if the priority can be decreased
                    # to represent lower cost, then update it
                    if (tuple(frontier[i][1].config) == tuple(neighbor.config)) and (frontier[i][0] >= neighbor_ttl_cost):
                        frontier.pop(i)
                        heapq.heappush(frontier, (neighbor_ttl_cost, neighbor))
    return False


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    total_cost = 0
    for i in range(1, (state.n*state.n)): # moving numbers 1-8 in the puzzle
        total_cost += calculate_manhattan_dist(state.config.index(i), i, state.n)
    return total_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    current_row = int(idx / n)
    current_col = idx % n
    ideal_row = int(value / n)
    ideal_col = value % n
    distance = abs(current_row - ideal_row) + abs(current_col - ideal_col)
    return distance

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    for i in range(puzzle_state.n * puzzle_state.n):
        if i == puzzle_state.config[i]:
            pass
        else:
            return False
    return True

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    if   search_mode == "bfs":
        actions, cost_of_path, nodes_expanded, max_search_depth = bfs_search(hard_state)
    elif search_mode == "dfs":
        actions, cost_of_path, nodes_expanded, max_search_depth = dfs_search(hard_state)
    elif search_mode == "ast":
        actions, cost_of_path, nodes_expanded, max_search_depth = A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    end_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2 ** 20)
    print("Program completed in %.3f second(s)"%(end_time-start_time))

    running_time = end_time - start_time
    max_memory_used = start_ram - end_ram

    writeOutput(actions, cost_of_path,nodes_expanded,max_search_depth,running_time,max_memory_used)

if __name__ == '__main__':
    main()