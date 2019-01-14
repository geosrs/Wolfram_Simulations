import numpy as np
import random
from Seeds import Seeds
from Kernel import Kernel

#this class handles the logic of swapping and modifying cells/rows
#on the 2D arrays for which these simulations exist
class Grid:
    round_value = 3
    wrap_around = False

    #sets all parameters for a grid
    def __init__(self, X, Y, max_cell_value, seed, seed_type, shift, kernel):
        self.row_length = X# + int(neighbors / 2) # possible no wrap around offset
        self.grid_height = Y
        self.max_cell_value = max_cell_value
        self.data = []
        self.seed = seed
        self.shift = shift
        self.seed_type = seed_type
        self.kernel = kernel
        self.neighbors = kernel.linear_kernel_length #redundant but still necessary
        self.linear_kernel_length = kernel.linear_kernel_length
        self.kernel_groups = self.Generate_Neighbor_Groups()


    #fills the grid with zeros
    def Zero_Grid(self):
        color = 0
        for i in range(self.grid_height):
            row = []
            for j in range(self.row_length):
                row.append(color)
            self.data.append(row)

    # randomize a given row
    def Randomize_Row(self, row_index):
        row = []
        for i in range(self.row_length):
            row.append(random.randint(0, self.max_cell_value - 1))
        self.data[row_index] = row

    # swap a given row with an inputted row
    def Replace_Row(self, row_index, row):
        self.data[row_index] = row

    # adds a row
    def Push_Row(self, row):
        data = []
        data.append(row)
        for i in range(0, self.grid_height):
            data.append(self.data[i])
        self.data = data

    # generates a new row given the parameters of the simulation
    # works for all types of kernels
    def Generate_Row_All_Kernels(self):
        new_row = []
        check_rows = [self.data[x] for x in range(self.kernel.start_rows_needed)]
        for cell_index in range(self.row_length):
            check_cell_group = []
            for kernel_index in range(self.kernel.linear_kernel_length):
                x_offset = self.kernel.ordered_pair_kernel[kernel_index][0]
                y_offset = self.kernel.ordered_pair_kernel[kernel_index][1]
                x_index = (x_offset + cell_index + self.shift) % self.row_length
                y_index = (y_offset)
                if x_index < 0: #wrap around if negative
                    x_index = self.row_length + x_index
                check_cell_group.append(check_rows[y_index][x_index])
            if self.seed_type == 1:
                new_row.append(int(self.Apply_Rule(check_cell_group)))
            elif self.seed_type == 2: # totalistic
                window_sum = 0
                for i in range(self.kernel.linear_kernel_length):
                    window_sum += check_cell_group[i]
                new_row.append(int(self.Apply_Rule(float(window_sum) / self.kernel.linear_kernel_length)))
        return new_row

    # called from Generate_Row_All_Kernels
    # takes a group of cells, looks up value using simulations rule
    def Apply_Rule(self, cell_group):
        if self.seed_type == 1: #checking group cell combination
            sequence = ''
            for j in range(len(cell_group)):
                sequence += str(int(cell_group[j]))
            for i in range(len(self.seed)):
                if sequence == self.kernel_groups[i]:
                    return self.seed[i]

        elif self.seed_type == 2: #checking average group cell value
            for i in range(len(self.seed)):
                #print(i)
                if round(cell_group,Grid.round_value) == self.kernel_groups[i]:
                    return self.seed[i]

        print('\nLoaded Seed(s) is not long enough given the base, kernel, and type of simulation.')
        quit()

    # generates all combinations of a size-N group of cells
    # generates elementary and totalistic combinations
    def Generate_Neighbor_Groups(self):
        list = []
        if self.seed_type == 1:
            s = Seeds()
            s.Config(self.seed_type,self.max_cell_value,self.linear_kernel_length)
            group = s.Generate_Seed_Range(0, (self.max_cell_value ** self.linear_kernel_length), self.linear_kernel_length) #only send parameter in this case
            for i in range(len(group)-1, -1 , -1):
                list.append( "".join(str(e) for e in group[i]))
        elif self.seed_type == 2:

            for i in range(len(self.seed) - 1,-1,-1):
                list.append(round((float(i) / self.linear_kernel_length), Grid.round_value))
        self.seed_length = len(list)
        return list
