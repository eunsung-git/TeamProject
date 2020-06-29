import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier


def color_dect(image, top=True):
    img = io.imread(image)
    if top:
        resize_img = img[int(img.shape[0]*0.4):int(img.shape[0]*0.6),
                         int(img.shape[1]*0.4):int(img.shape[1]*0.6), :]
    else:
        resize_img = img[int(img.shape[0]*0.3):int(img.shape[0]*0.5),
                         int(img.shape[1]*0.3):int(img.shape[1]*0.5), :]
    pixels = np.float32(img.reshape(-1, 3))
    
    n_colors = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    
    classifier = KNeighborsClassifier(n_neighbors=1)
    if top:
        training_points = [
            [213, 186, 152], # beige
            [0, 0, 255], # blue
            [0, 140, 78], # green
            [0, 0, 64], # navy
            [255, 0, 0], # red
            [255, 255, 0] # yellow
        ]
        training_labels = [0, 2, 5, 7, 8, 10]
    else:
        training_points = [
            [213, 186, 152], # beige
            [0, 0, 0], # black
            [241, 240, 226], # cream
            [68, 55, 123], # deepblue
            [163, 146, 100], # kaki
            [172, 223, 221], # skyblue
        ]
        training_labels = [0, 1, 3, 4, 6, 9]
    
    classifier.fit(training_points, training_labels)
    color_index = classifier.predict([list(dominant)])
    color_dict = {0:'beige', 1:'black', 2:'blue', 3:'cream', 4:'deepblue', 5:'green', 6:'khaki', 7:'navy', 8:'red', 9:'skyblue', 10:'yellow'}

    color = color_dict[color_index[0]]
    return color