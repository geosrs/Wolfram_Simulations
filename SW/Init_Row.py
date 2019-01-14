import random
import math
class Init_Row:

    def __init__(self,width,base):
        self.width = width
        self.base = base
        self.group_ratio = width / 2
        self.g1_length = 4
        self.g2_length = 2

    #creates a start row give inputted conditions
    def Create_Row(self, type, sub_type, gap = 1, groups = 1):
        row = []
        if type == 1: #non groups simple init Rows_Above
            if sub_type == 1: #randomized
                for i in range(self.width):
                    row.append(random.randint(0,self.base - 1))
            elif sub_type == 2: #steps up with gap
                cell = 0
                while len(row) != self.width:
                    row.append(cell % (self.base))
                    if cell % (self.base) == self.base - 1:
                        for j in range(gap):
                            row.append(0)
                    cell += 1

            elif sub_type == 3: #steps down with gap
                cell = self.width
                while cell != 0:
                    row.append(cell % (self.base))
                    cell -= 1
                    if cell == 0:
                        return row
                    if cell % (self.base) == 0:
                        for j in range(gap):
                            row.append(0)
                            cell -= 1
                            if cell == 0:
                                return row

        elif type == 2: #Groups
            if sub_type == 1: #even group gaps based on group count
                row = [0 for x in range(self.width)]
                gap = self.width / (groups + 1)
                for i in range(gap / 2,self.width - (gap / 2)):
                    if i % (gap) == 0:
                        row[i] = self.base - 1
                for i in range(len(row)):
                    if row[i] == self.base - 1:
                        for offset in range(1,self.base - 1):
                            row[i - offset] = self.base - 1 - offset
                            row[i + offset] = self.base - 1 - offset

            elif sub_type == 2: #random group gaps based on group count
                row = []
                group = []
                gaps = []
                edge_gaps = []
                remaining_blocks = 0
                reserved_blocks = 0
                group_width       = (self.base * 2) - 3
                group_count       = groups
                reserved_blocks  += (group_count * group_width)
                remaining_blocks += int(self.width - reserved_blocks)
                initial_remaining_blocks = remaining_blocks
                gap_count = group_count - 1
                for i in range(1,self.base): #create group
                    group.append(i)
                for i in range(self.base - 2, 0, -1):
                    group.append(i)
                #assemble gaps
                edge_gaps.append(1) #left
                edge_gaps.append(1) #right
                remaining_blocks -= 2
                for i in range(gap_count + 2): #added plus 2 for edges
                    gaps.append(1) #all gaps start with one
                    remaining_blocks -= 1
                #jump around between random gaps, increase value randomly
                while(remaining_blocks > 0):
                    gap_index = random.randint(0,len(gaps) - 1)
                    if gaps[gap_index] < math.ceil(initial_remaining_blocks / 2):
                        add = random.randint(0,self.group_ratio)
                        if remaining_blocks - add <= 0:
                            gaps[gap_index] += remaining_blocks
                            remaining_blocks = 0
                        else:
                            gaps[gap_index] += add
                            remaining_blocks -= add
                row.append(0)
                for i in range(gaps.pop()):
                    row.append(0)
                for i in range(gap_count + group_count):
                    if i % 2 == 0: # group
                        for i in range(len(group)):
                            row.append(group[i])
                    else:
                        for i in range(gaps.pop()):
                            row.append(0)
                for i in range(gaps.pop()):
                    row.append(0)
                row.append(0)

        return row #return for all init rows

   