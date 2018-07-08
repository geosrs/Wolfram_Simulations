
from Driver import Driver
from Seeds import Seeds
from Simulation import Simulation
from DB_Control import DB_Control
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from Seeds import Seeds
import time
import random
class Animation_Driver(Driver):

    def __init__(self, rule_type, base, kernel, seed, width, height):
        print('New Simulation:\t')
        Driver.__init__(self, width, height, rule_type, base, kernel, seed)
        self.shift = 0
        self.seedControl = Seeds(rule_type,kernel,base)
        self.save = True
        if seed == 0: # no default seed picked
            self.seed = self.seedControl.Generate_Random_Seed()
        else:
            self.seed = seed

        self.dec_seed = self.seedControl.Convert(self.base,self.seed)
        print('Seed: ' + ''.join(map(str,self.seed)) + '\tDecimal: ' + str(self.dec_seed))
        print('Seed Length: ' + str(len(self.seed)))
        error = self.Conflicting_Parameters()
        if error == True:
            quit()


    def Init_Simulation(self,start_type,steps, start_groups = 1, start_ratio = .5):
        #print('Initializing Simulation...')
        self.start_type = start_type
        self.steps = steps
        self.start_groups = start_groups
        self.start_ratio = start_ratio
        self.sim = Simulation(self.rule_type, self.base,self.steps, self.width,self.height, self.kernel)
        self.sim.Set_Seed(self.seed)
        self.sim.Set_Initial_Condition(self.start_type,self.start_groups, self.start_ratio)
        self.sim.Set_Animation()

    def Init_Colormaps(self, custom_cmap = 'chet'):
        if custom_cmap != 'chet':
            self.cmaps = [custom_cmap]
        else:
            self.Load_Cmaps()
        self.sim.Set_Cmaps(self.cmaps)

    def Run_Simulation(self):
        print('Running Simulation...')
        start_time = time.time()
        refresh_time = time.time()
        #sim.Setup_Subplots(subplot_count, orientation, False ,cycle_colormaps,cmaps)
        for i in range(self.steps):
            self.sim.Next_Step()
            if i % 100 == 0:
                print('Step Progress:\t' + str(i) + '\tElapsed Time:\t' + str(round(time.time() - start_time,1)) + ' s')
                refresh_time = time.time()



    def Display_Animation(self):
        self.fig = plt.gcf()
        self.ax = plt.gca()
        def update_grid():
            self.f_index += 1
            yield self.frames[self.f_index]
        def update_plot(x):
            #fig.text(0.5,0.9,x)
            self.f_index += 1
            chet = plt.pcolormesh(self.frames[self.f_index], cmap = self.cmaps[0])
            #plt.close()
            return [chet]

        #fig.canvas.mpl_connect('key_press_event', on_press)
        self.frames = self.sim.Get_Frames()
        self.f_index = 0
        self.ax.set_aspect('equal')
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        anim = ani.FuncAnimation(self.fig, update_plot,blit = True, frames=self.steps,
                                 interval=50, repeat=False)
        plt.show()



    def Conflicting_Parameters(self):
        if self.rule_type == 1:
            req_seed_len = self.base ** self.kernel
        elif self.rule_type == 2:
            req_seed_len = self.kernel*(self.base - 1) + 1
        if len(self.seed) != req_seed_len:
            print('Seed Incorrect. Length required: ' + str(req_seed_len))
            return True
