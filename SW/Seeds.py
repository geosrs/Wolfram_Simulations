#from itertools import permutations

import numpy as np
import random
class Seeds:

    def __init__(self, base = 0):
        pass

    #loads seed information
    def Config(self, seed_type, base, kernel_length):
        self.seed_type = seed_type
        if seed_type == 1: #elementary
            self.seed_length = base ** kernel_length
        elif seed_type == 2: #totalistic
            self.seed_length = kernel_length * (base - 1) + 1
        self.base = base
        self.kernel_length = kernel_length

    #generates a single random seed
    def Generate_Random_Seed(self):
        seed = [random.randint(0,self.base - 1) for x in range(self.seed_length)]
        return ''.join(map(str,seed))
    
    #generates an array of random seeds
    def Generate_Random_Seeds(self,count):
        return  [self.Generate_Random_Seed() for x in range(count)]

    #generates a range of seeds
    #upper and lower are decimal inputs
    def Generate_Seed_Range(self,lower_bound, upper_bound, length = 0):
        result = []
        if (length == 0):
            length = upper_bound - lower_bound

        for i in range(lower_bound, upper_bound):
            cur_seed = self.base10toN(i,self.base)
            while (len(cur_seed) != length):
                cur_seed = '0' + cur_seed
            result.append(cur_seed)
        return self.To_Int_Array(result,length)

    #changes a string into an array of integers
    def To_Int_Array(self, array, str_len):
        result = []
        for i in range(len(array)):
            temp = []
            for j in range(str_len):
                temp.append(int(array[i][j]))
            result.append(temp)
        return result

    #changes a number from base 10 to any other base
    def base10toN(self,num, base):
        """Change ``num'' to given base
        Upto base 36 is supported."""
        converted_string, modstring = "", ""
        currentnum = num

        if not num:
            return '0'
        while currentnum:
            mod = currentnum % base
            currentnum = currentnum // base
            converted_string = chr(48 + mod + 7*(mod > 10)) + converted_string
        return converted_string

    #changes a number from any base to base 10
    def Convert(self,base0,n):
        length = len(n)
        sum = 0
        max_bit_vals = []
        for i in range(length):
            digit = int(n[(length - 1) - i]) #reverse string
            sum += (digit * (base0 ** i))
            max_bit_vals.append(base0 ** i)
        return str(sum)
