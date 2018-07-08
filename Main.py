
from Single_Driver import Single_Driver
from Group_Driver import Group_Driver
from Animation_Driver import Animation_Driver
type = 1
#Start Types
# 1 Random
# 2 Groups (not working 100%)
# 3 Even of each color
# 4 High-Low Ratio
# 5 Experiemental
# 6 Single ticks (uses group count)

#SINGLE
if type == 1:
    #Params: seed type, base, kernel, seed, width, height
    s = Single_Driver(1, 2, 5,'11110010011011001100001000111100' , 4000, 4000) #nested triangle seed
    #s = Single_Driver(2, 8, 2,'050752073546101', 2000, 600) #max size:  1100x1100 dpi = 1400
    #s = Single_Driver(2, 8, 2,'763256651547454', 400, 400)
    #s = Single_Driver(2, 8, 2,'507520735461010', 400, 100)
    #Params: start type, steps |#DEF: groups, high-low ratio
    s.Init_Simulation(4, 4000, 1)
    s.Init_Colormaps()#'gist_stern')#'gist_ncar')#'jet')#'gist_earth')#'CMRmap')
    s.Run_Simulation() #steps
    s.Save()
    #s.Display()

#GROUP
elif type == 2:
    #Params: seed type, base, kernel, width, height, steps
    g = Group_Driver(1, 7, 2, 600, 400, 200)
    #Params: iterations, ordered, start_type  |#DEF: start groups, start_ratio
    g.Init_Simulation_Group(5,False,2, 3)
    g.Init_Colormaps()
    g.Run_Simulation_Group()

#ANIMATION
elif type == 3:
    #Params: seed type, base, kernel, seed, width, height
    a = Animation_Driver(2, 3, 9,'2020101121101110002', 200, 100)
    #Params: start type, steps |#DEF: groups, high-low ratio
    a.Init_Simulation(2,1600, 2)
    a.Init_Colormaps('gist_earth')
    a.Run_Simulation()
    a.Display_Animation()
