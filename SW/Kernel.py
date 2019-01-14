from PIL import Image
import numpy as np

#this class creates a kernel from the inputted 2D array
#also calculates linearized and ordered pair versions of kernels

class Kernel:

    #input kernel needs to be square, or integer to represent horizontal line (legacy)
    def __init__(self, kernel):
        self.grid_format_kernel = kernel
        self.linear_kernel = []
        self.ordered_pair_kernel = []
        self.def_kernel = True
        self.k_dim = len(kernel[0])
        self.start_rows_needed = 0
        self.def_kernel = False
        print(kernel)
        try:
            for i in range(self.k_dim):
                r = 0
                for j in range(self.k_dim):
                    r += kernel[i][j]
                if r > 0:
                    self.start_rows_needed += 1
        except:
            print('\nShape of kernel matrix is incorrect.')
            quit()
            
        for i in range(self.k_dim):
            for j in range(self.k_dim):
                result = kernel[i][j]
                self.linear_kernel.append(result)
                if result == 1:
                    self.ordered_pair_kernel.append([j - (int(self.k_dim / 2)), self.k_dim - i - 1])
        self.linear_kernel_length = len(self.ordered_pair_kernel)


