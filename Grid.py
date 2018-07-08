import numpy as np
import random
from Seeds import Seeds
class Grid:
    round_value = 3
    wrap_around = False
    def __init__(self, X, Y, max_cell_value, seed, seed_type, shift, neighbors):
        self.row_length = X
        self.grid_height = Y
        self.max_cell_value = max_cell_value
        self.data = []
        self.seed = seed
        #print(self.seed)
        self.shift = shift
        self.seed_type = seed_type
        self.neighbors = neighbors
        self.neighborhoods = self.Generate_Neighbor_Groups()
        #print('Kernel Values: ' + ' '.join(map(str,self.neighborhoods)))
        #print('Kernel Values/ Seed Length: ' + str(len(self.neighborhoods)))

        #print(self.neighborhoods)


    def Zero_Grid(self):
        color = 0
        for i in range(self.grid_height):
            row = []

            for j in range(self.row_length):
                row.append(color)
            self.data.append(row)

    def Randomize_Row(self, row_index):
        row = []
        for i in range(self.row_length):
            row.append(random.randint(0, self.max_cell_value - 1))
        self.data[row_index] = row

    def Replace_Row(self, row_index, row):
        self.data[row_index] = row

    def Push_Row(self, row_index, row):
        data = []
        data.append(row)

        for i in range(0, self.grid_height):
            #print('row: '+ str(i + 1) + '\t' + ''.join(map(str,self.data[i - 1])))
            data.append(self.data[i])
        #data[0] = row
        self.data = data

    '''
    def Generate_Elementary_Row(self):
        new_row = []
        EXP = False
        check_row = self.data[0]
        for i in range(self.row_length):
            cell_group = []
            if EXP:
                #left justified rule
                cell_group.append(check_row[i])
                cell_group.append(check_row[(i + 1)% self.row_length])
                cell_group.append(check_row[(i + 2)% self.row_length])

            else:
                if  i == 0: # have to wrap around to other side
                    cell_group.append(check_row[self.row_length - 1])
                    cell_group.append(check_row[i])
                    cell_group.append(check_row[i + 1])
                else:
                    cell_group.append(check_row[i - 1])
                    cell_group.append(check_row[i])
                    cell_group.append(check_row[(i + 1) % self.row_length])
            new_row.append(self.Apply_Rule(cell_group))
        return new_row
    '''

    def Generate_Row_N_Neighbors(self):
        print_info = False
        new_row = []
        check_row = self.data[0]
        start_offset = (self.neighbors - 1) / 2
        for cell_index in range(self.row_length):
            cell_group = []
            for neighbor_index in range(self.neighbors):
                if (neighbor_index + cell_index) < (start_offset + self.shift): # wrap around case
                    complicated_index = (self.row_length - start_offset - self.shift) + (neighbor_index + cell_index)
                else:
                    complicated_index = ((neighbor_index + cell_index - self.shift) - start_offset) % self.row_length
                cell_group.append(check_row[complicated_index])

            if self.seed_type == 1:
                #send window group
                new_row.append(int(self.Apply_Rule(cell_group)))
            elif self.seed_type == 2: # totalistic
                window_sum = 0
                #print(cell_group)
                for i in range(self.neighbors):
                    window_sum += cell_group[i]
                #print(window_sum)
                new_row.append(int(self.Apply_Rule(float(window_sum) / self.neighbors)))
            #elif self.seed_type == 3:
        return new_row





    '''
    def Generate_Totalistic_Row(self):
        new_row = []

        #cycle through each cell in the top row
        for i in range(self.row_length):
            group_sum = 0
            check_row = self.data[0]
            if  i == 0: # have to wrap around to other side
                #if not Grid.wrap_around:
                group_sum += check_row[self.row_length - 1]
                group_sum += check_row[i]
                group_sum += check_row[i + 1]
            else:
                group_sum += (check_row[i - 1])
                group_sum += (check_row[i])
                #if i == self.row_length and not Grid.wrap_around:
                group_sum += (check_row[(i + 1) % self.row_length])
            new_row.append(self.Apply_Rule(float(group_sum) / self.max_cell_value))

        return new_row
    '''


    def Apply_Rule(self, cell_group):
        if self.seed_type == 1: #checking group cell combination
            #print(self.neighborhoods)
            sequence = ''
            ###print(self.neighborhoods)
            for j in range(len(cell_group)):
                sequence += str(int(cell_group[j]))
            #else:
            #    print(cell_group)
            #sequence = (str(int(cell_group[0])) + str(int(cell_group[1])) + str(int(cell_group[2])))
            for i in range(len(self.seed)):
                if sequence == self.neighborhoods[i]:
                    return self.seed[i]

        elif self.seed_type == 2: #checking average group cell value
            for i in range(len(self.seed)):
                #print(i)
                if round(cell_group,Grid.round_value) == self.neighborhoods[i]:
                    return self.seed[i]

                #else:
                    #print('chet:\t' + str(round(cell_group,Grid.round_value)))


        #print(round(cell_group,Grid.round_value))
        #print(cell_group)
        print('Seed too short')
        #return 0



    def Generate_Neighbor_Groups(self):
        list = []
        if self.seed_type == 1:
            s = Seeds(self.seed_type,self.neighbors,self.max_cell_value)
            #print('neighbors ' + str(self.neighbors))
            group = s.Generate_Seed_Range(0, (self.max_cell_value**self.neighbors),self.neighbors) #only send parameter in this case
            for i in range(len(group)-1, -1 , -1):
                list.append( "".join(str(e) for e in group[i]))
            #print(list)
        elif self.seed_type == 2:
            #for i in range((self.neighbors * 2) + 1):
            #for i in range(1 + (self.neighbors * (self.max_cell_value - 1))):
            for i in range(len(self.seed) - 1,-1,-1):
                list.append(round((float(i) / self.neighbors), Grid.round_value))
        self.seed_length = len(list)
        #print('Window Averages:\t' + str(list))
        #print('Required seed length:\t' + str(len(list)))
         #print(list)
        return list

'''
g = Grid(50,50,2,0,2,-1,5)
'''
