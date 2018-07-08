from Driver import Driver
from Seeds import Seeds
from Simulation import Simulation
from DB_Control import DB_Control
import matplotlib.pyplot as plt
from Seeds import Seeds
import time
import random
import os
import datetime
class Group_Driver(Driver):



    #start of new
    def __init__(self, rule_type,base,kernel,width,height, steps):
        Driver.__init__(self, width, height, rule_type, base, kernel)
        self.steps = steps #I01
        print('New Seed Group')

    def Init_Simulation_Group(self,iterations, ordered,start_type, start_groups = 1, start_ratio = .5):
        self.sim = Simulation(self.rule_type, self.base,self.steps, self.width, self.height, self.kernel)
        self.iterations = iterations
        self.ordered = ordered
        self.start_type = start_type
        self.start_groups = start_groups
        self.start_ratio = start_ratio
        self.seedControl = Seeds(self.rule_type,self.kernel,self.base)
        if ordered:
            start_seed = self.seedControl.Generate_Random_Seed()
            #start and end seed must be in decimal

            self.seedGroup = self.seedControl.Generate_Seed_Range(int(self.seedControl.Convert(self.base,start_seed)),
                                                                  int(self.seedControl.Convert(self.base,str(int(start_seed))))  + iterations,
                                                                  self.seedControl.seed_length)
        else:
            self.seedGroup = self.seedControl.Generate_Random_Seeds(iterations)
        self.Setup_Group_Save()

    def Init_Colormaps(self, custom_cmaps = False):
        if not custom_cmaps:
            self.Load_Cmaps()
        print(self.cmaps)
        self.sim.Set_Cmaps(self.cmaps)

    def Run_Simulation_Group(self):
        start_time = time.time()

        for s in range(self.iterations):
            self.dec_seed = self.seedControl.Convert(self.base,self.seedGroup[s])
            self.sim.Set_Seed(self.seedGroup[s]) #also creates new grid and zeros it
            self.sim.Set_Initial_Condition(self.start_type,self.start_groups, self.start_ratio)
            for r in range(self.steps):
                self.sim.Next_Step()

            path = self.Gen_Sim_Path(s)
            self.seed_log_file.write(''.join(map(str,self.seedGroup[s])) + '\n')
            self.sim.Save_Current_Figure(path, self.dec_seed)
            #elapsed = datetime.timedelta(seconds = int(time.time() - start_time))
            elapsed_sec = int(time.time() - start_time)
            perc_complete = ((s + 1) / self.iterations)
            print('\tGroup Progress: ' + str(s + 1) + ' of ' + str(self.iterations) +
                  '\tElapsed Time: ' + str(datetime.timedelta(seconds = elapsed_sec)) +
                  '\tTime Remaining: ' + str(datetime.timedelta(seconds = ((elapsed_sec + 1) * self.iterations) / (s + 1) - elapsed_sec)))

            self.sim.Reset_Plot()
        self.seed_log_file.close()


    def Setup_Group_Save(self):
        self.path = self.def_path
        self.group_folder =(str(self.rule_type) + '-' +
                            str(self.base) + '-' +
                            str(self.kernel) + '-' +
                            str(self.iterations))
        self.path += 'Plots\\'
        if self.ordered == True:
            self.path += 'OrderedGroup\\' #folder
        else:
            self.path += 'RandomGroup\\'
        self.path += self.group_folder
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def Gen_Sim_Path(self,index):
        self.seed_log_file = open(self.path + '\\' + 'seed_maps.txt', 'ab')

        path = self.path + '\\'
        path += (str(index) + '.png')

        #path += self.seedControl.Convert(self.base,self.seedGroup[index])
        #path += ('-' + ''.join(map(str,self.sim.seed)) + '.png')
        return path

    def Conflicting_Parameters(self):
        req_seed_len = self.kernel*(self.base + 1) + 1
        if len(self.seed) != req_seed_len:
            print('Seed Incorrect. Length required: ' + str(req_seed_len))
            return True
        return False
