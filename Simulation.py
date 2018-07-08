from Grid import Grid
from IndexTracker import IndexTracker
from DB_Control import DB_Control
from Init_Row import Init_Row
from PIL import Image
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani
import mpl_toolkits.axes_grid1 as axes_grid1
import random
import matplotlib.gridspec as gridspec
import time
import os
#from PIL import Image

class Simulation:

    #new
    def __init__(self,seed_type, base, steps,width,height, kernel):

        #self.seed = seed
        self.seed_type = seed_type
        self.base = base
        self.steps = steps
        self.width = width
        self.height = height
        self.kernel = kernel
        self.shift = 0
        self.save_frames = False
        #self.grid = Grid(width, steps, base, seed, seed_type, self.shift, kernel)
        #self.grid.Zero_Grid()
        #self.height = steps #temporary

    def Reset_Sim(self):
        self.grid = Grid(width, steps, base, seed, seed_type, self.shift, kernel)

    def Set_Seed(self,seed):
        self.seed = seed
        self.frames = []
        print(self.height)
        self.grid = Grid(self.width, self.height, self.base, self.seed, self.seed_type, self.shift, self.kernel)
        self.grid.Zero_Grid()
        self.frames.append(self.grid.data)
    #new
    def Set_Initial_Condition(self, start_type, start_groups = 1, hl_disperse_ratio = .5):
        self.start_type = start_type
        self.hl_disperse_ratio = hl_disperse_ratio
        self.start_groups = start_groups
        self.step_count = 0
        self.row_creator = Init_Row(start_type, self.width, self.base, start_groups, hl_disperse_ratio)
        self.grid.Replace_Row(self.step_count, self.row_creator.Create_Row())


    def Set_Cmaps(self,cmaps):
        self.cmaps = cmaps


    def Set_Plotting(self):
        self.fig , self.ax = plt.subplots()


    def Set_Animation(self):
        self.save_frames = True
        self.ani_frames = []

    def Get_Frames(self):
        return self.ani_frames



    #unused, should be used
    def Print_Information(self):
        if self.seed_type == 1:
            print('New Elementary Simulation:\t' + str(self.width) + ' x ' + str(self.height))
        elif self.seed_type == 2:
            print('New Totaltarian Simulation:\t' + str(self.width) + ' x ' + str(self.height))
        elif self.seed_type == 3:
            print('New Experimental Simulation:\t' + str(self.width) + ' x ' + str(self.height))
        print('Seed:\t' + ''.join(map(str,self.seed)))
        print('Steps:\t' + str(self.steps))



    def Next_Step(self):
        row = self.grid.Generate_Row_N_Neighbors()
        self.grid.Push_Row(self.step_count, row)
        self.frames.append(self.grid.data)
        self.step_count += 1


        if self.save_frames:
            self.ani_frames.append(self.grid.data)


        subplots_on = False
        if subplots_on:
            if self.step_count % (self.steps / self.subplot_count) == 0:
                self.subplot_data.append(self.grid.data)

    #unused
    def Setup_Subplots(self, count, orientation, duplicate, cycle_colormaps, cmaps):
        self.subplot_count = count
        #self.subplot_orientation = orientation
        #self.subplot_duplicate = duplicate
        #self.cycle_colormaps = cycle_colormaps

        #print('Subplots:\t' + str(self.subplot_count) + '\t' + str(self.subplot_orientation))

    #unused
    def Enable_Logging(self, db):
        self.db = db

    #unused
    def Enable_Frame_Save(self,seed):

        self.db.Push_Grid(self.grid.data,self.seed)
        plt.clf()

    #unused
    def Reset_Plot(self):
        plt.clf()
        plt.cla()


    #could be used, is not used
    def Display_Starting_State(self):
        plt.xticks(np.arange(0,self.width + 1,self.width / 10))
        plt.yticks(np.arange(0,self.height + 1,self.height / 10))
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.imshow(self.frames[0], cmap = self.cmap)


    def Display_Current_Figure(self):
        print('Displaying Current Figure...')
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        cmap_index = random.randint(0,len(self.cmaps) - 1)
        plt.pcolor(self.frames[self.step_count], cmap = self.cmaps[cmap_index])
        plt.show()
        print('Current Figure Displayed.')

    def Add_Subplots(self,X,Y):
        axes = []
        fig = plt.figure(figsize=(X, Y))
        #if self.subplot_orientation == 'HOR':
            #fig = plt.figure(figsize = (1, subplots))
           # gs1 = gridspec.GridSpec(1, subplots)
        #elif self.subplot_orientation == 'VER':
        #    fig = plt.figure(figsize=(X,1))
            #fig = plt.figure(figsize = (subplots, 1))
            #gs1 = gridspec.GridSpec(subplots, 1)
        #gs1.update(wspace=.1, hspace=.1)
        start_time = time.time()
        print('Adding Subplots to Figure...')
        for i in range(X):
            #axes.append(fig.add_subplot(2,i+1,i+1))#gs1[i]))
            #ax = plt.subplot(gs1[i])
            #if self.subplot_duplicate:
            #    plt.pcolor(self.frames[self.step_count], cmap = self.cmap)
            #else:
            #if self.cycle_colormaps:
            #    #axes[i].imshow(self.subplot_data[i], cmap = self.cmaps[i % len(self.cmaps)])
            #    ax = fig.add_subplot(X,Y,i+1)
            #    ax.set_aspect('equal')
            #    plt.pcolor(self.subplot_data[i], cmap = self.cmaps[i % len(self.cmaps)])
                #plt.imshow(self.subplot_data[i], cmap = self.cmaps[i % len(self.cmaps)])
            #else:
            ax = fig.add_subplot(X,Y,i+1)
            ax.set_aspect('equal')
            plt.pcolor(self.subplot_data[i], cmap = self.cmaps[0])
            ax.set_axis_off()
            print('Added Subplot #' + str(i + 1) + '\tElapsed Time:\t' +str(round(time.time() - start_time,1)) + ' s')
        plt.show()




    def Save_Current_Figure(self,path,decimal_seed):#,index):#,cmap_str):
        resize_factor = 1
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        cmap_index = 0
        cmap_index = random.randint(0,len(self.cmaps) - 1)
        file_name = ''.join(map(str,self.seed)) + '\n' + decimal_seed


        a = np.flip(np.array(self.frames[self.step_count]),0)
        a *= 255 / a.max()
        im = Image.fromarray(np.uint8(a))
        print(a)

        im = im.resize((resize_factor * self.width,resize_factor * self.height), Image.NEAREST)
        #print(a)
        im.save(path,"BMP",quality=100)
        ts = time.time()

        #old Matplotlib save method
        #plt.pcolor(self.frames[self.step_count], cmap = self.cmaps[cmap_index], rasterized=True)
        #plt.savefig(path, dpi = 1000, bbox_inches='tight')
        plt.clf()
