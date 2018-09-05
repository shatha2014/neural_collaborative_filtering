'''
Created on Aug 31, 2018
Processing Instagram dataset

@author: Shatha Jaradat (shatha@kth.se)
KTH - Royal Institute of Technology
'''

class outfitInstance(object):
    mainsubcategory = 0
    pattern = 0
    material = 0
    style = 0

    def __init__(self, val_subcategory, val_patterns, val_materials, val_style):
        self.mainsubcategory = val_subcategory
        self.pattern = val_patterns
        self.material = val_materials
        self.style = val_style
