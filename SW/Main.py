from Stitched_Driver import Stitched_Driver
from collections import OrderedDict
from matplotlib import cm

#These parameters control the simulation or group of simulations you are running
#images are saved to "C:/Users/[whoever]/Desktop/"
cmaps = OrderedDict()
cf = []

#Number of simulation images saved
# if one simulation is selected, it will be
# displayed as well as saved
cf.append(1) #stitched simulation count

#number of seeds each image will have
cf.append(4) #segment count

#width of each image
cf.append(200) #px

#Number of steps ran for each seed before changing
cf.append([75,50]) #segment heights

#Load seeds, random seeds if empty
cf.append([]) #random seeds

#rule type 1, Elementary CA
#rule type 2, Totalistic CA
#totalistic performs better with more colors
cf.append(2) #rule type

#number of colors used
cf.append(3) #base

#kernels are NxN matrices dictacting which
#cell group is to be evaluated when deciding 
#what the next cell will be in the row.
# Examples:
#------------
# O O X X X O O
#       C ->
# 3 x 1
#kernel = [[0,0,0],[0,0,0],[1,1,1]]
#------------
# O O X O X O O
# O O O X O O O
# O O X O X O O
#       C ->
kernel = [[1,0,1],[0,1,0],[1,0,1]]
#------------
cf.append(kernel)

#Seed options
#1. 'random' : first seed of each image is random
#   A.  'random' : all remaining seeds in each image are random
#   B.  'ordered' : all remaining seeds are incremented based on the first seed
#
#2. 'loaded' : first seed of each image is chosen from loaded seed array
#   A.  'random loaded' : remaining seeds of each image are randomly chosen
#   B.  'cyclic loaded' : remaining seeds of each image is chosen incrementally, 
#                         looping if length of seed array is less than image count
#   C.  'random'        : remaining seeds of each image are chosen randomly outside of 
#                         seed array
cf.append('random') #first seed option
cf.append('random') #remaining seeds option


#initial rows for all images in a group
#start type
#   1 : non-groups
#       1 : randomized
#       2 : steps up with gap
#       3 : steps down with gap

#   2 : groups
#       1 : evenly spaced groups based on group count
#       1 : randomly spaced groups based on group count

cf.append(2) #start type
cf.append(1) #start sub type

# gap count : for start types (1,2) & (1,3)
cf.append(2) #gap

# group count : for start types (2,1) & (2,2)
cf.append(1) #groups

# step count for each seed options
# 1. 'cyclic' : uses segment height in order of segment heights array
# 2. 'random loaded' : randomly choses segment heights from segment heights array
# 3. 'random' : only 2 heights are in segment heights array
#               [ upper_height_bound, lower_height_bound ]
#               random height values are chosen between upper and lower bound
cf.append('cyclic') #heights option

#size of each image being saved
cf.append(4) #save MB

# saves each image in all color maps within Favorites
cf.append(False) #Save all colormaps


# Colormap category selection
cmaps['Selection'] = 'Favorites'

# Available groups of colormaps
cmaps['Perceptually Uniform Sequential'] = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
cmaps['Sequential'] =                      ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
cmaps['Sequential (2)'] =                  ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']
cmaps['Diverging'] =                       ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
cmaps['Qualitative'] =                     ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']
cmaps['Miscellaneous'] =                   ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv', 'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
cmaps['Favorites'] =                       ['jet','gist_stern','PuOr', 'viridis', 'gist_stern','ocean', 'gist_earth', 'terrain','CMRmap', 'cubehelix', 'coolwarm', 'jet']
cmaps['Austere'] =                         ['binary']

#================================================================
#Start of simulation sequence, DO NOT MODIFY
s = Stitched_Driver(cf[0], cf[1], cf[2], cf[3]) #new
s.Setup_Seeds(cf[4],cf[5],cf[6],cf[7],cf[8],cf[9])
s.Setup_Saving()
s.Setup_Initial_Conditions(cf[10],cf[11],cf[12],cf[13],cf[14])
s.Load_Cmaps(cmaps)
s.Run_Stitches(cf[15], cf[16])
#================================================================
