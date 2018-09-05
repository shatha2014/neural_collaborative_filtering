'''
Created on Aug 31, 2018
Processing Instagram dataset

@author: Shatha Jaradat (shatha@kth.se)
KTH - Royal Institute of Technology
'''

import scipy.sparse as sp
import numpy as np
from outfit import outfitInstance

class InstagramDataset(object):
     def __init__(self, path):
        '''
        Constructor
        '''
        self.trainData = self.loadData_SingleValues(path)
        self.testData = self.loadData_SingleValues(path)
        #self.testNegatives = self.load_negative_file(path + ".test.negative")
        #assert len(self.testData) == len(self.testNegatives)

        #self.num_users, self.num_items = self.trainData.shape

     def loadData_SingleValues(self, filename):
        '''
        Read file and Return outfit class instance.
        '''
        # Get number of users and items
        userId, subcategories, patterns, materials, styles =0,0,0,0,0
        with open(filename, "r") as f:
            line = f.readline()
            lstOutfits_withStyles = []
            while line != None and line != "":
                arr = line.split("  ")
                print('length of array')
                print(len(arr))
                print(arr)
                subcategories = int(arr[0])
                patterns = int(arr[1])
                materials = int(arr[2])
                styles = int(arr[3])
                print('subcategory')
                print(subcategories)
                print('pattern')
                print(patterns)
                print('material')
                print(materials)
                print('style')
                print(styles)
                obj_outfit = outfitInstance(userId,subcategories,patterns,materials, styles)
                lstOutfits_withStyles.append(obj_outfit)
                line = f.readline()
        return lstOutfits_withStyles

#obj = InstagramDataset('/var/root/PycharmProjects/neural_collaborative_filtering/InstagramData/outfits_training')
#obj.loadData_SingleValues('/var/root/PycharmProjects/neural_collaborative_filtering/InstagramData/outfits_training')