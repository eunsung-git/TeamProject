import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

def color_dect(image):
    img = io.imread(image)

    resize_img = img[int(img.shape[0]*0.3):int(img.shape[0]*0.5),
                    int(img.shape[1]*0.3):int(img.shape[1]*0.5), :]
    pixels = np.float32(resize_img.reshape(-1, 3))
    
    n_colors = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    
    classifier = KNeighborsClassifier(n_neighbors=1)
    
    training_points = [
        [255, 0, 0], [255, 94, 0], 
        [255, 167, 167], [255, 193, 158],
        [255, 95, 95], [242, 150, 97],
        [204, 61, 61], [204, 114, 61],
        [152, 0, 0], [153, 56, 0],
        [103, 0, 0], [102, 37, 0],
        ########## red
        [255, 187, 0], [255, 228, 0],
        [255, 224, 140], [250, 237, 125],
        [242, 203, 97], [229, 216, 92],
        [204, 166, 61], [196, 183, 59],
        [153, 112, 0], [153, 138, 0], 
        [102, 75, 0], [102, 92, 0], 
        ########## yellow
        [171, 242, 0], [29, 219, 22],
        [206, 242, 121], [183, 240, 177],
        [188, 229, 92], [134, 229, 127],
        [159, 201, 60], [71, 200, 62],
        [107, 153, 0], [47, 157, 39],
        [71, 102, 0], [34, 116, 28],
        ########## green
        [0, 216, 255], [0, 84, 255],
        [178, 235, 244], [178, 204, 255],
        [92, 209, 229], [103, 153, 255],
        [61, 183, 204], [67, 116, 217],
        [0, 130, 153], [0, 51, 153],
        [0, 87, 102], [0, 34, 102],
        ########## blue
        [1, 0, 255], [95, 0, 255],
        [181, 178, 255], [209, 178, 255],
        [107, 102, 255], [165, 102, 255],
        [70, 65, 217], [128, 65, 217],
        [5, 0, 153], [63, 0, 153],
        [3, 0, 102], [42, 0, 102],
        ########## navy
        [255, 0, 221], [255, 0, 127],
        [255, 178, 245], [255, 178, 217],
        [243, 97, 220], [243, 97, 166],
        [217, 65, 197], [217, 65, 140],
        [153, 0, 133], [153, 0, 76],
        [102, 0, 88], [102, 0, 51],
        ########## pink
        [0, 0, 0], [25, 25, 25],
        [33, 33, 33], [53, 53, 53],
        ########## black
        [166, 166, 166], [140, 140, 140],
        [116, 116, 116], [93, 93, 93], [76, 76, 76],
        ########## gray
        [255, 255, 255],
        [246, 246, 246], [234, 234, 234],
        [213, 213, 213], [189, 189, 189]
        ########## white
    ]
    training_labels = [0]*12
    training_labels.extend([1]*12)
    training_labels.extend([2]*12)
    training_labels.extend([3]*12)
    training_labels.extend([4]*12)
    training_labels.extend([5]*12)
    training_labels.extend([6]*4)
    training_labels.extend([7]*5)
    training_labels.extend([8]*5)
    
    classifier.fit(training_points, training_labels)
    color_index = classifier.predict([list(dominant)])
    color_dict = {0:'red', 1:'yellow', 2:'green', 3:'blue', 4:'navy', 5:'pink', 6:'black', 7:'gray', 8:'white'}

    color = color_dict[color_index[0]]
    return color