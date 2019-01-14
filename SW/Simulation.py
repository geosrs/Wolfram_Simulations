from Grid import Grid
from Init_Row import Init_Row
from PIL import Image
from matplotlib import cm
import numpy as np
import matplotlib.animation as ani
import random
import math
import os
#from PIL import Image




class Simulation:

    #loads fundemental information for simulation
    def __init__(self,seed_type=0, base=0, steps=0,width=0,height=0, kernel=0):
        self.seed_type = seed_type
        self.base = base
        self.steps = steps
        self.width = width
        self.height = height
        self.kernel = kernel
        self.shift = 0
        self.step_count = 0
        self.save_frames = False


    def Set_Seed(self,seed):
        self.seed = seed
        self.frames = []
        self.grid = Grid(self.width, self.height, self.base, self.seed, self.seed_type, self.shift, self.kernel)
        self.grid.Zero_Grid()
        self.frames.append(self.grid.data)
    #new

    # loads start conditions for each simulation
    def Set_Initial_Condition(self, start_type, start_sub_type, gap = 1, groups = 1, duplicate_start_rows = True):
        self.start_type = start_type
        self.start_sub_type = start_sub_type
        self.gap = gap
        self.start_groups = groups
        self.row_creator = Init_Row(self.width, self.base)
        start_row = self.row_creator.Create_Row(start_type, start_sub_type, gap, groups)
        for i in range(self.kernel.start_rows_needed):
            self.grid.Replace_Row(i, start_row)



    # replaces rows at the top of a simulation
    # used for transitioning between simulations
    def Insert_Rows_Top(self, rows):
        for i in range(len(rows)):
            self.grid.Replace_Row(self.step_count, rows[i])


    # returns rows from either the front end or back end of a simulation
    # used for transitioning between simulations
    def Get_Rows(self, front_or_back, count):
        rows = []
        for i in range(count):
            if front_or_back == 1:
                rows.append(self.grid.data[i])
            elif front_or_back == 2:
                rows.append(self.grid.data[self.height - i])
        return rows


    #loads cmaps
    def Set_Cmaps(self,cmaps):
        self.cmaps = cmaps

    #creates another row for the given simulation
    def Next_Step(self, custom_row = []):
        if len(custom_row ) != 0:
            row = custom_row
        else:
            row = self.grid.Generate_Row_All_Kernels()
        self.grid.Push_Row( row)
        self.frames.append(self.grid.data)
        self.step_count += 1

    #displays current image
    #only used when single images are created
    def Display_Current_Figure(self):
        print('Displaying Current Figure...')
        max_image_size = 1024 * 1024 * 40 #  10485760bytes  10mb pictures
        resize_factor = max_image_size / (self.width * self.height)
        formatted_data = np.flip(np.array(self.frames[self.step_count]),0)
        formatted_data *= 255 / formatted_data.max()
        cmap_list = self.cmaps['Favorites']
        cmap = cm.get_cmap(cmap_list[random.randint(0,len(cmap_list)) - 1])
        im = Image.fromarray(np.uint8(cmap(formatted_data) * 255))
        #scales image so file size is constant
        scaled_img_x = int(math.sqrt(max_image_size * self.width / self.height))# - self.width)
        scaled_img_y = int(math.sqrt(max_image_size * self.height / self.width))# - self.height)
        im = im.resize((scaled_img_x, scaled_img_y), Image.NEAREST)
        im.show()


    #saves current image, also picks cmap based on selection
    def Save_Current_Figure(self,path, mb, save_duplicates):#,index):#,cmap_str):
        mbI = int(mb)
        max_image_size = 1024 * 1024 * mbI / 4 #  10485760bytes  10mb pictures
        resize_factor = max_image_size / (self.width * self.height)
        cmap_index = random.randint(0,len(self.cmaps) - 1)
        cmap_list = self.cmaps[self.cmaps['Selection']]
        if save_duplicates:
            saves = len(self.cmaps['Austere'])
        else:
            saves = 1
        for i in range(saves):
            if save_duplicates:
                cmap_index = i#@ % len(self.cmaps['Favorites'])
            else:
                cmap_index = random.randint(0,len(cmap_list) - 1)
            cmap = cm.get_cmap(cmap_list[cmap_index])
            formatted_data = np.flip(np.array(self.frames[self.step_count]),0)
            formatted_data = formatted_data * (255 / formatted_data.max())
            im = Image.fromarray(np.uint8(cmap(formatted_data) * 255))
            #scales image so file size is constant
            scaled_img_x = int(math.sqrt(max_image_size * self.width / self.height))# - self.width)
            scaled_img_y = int(math.sqrt(max_image_size * self.height / self.width))# - self.height)
            im = im.resize((scaled_img_x, scaled_img_y), Image.NEAREST)
            im.save(path + '_' + cmap.name + '.bmp',"BMP",quality=100)
