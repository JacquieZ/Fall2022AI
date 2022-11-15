from BaseAI import BaseAI
import time
import random
import math



class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        start_time = time.process_time()
        moveset = grid.getAvailableMoves()
        maxUtility = float('-inf')


        for child in moveset:
            move, moved_grid = child
            utility = self.expectminimax(moved_grid, 3, float('-inf'), float('inf'), start_time)

            if utility >= maxUtility:
                direction, maxUtility = move, utility

        return direction # it is a move

    def emptyHeuristic(self,grid):
        return len(grid.getAvailableCells())

    def monotonicityHeuristic(self, grid):
        differences = [0] * 4

        # left/right
        for check_row in range(4):
            current_col = 0
            next_col = current_col+1

            while grid.crossBound((check_row,next_col)):
                # check if the cell value is 0, jump over
                while grid.getCellValue((check_row,next_col)) == 0:
                    next_col += 1
                    if not grid.crossBound((check_row,next_col)):
                        break
                if not grid.crossBound((check_row, next_col)):
                    break

                currentValue = 0
                if grid.map[check_row][current_col] != 0:
                    currentValue = grid.map[check_row][current_col]

                nextValue = grid.map[check_row][next_col]

                if currentValue > nextValue:
                    differences[0] += currentValue - nextValue
                if nextValue > currentValue:
                    differences[1] += nextValue - currentValue

                current_col = next_col
                next_col+=1

        # up/down
        for check_col in range(4):

            current_row = 0
            next_row = current_row + 1
            while grid.crossBound((next_row,check_col)):
                # if the cell value is 0, jump over
                while grid.getCellValue((next_row,check_col)) == 0:
                    next_row += 1
                    if not grid.crossBound((next_row,check_col)):
                        break
                if not grid.crossBound((next_row,check_col)):
                    break

                currentValue = 0
                if grid.map[current_row][check_col] != 0:
                    currentValue = grid.map[current_row][check_col]

                nextValue = grid.map[next_row][check_col]

                if currentValue > nextValue:
                    differences[2] += currentValue - nextValue
                if  nextValue > currentValue:
                    differences[3] += nextValue - currentValue
                current_row = next_row
                next_row += 1

        return min(differences[0], differences[1]) + min(differences[2], differences[3])


    def maxValueHeuristic(self, grid):
        max = 0
        for i in range(4):
            for j in range(4):
                val = grid.getCellValue((i,j))
                if val > max:
                    max = val
        return math.log2(max)

    def largeOnCornerHeuristic(self,grid):
        positions_list = [(0, 0), (3, 0), (0, 3), (3, 3)]
        cell_value_list = []
        for position in positions_list:
            cell_value_list.append(grid.getCellValue(position))
        max = 0
        second_large = 0
        for i in range(4):
            for j in range(4):
                val = grid.getCellValue((i,j))
                if val > max:
                    max = val
        if max != 2:
            second_large = max/2
        if max and second_large in cell_value_list:
            return max+second_large
        elif max in cell_value_list:
            return max
        elif second_large in cell_value_list:
            return second_large
        else:
            return 0



    def smoothnessHeuristic(self, grid):
        smoothness = 0
        # left to right
        for row in grid.map:
            for col in range(3):
                smoothness += abs(row[col] - row[col + 1])

        # up to down
        for col in range(4):
            for row in range(3):
                smoothness += abs(grid.map[row][col] - grid.map[row + 1][col])

        return smoothness

    def Heuristic(self,grid):
        return 28.0 * self.emptyHeuristic(grid) - 11.2 * self.monotonicityHeuristic(grid) - \
               0.7 * self.maxValueHeuristic(grid) + 0.4 * self.largeOnCornerHeuristic(grid) - 0.1 * self.smoothnessHeuristic(grid)
    # def Maximize(self, grid, alpha, beta,start_time):
    #     if not grid.canMove():
    #         return (None,grid.getMaxTile())
    #
    #
    #     (maxGrid,maxUtility) = (None,float('-inf'))
    #     for child in grid.getAvailableMoves():
    #         move,grid_moved = child
    #
    #         if time.process_time() - start_time >= maxTime:
    #             return (child,self.Heuristic(grid))
    #
    #         (_,utility) = self.Minimize(grid_moved,alpha,beta,start_time)
    #
    #         if utility > maxUtility:
    #             maxChild,maxUtility = child,utility
    #         if maxUtility >= beta:
    #             break
    #         if maxUtility > alpha:
    #             alpha = maxUtility
    #
    #     return (maxChild,maxUtility)
    #
    # def Minimize(self, grid, alpha, beta,start_time):
    #     if not grid.canMove():
    #         return (None,grid.getMaxTile())
    #
    #     (minGrid,minUtility) = (None,float('inf'))
    #     for child in grid.getAvailableMoves():
    #         move,grid_moved = child
    #
    #         if time.process_time() - start_time >= maxTime:
    #             return (child,self.Heuristic(grid))
    #
    #         (_,utility) = self.Maximize(grid_moved,alpha,beta,start_time)
    #
    #         if utility < minUtility:
    #             minChild,minUtility = child,utility
    #         if minUtility <= alpha:
    #             break
    #         if minUtility < beta:
    #             beta = minUtility
    #
    #     return (minChild,minUtility)

    def expectminimax(self, grid, depth, alpha, beta, start):

        if time.process_time() - start > 0.20/60 or depth == 0:
            return self.Heuristic(grid)
        minUtility = float("inf")

        # computer gives 2
        grid2 = grid.clone()
        move2 = random.choice(grid2.getAvailableCells()) #if grid.getAvailableCells() else None
        grid2.setCellValue(move2, 2)
        utility2 = (self.maxSearch(grid2, depth, alpha, beta, start))


        # computer gives 4
        grid4 = grid.clone()
        move4 = random.choice(grid4.getAvailableCells()) #if grid.getAvailableCells() else None
        grid4.setCellValue(move4, 4)
        utility4 = (self.maxSearch(grid4, depth, alpha, beta, start))

        # calculate the expectation
        expectUtility = 0.9 * utility2 + 0.1 * utility4
        minUtility = min(minUtility, expectUtility)
        #beta = min(beta, minUtility)
        return minUtility

    def maxSearch(self, grid, depth, alpha, beta, start):

        maxUtility = float("-inf")
        moveset = grid.getAvailableMoves()

        for move in moveset:
            utility = self.expectminimax(move[1], depth - 1, alpha, beta, start)

            if utility > maxUtility:
                maxUtility = utility

            if maxUtility >= beta:
                break
            alpha = max(maxUtility, alpha)
        return maxUtility
