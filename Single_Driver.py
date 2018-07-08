from Driver import Driver
from Seeds import Seeds
from Simulation import Simulation
from DB_Control import DB_Control
import matplotlib.pyplot as plt
from Seeds import Seeds
import time
import random
class Single_Driver(Driver):

    def __init__(self, rule_type, base, kernel, seed, width, height):
        print('New Simulation:\t')
        Driver.__init__(self, width, height, rule_type, base, kernel, seed)
        #self.kernel = kernel
        #self.steps = steps #I01
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

    def Init_Simulation(self,start_type,steps ,start_groups = 1, start_ratio = .5):
        #print('Initializing Simulation...')
        self.start_type = start_type
        self.steps = steps
        self.start_groups = start_groups
        self.start_ratio = start_ratio
        self.sim = Simulation(self.rule_type, self.base,self.steps, self.width, self.height, self.kernel)
        self.sim.Set_Seed(self.seed)
        self.sim.Set_Initial_Condition(self.start_type,self.start_groups, self.start_ratio)

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
        print('steps: ' + str(self.steps))
        for i in range(self.steps):
            self.sim.Next_Step()
            if i % 100 == 0:
                print('Step Progress:\t' + str(i) + '\tElapsed Time:\t' + str(round(time.time() - start_time,1)) + ' s')
                refresh_time = time.time()

    def Save(self):

        path = self.def_path + 'plots\\'
        self.Setup_Save(path)
        print('Saving . . .')
        self.sim.Save_Current_Figure(self.path, self.dec_seed)

    def Display(self):
        self.sim.Set_Plotting()
        self.sim.Display_Current_Figure()


##################local methods#####################


    def Setup_Save(self,path):

        self.path = path

        self.path += 'Single\\' #folder
        self.path += (str(self.rule_type) + '-')
        self.path += (self.dec_seed + '-')
        self.path += (str(self.base) + '-')
        self.path += (str(self.kernel) + '-')
        #self.path += (self.cmaps[0])
        self.path += (str(self.width) + 'x')
        self.path += (str(self.height) + '-R_')
        self.path += str(random.randint(0,1000))
        self.path += '.bmp'

    def Conflicting_Parameters(self):
        if self.rule_type == 1:
            req_seed_len = self.base ** self.kernel
        elif self.rule_type == 2:
            req_seed_len = self.kernel*(self.base - 1) + 1
        if len(self.seed) != req_seed_len:
            print('Seed Incorrect. Length required: ' + str(req_seed_len))
            return True
