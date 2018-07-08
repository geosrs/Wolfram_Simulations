import random

class Init_Row:


    def __init__(self,type,width,base, groups, HL_ratio):
        self.type = type
        self.width = width
        self.base = base
        self.groups = groups
        self.HL_ratio = HL_ratio
        self.row = []

    def Create_Row(self):
        row = []
        if self.type == 1: # Randomize
            for i in range(self.width):
                row.append(random.randint(0,self.base - 1))
        elif self.type == 2: # distributed start blocks
            start_block = []
            for i in range(1, self.base):
                start_block.append(i)
            for i in range(self.base - 2, 0, -1):
                start_block.append(i)
            #print(start_block)

            indexes = []
            row = [(self.base - 1) if x % ((self.width / (self.groups + 1))) == 0 and x != 0 else 0 for x in range(0 , self.width)]
            for i in range(self.width):
                if row[i] == self.base - 1 and i != 0:
                    for j in range(len(start_block)):
                        row[i + j - (len(start_block) / 2)] = start_block[j]

            #for i in range(len(row)):
            #    row[i] = row[((len(row) / 2) + i) % len(row)]

            #print(row)

        elif self.type == 3: # even distribution of all colors, random order
            partitions = []
            for i in range(1,self.base):
                partitions.append(self.width / self.base * i)
            partitions.append(self.width)
            row = []
            partition_count = 0
            for i in range(self.width):
                if i > partitions[partition_count]:
                    partition_count += 1
                row.append(partition_count)
            random.shuffle(row)

        elif self.type == 4: # max to min ratio, no inbetween
            row = [0 if x < int(self.width * self.HL_ratio) else self.base - 1 for x in range(self.width)]
            random.shuffle(row)
        elif self.type == 5:
            start_block = []
            for i in range(1, self.base):
                start_block.append(i)
            for i in range(self.base - 2, 0, -1):
                start_block.append(i)
            #print(start_block)
            count = 0
            for i in range((self.width / 2) - self.base - 1, (self.width / 2) + self.base - 1):
                print((self.width / 2) - self.base)
                row[i] = start_block[count]
                count += 1
        elif self.type == 6: #only one in the middle
            row = [self.base - 1 if (x) % (self.width / (self.groups + 1)) == 0 and x != 0 and x != self.width - 1 else (0) for x in range(self.width)]


        return row


#chet = Init_Row(2,40,5,4)
#chet.Create_Row()

'''
self.init_index = init_index
#self.Print_Information()
if init_index == 1: #random row
    self.grid.Randomize_Row(self.step_count)
    return
elif init_index == 2: # several High in middle
    row = [ 0 if x == self.width / 2
              or x == (self.width / 2) + 1
              or x == (self.width / 2) - 1
              else self.max_cell_value - 1
              for x in range(self.width)]
elif init_index == 3: # evenly distribution of all colors

elif init_index == 4:# H:L ratio

elif init_index == 5: #even group
    row = [0] * self.width
    # single width

    #row = [0 if x % (self.width / (ticks + 1)) == 0 else (self.max_cell_value - 1) for x in range(self.width)]


    for x in range(0,self.width - 1):
        if x % (self.width / (ticks)) == 0 and x != 0 and x != self.width - 1:
            print(x)
            row[x] = 0
            #row[(x + 1) % self.width - 1] = 0
            #print('tick at ' + str(x))

        else:
            row[x] = self.max_cell_value - 1
            #row[(x + 1) % self.width - 1] = self.max_cell_value - 1
    box_width = 2


    #row = [0 if (x % (self.width / (ticks + 1)) == 0) else (self.max_cell_value - 1) for x in range(self.width)]

elif init_index == 6: #variable
    row = []
'''
