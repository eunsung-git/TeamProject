import pandas as pd
import random
from sklearn.neighbors import KNeighborsClassifier

def color_match(c1, c2):
    color_dict = {0:'red', 1:'yellow', 2:'green', 3:'blue', 4:'navy', 5:'pink', 6:'black', 7:'gray', 8:'white'}
    
    train_point = [[top, bottom] for top in range(9) for bottom in range(9)]

    train_label = [1, 1, 1, 1, 1, 1, 0, 1, 0, # top = red
                   1, 1, 0, 1, 0, 1, 0, 1, 0, # top = yellow
                   1, 1, 1, 1, 1, 1, 0, 1, 0, # top = green
                   1, 1, 1, 1, 0, 1, 0, 1, 0, # top = blue
                   1, 0, 0, 1, 1, 1, 0, 0, 0, # top = navy
                   1, 1, 1, 1, 1, 1, 0, 1, 0, # top = pink
                   0, 0, 0, 0, 1, 0, 0, 0, 0, # top = black
                   1, 1, 1, 1, 0, 1, 0, 1, 1, # top = gray
                   0, 0, 0, 0, 0, 0, 0, 1, 1] # top = white
    
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(train_point, train_label)
    
    n1 = list(color_dict.values()).index(c1)
    n2 = list(color_dict.values()).index(c2)
    
    result = classifier.predict([[n1, n2]])[0]
    
    return result
