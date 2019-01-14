#from Driver import Driver
from Seeds import Seeds
from Simulation import Simulation
import matplotlib.pyplot as plt
from Seeds import Seeds
from Kernel import Kernel
#import XlsxWriter
import time
import random
import os
import re
import datetime

#Improved/Decoupled
class Stitched_Driver():

    # loads fundemental information for group of stitched simulations
    def __init__(self, simulation_count, segment_count, width, segment_heights):
        self.stitched_simulation_count = simulation_count
        self.segment_count = segment_count
        self.width = width
        self.loaded_segment_heights = segment_heights
        self.segment_steps = segment_heights


    # loads information regarding seeds for each simulation
    # handles all types of options for first seed and remaining seeds of each image
    def Setup_Seeds(self, seed_group, rule_type, base, kernel, first_seeds, remaining_seeds):
        self.seed_group             = seed_group
        self.rule_type              = rule_type
        self.base                   = base
        self.kernel                 = Kernel(kernel)
        self.first_seed_option      = first_seeds
        self.remaining_seed_option  = remaining_seeds
        self.all_seeds = []
        self.seedControl = Seeds()
        self.seedControl.Config(self.rule_type, self.base, self.kernel.linear_kernel_length)
        for S in range(self.stitched_simulation_count):
            current_stitch_seeds = []
            if self.first_seed_option == 'random':
                if self.remaining_seed_option == 'random':
                    current_stitch_seeds = self.seedControl.Generate_Random_Seeds(self.segment_count)

                elif self.remaining_seed_option == 'ordered':
                    random_start_seed = self.seedControl.Generate_Random_Seed()
                    lower_bound = int(self.seedControl.Convert(self.base, random_start_seed))                       #convert lower bound to base 10
                    upper_bound = int(self.seedControl.Convert(self.base, random_start_seed))  + self.segment_count #convert seed range upper bound to base 10
                    current_stitch_seeds = self.seedControl.Generate_Seed_Range(lower_bound, upper_bound, self.seedControl.seed_length)
                else:
                    print('Seed options incorrect')
                    quit()

            elif self.first_seed_option == 'loaded':
                if self.remaining_seed_option == 'random loaded':
                    if len(self.seed_group) == 0:
                        print('\nNo seeds loaded.')
                        quit()
                    current_stitch_seeds = [self.seed_group[random.randint(0,len(self.seed_group) - 1)] for x in range(self.segment_count)]

                elif self.remaining_seed_option == 'cyclic loaded': #always starts with first seed
                    current_stitch_seeds = [self.seed_group[x % len(self.seed_group)] for x in range(self.segment_count)]

                elif self.remaining_seed_option == 'random': #remaining seeds are completely random, not in loaded group
                    loaded_start_seeds = self.seed_group[S % len(self.seed_group)]# for x in range(len(self.seed_group))]
                    random_remaining_group = self.seedControl.Generate_Random_Seeds(self.segment_count - len(loaded_start_seeds))
                    current_stitch_seeds = loaded_start_seeds + random_remaining_group

                elif self.remaining_seed_option == 'ordered':
                    print('ordered remaining seeds is not implemented at this time')
                    quit()
                else:
                    print('Seed options incorrect')
                    quit()
            else:
                print('Seed options incorrect')
                quit()

            self.all_seeds.append(current_stitch_seeds)


    # sets up folder structure for image groups
    # creates seed log
    def Setup_Saving(self):
        #create simulation data container
        self.Setup_Data_Container()
        #create group folder
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        desktop += '\\WolframSimulations'
        if not os.path.exists(desktop):
            os.makedirs(desktop)
        self.default_save_path = desktop
        self.relative_save_path = self.default_save_path
        print('Image Save Path:')
        if self.stitched_simulation_count > 1:
            self.latest_dir_index = 0
            self.relative_save_path += '\\Groups'
            dirs = []
            for root, d, files in os.walk(self.relative_save_path, topdown = False):
                dirs = d
            if len(dirs) > 0:
                self.latest_dir_index = max([int(dirs[x][:(dirs[x].find('_'))]) for x in range(len(dirs))])
            folder = (str(self.latest_dir_index + 1) + '_SC' + self.display_info[0] + '-SG_' +
                                                         self.display_info[1] + '-RT_' +
                                                         self.display_info[2] + '-B_' +
                                                         self.display_info[3])
            self.relative_save_path += '\\' + folder

            if not os.path.exists(self.relative_save_path):
                os.makedirs(self.relative_save_path)
            #save seed log to folder
            self.seed_log_file = open(self.relative_save_path + '\\seed_maps.txt', 'a')
            for i in range(self.stitched_simulation_count):

                self.seed_log_file.write('Stitch: ' + str(i + 1) + '\n')
                for j in range(self.segment_count):
                    self.seed_log_file.write(''.join(map(str,self.all_seeds[i][j])) + '\n')
            self.seed_log_file.close()
            
            print(self.relative_save_path)

        else:
            self.latest_file_index = 0
            self.relative_save_path += '\\Singles'
            print(self.relative_save_path)            
            if not os.path.exists(self.relative_save_path):
                os.makedirs(self.relative_save_path)
            file_names = []
            for root, d, files in os.walk(self.relative_save_path, topdown = False):
                file_names = files
            if len(file_names) > 0:
                self.latest_file_index = max([int(file_names[x][:(file_names[x].find('_'))]) for x in range(len(file_names)) ])
            self.latest_file_index += 1

    # sets up all initial rows for each simulation chain in each image
    def Setup_Initial_Conditions(self,start_type, start_sub_type, start_gap, start_groups, heights_setting):
        self.start_type     = start_type
        self.start_sub_type = start_sub_type
        self.start_gap      = start_gap
        self.start_groups   = start_groups
        self.all_heights = []
        self.heights_setting = heights_setting
        if heights_setting == 'cyclic':
            constant_height_order = [self.loaded_segment_heights[x % len(self.loaded_segment_heights)] for x in range(self.segment_count)]
            self.all_heights = [constant_height_order for x in range(self.stitched_simulation_count)]
        elif heights_setting == 'random loaded':
            for i in range(self.stitched_simulation_count):
                random_loaded_height_order = [self.loaded_segment_heights[random.randint(0,len(self.loaded_segment_heights) - 1)] for x in range(self.segment_count)]
                self.all_heights.append(random_loaded_height_order)
        elif heights_setting == 'random':
            #upper bounds are first and second heights entered
            try:
                for i in range(self.stitched_simulation_count):
                    random_height_order = [random.randint(self.loaded_segment_heights[0],self.loaded_segment_heights[1]) for x in range(self.segment_count)]
                    self.all_heights.append(random_height_order)
            except:
                print('Please input upper and lower bounds for heights.')
                quit()

        else:
            print('Incorrect heights settings')
            quit()
        self.Print_Info()


    # runs simulations for each image, saves one at a time to prevent memory overload
    # runs each segment as individual simulation, calls 'Stitch_Simulations' to combine and save.
    def Run_Stitches(self, save_size, duplicate_saves, ):
        self.save_size = save_size
        for i in range(self.stitched_simulation_count):

            current_stitch_sims = []
            current_stitch_sims.append(Simulation(self.rule_type, self.base, self.all_heights[i][0], self.width, self.all_heights[i][0], self.kernel))
            current_stitch_sims[0].Set_Seed(self.all_seeds[i][0])
            current_stitch_sims[0].Set_Initial_Condition(self.start_type, self.start_sub_type, self.start_gap, self.start_groups)
            for j in range(current_stitch_sims[0].height):# - self.kernel.start_rows_needed):
                current_stitch_sims[0].Next_Step()

            #remaining simulations of stitch
            for j in range(1,self.segment_count):
                previous_end_rows = current_stitch_sims[j - 1].Get_Rows(1, self.kernel.start_rows_needed)
                current_stitch_sims.append(Simulation(self.rule_type, self.base, self.all_heights[i][j], self.width, self.all_heights[i][j], self.kernel))
                #should not need to send initial conditions
                current_stitch_sims[j].Set_Seed(self.all_seeds[i][j])
                current_stitch_sims[j].Insert_Rows_Top(previous_end_rows)
                for k in range(current_stitch_sims[j].height):
                    current_stitch_sims[j].Next_Step()

            self.Stitch_Simulations(i,current_stitch_sims,duplicate_saves, )
            print('Group Completion: ' + str(float(i + 1) / self.stitched_simulation_count * 100 ) + '%')

    
    # combines simulations into one large stitiched simulation
    def Stitch_Simulations(self,stitch_index, current_stitch, duplicate_saves, ):
        total_height = 0
        grids = []
        #getting all grids for single stitch
        for j in range(self.segment_count):
            total_height += current_stitch[j].height
            grids.append(current_stitch[j].grid.data)
        combined_rows = []
        for j in range(len(grids)): #current simulation within one stitch
            for k in range(len(grids[j])): #row within simulation
                combined_rows.append(grids[j][current_stitch[j].height - k])
        combined_simulation = Simulation(self.rule_type, self.base, total_height, self.width, total_height, self.kernel)
        combined_simulation.Set_Seed(self.all_seeds[0][0]) #dummy seed
        for i in range(total_height + 1):
            combined_simulation.Next_Step(combined_rows[i])
        combined_simulation.Set_Cmaps(self.cmaps)
        result_name = (str(stitch_index + 1)  + '_K' + self.display_info[4] +
                                                '_Dim' + str(self.width) +
                                                '_x_' + str(total_height))
        if self.stitched_simulation_count == 1:
            combined_simulation.Display_Current_Figure()
        combined_simulation.Save_Current_Figure(self.relative_save_path + '\\' + result_name, self.save_size, duplicate_saves)


    #private
    # creates container to hold relevant console print information
    # and information used when saving groups of images
    def Setup_Data_Container(self):
        self.display_info_labels = []
        self.display_info = []
        self.display_info_labels.append('Stitch Count:\t')
        self.display_info_labels.append('Segment Count:\t')
        self.display_info_labels.append('Rule Type:\t')
        self.display_info_labels.append('Number Base:\t')
        self.display_info_labels.append('Kernel:\t')
        self.display_info_labels.append('Width:\t')
        self.display_info_labels.append('Height:\t')
        self.display_info.append(str(self.stitched_simulation_count))
        self.display_info.append(str(self.segment_count))
        self.display_info.append(str(self.rule_type))
        self.display_info.append(str(self.base))
        self.display_info.append(''.join(map(str,self.kernel.linear_kernel)))

    #prints all group info at beginning of run
    def Print_Info(self):
        for i in range(len(self.display_info)):
            print(self.display_info_labels[i] + str(self.display_info[i]))
        for i in range(len(self.all_seeds)):
            print('\nStitch ' + str(i + 1) + ':')

            print('\tDimensions:\t' + str(self.width) + ' x ' + str(self.all_heights[i]))
            for j in range(len(self.all_seeds[i])):
                print('\tSeed ' + str(j + 1) + ':\t' + str(''.join(map(str,self.all_seeds[i][j]))))

    #loads cmaps from Main
    def Load_Cmaps(self, cmaps):
        self.cmaps = cmaps