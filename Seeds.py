from itertools import permutations

import numpy as np
import random
class Seeds:


    def __init__(self,seed_type,kernel, base):#, length_totalistic,base, length_elementary):
        self.seed_type = seed_type
        self.kernel = kernel
        if seed_type == 1: #elementary
            self.seed_length = base ** kernel
        elif seed_type == 2: #totalistic
            self.seed_length = kernel * (base - 1) + 1

        self.base = base
        self.seed_group = []

    #upper and lower are decimal inputs
    def Generate_Seed_Range(self,lower_bound, upper_bound, length = 0):
        #allows for use by bother driver and grid classes with default parameter
        result = []
        if (length == 0):
            length = upper_bound - lower_bound

        for i in range(lower_bound, upper_bound):
            cur_seed = self.base10toN(i,self.base)
            #print(self.seed_length)
            while (len(cur_seed) != length): #changed from != self.seed_lengh
                cur_seed = '0' + cur_seed

                #print(cur_seed)
            result.append(cur_seed)

            #self.seed_group.append(cur_seed)
        #print(self.seed_group)
        #print(self.To_Int_Array(result,length))
        return self.To_Int_Array(result,length)

    def Load_Seed_Group(self):
        self.seed_group = []
        temp_group = []
        path = 'C:\Files\Programming\Wolfram_Simulations\seed_ini.txt'
        print('Loading Seeds...' + 'From:' + path)
        file = open(path, "r")
        for line in file:
            if line[0] != '-':
                temp_group.append(line)
            else:
                print('Seed range ' + line +' removed.')
        print('Seed Group Loaded.')
        #self.seed_group = temp_group
        #print(self.seed_group)
        self.seed_group = self.To_Int_Array(temp_group)
        file.close()


    def To_Int_Array(self, array, str_len):
        result = []
        #for i in range(len(self.seed_group)):
        for i in range(len(array)):
            temp = []
            for j in range(str_len):
                #temp.append(int(self.seed_group[i][j]))
                temp.append(int(array[i][j]))
            result.append(temp)
            #self.seed_group[i] = temp
        return result

    def Print_Seeds(self):
        print('Base:\t' + str(self.base) + '\nSeed Count:\t' + str(len(self.seed_group)))
        for i in self.seed_group:
            print(''.join(map(str,i)) + '\t:\t')# + b_t)


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


    def Generate_Random_Seed(self):
        seed = [random.randint(0,self.base - 1) for x in range(self.seed_length)]
        return ''.join(map(str,seed))

    def Generate_Random_Seeds(self,count):
        return  [self.Generate_Random_Seed() for x in range(count)]



    #output(str)
    def Convert(self,base0,n):#,base1,n):
        length = len(n)
        sum = 0
        max_bit_vals = []
        for i in range(length):
            digit = int(n[(length - 1) - i]) #reverse string
            sum += (digit * (base0 ** i))
            max_bit_vals.append(base0 ** i)

        #print('Base 10 value:\t' + str(sum)) # At base 10
        #if base1 == 10:
        return str(sum)








#s = Seeds()
#s.Convert()
#s.Convert(4,10,'1130')


'''
s = Seeds(11,3)
print(s.Generate_Random_Seed())
#s.Print_Seeds()

#s.Generate_All_Seeds()
'''
