import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Maze:
    def __init__(self, num_rows, num_cols, start_row, start_col, end_row, end_col):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.Memory_units = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
        self.image = np.zeros((num_rows * 10, num_cols * 10), dtype=np.uint8)
        self.history = [(start_row, start_col)]

    def DFS_MazeGenerate(self):
        while self.history:
            # Mark current position as visited
            self.Memory_units[self.start_row, self.start_col, 4] = 1

            # Check neighboring cells for unvisited ones
            check = []
            if self.start_col > 0 and self.Memory_units[self.start_row, self.start_col - 1, 4] == 0:
                check.append('L')
            if self.start_row > 0 and self.Memory_units[self.start_row - 1, self.start_col, 4] == 0:
                check.append('U')
            if self.start_col < self.num_cols - 1 and self.Memory_units[self.start_row, self.start_col + 1, 4] == 0:
                check.append('R')
            if self.start_row < self.num_rows - 1 and self.Memory_units[self.start_row + 1, self.start_col, 4] == 0:
                check.append('D')

            if len(check) > 0:
                # Push current position to history stack
                self.history.append([self.start_row, self.start_col])

                # Move in a randomly chosen direction and open the corresponding wall
                move_direction = random.choice(check)
                if move_direction == 'L':
                    self.Memory_units[self.start_row, self.start_col, 0] = 1
                    self.start_col = self.start_col - 1
                    self.Memory_units[self.start_row, self.start_col, 2] = 1
                elif move_direction == 'U':
                    self.Memory_units[self.start_row, self.start_col, 1] = 1
                    self.start_row = self.start_row - 1
                    self.Memory_units[self.start_row, self.start_col, 3] = 1
                elif move_direction == 'R':
                    self.Memory_units[self.start_row, self.start_col, 2] = 1
                    self.start_col = self.start_col + 1
                    self.Memory_units[self.start_row, self.start_col, 0] = 1
                elif move_direction == 'D':
                    self.Memory_units[self.start_row, self.start_col, 3] = 1
                    self.start_row = self.start_row + 1
                    self.Memory_units[self.start_row, self.start_col, 1] = 1
            else:
                self.start_row, self.start_col = self.history.pop()

        # Open walls at the maze's start and end points
        self.Memory_units[0, 0, 0] = 1
        self.Memory_units[self.end_row, self.end_col, 2] = 1

        # Generate the final image to display
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_data = self.Memory_units[row, col]

                # Draw walls of the cells
                for i in range(10 * row + 2, 10 * row + 8):
                    self.image[i, 10 * col + 2:10 * col + 8] = 255
                if cell_data[0] == 1:
                    self.image[10 * row + 2:10 * row + 8, 10 * col] = 255
                    self.image[10 * row + 2:10 * row + 8, 10 * col + 1] = 255
                if cell_data[1] == 1:
                    self.image[10 * row, 10 * col + 2:10 * col + 8] = 255
                    self.image[10 * row + 1, 10 * col + 2:10 * col + 8] = 255
                if cell_data[2] == 1:
                    self.image[10 * row + 2:10 * row + 8, 10 * col + 9] = 255
                    self.image[10 * row + 2:10 * row + 8, 10 * col + 8] = 255
                if cell_data[3] == 1:
                    self.image[10 * row + 9, 10 * col + 2:10 * col + 8] = 255
                    self.image[10 * row + 8, 10 * col + 2:10 * col + 8] = 255

    def Prim_MazeGenerate(self):
        while self.history:
            r, c = random.choice(self.history)
            self.Memory_units[r, c, 4] = 1
            self.history.remove((r, c))
            check = []
            if c > 0:
                if self.Memory_units[r, c - 1, 4] == 1:
                    check.append('L')
                elif self.Memory_units[r, c - 1, 4] == 0:
                    self.history.append((r, c - 1))
                    self.Memory_units[r, c - 1, 4] = 2
            if r > 0:
                if self.Memory_units[r - 1, c, 4] == 1:
                    check.append('U')
                elif self.Memory_units[r - 1, c, 4] == 0:
                    self.history.append((r - 1, c))
                    self.Memory_units[r - 1, c, 4] = 2
            if c < self.end_col:
                if self.Memory_units[r, c + 1, 4] == 1:
                    check.append('R')
                elif self.Memory_units[r, c + 1, 4] == 0:
                    self.history.append((r, c + 1))
                    self.Memory_units[r, c + 1, 4] = 2
            if r < self.end_row:
                if self.Memory_units[r + 1, c, 4] == 1:
                    check.append('D')
                elif self.Memory_units[r + 1, c, 4] == 0:
                    self.history.append((r + 1, c))
                    self.Memory_units[r + 1, c, 4] = 2

            # select one of these edges at random.
            if len(check):
                move_direction = random.choice(check)
                if move_direction == 'L':
                    self.Memory_units[r, c, 0] = 1
                    c = c - 1
                    self.Memory_units[r, c, 2] = 1
                if move_direction == 'U':
                    self.Memory_units[r, c, 1] = 1
                    r = r - 1
                    self.Memory_units[r, c, 3] = 1
                if move_direction == 'R':
                    self.Memory_units[r, c, 2] = 1
                    c = c + 1
                    self.Memory_units[r, c, 0] = 1
                if move_direction == 'D':
                    self.Memory_units[r, c, 3] = 1
                    r = r + 1
                    self.Memory_units[r, c, 1] = 1

        # Open the walls at the start and finish
        self.Memory_units[0, 0, 0] = 1
        self.Memory_units[self.end_row, self.end_col, 2] = 1

        # Generate the image for display
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                cell_data = self.Memory_units[row, col]
                for i in range(10 * row + 2, 10 * row + 8):
                    self.image[i, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[0] == 1:
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col] = 255
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 255
                if cell_data[1] == 1:
                    self.image[10 * row, range(10 * col + 2, 10 * col + 8)] = 255
                    self.image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[2] == 1:
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 255
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 255
                if cell_data[3] == 1:
                    self.image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 255
                    self.image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 255


    def Show_Maze(self):
        plt.imshow(self.image, cmap=cm.Greys_r, interpolation='none')
        plt.show()