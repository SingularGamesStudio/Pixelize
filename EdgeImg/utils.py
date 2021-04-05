import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import os
import scipy.misc as sm

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def load_data(file):    
    img = mpimg.imread(file)
    img = rgb2gray(img)
    return img


def visualize(img, num):
    plt.imshow(img, cmap='gray')
    plt.savefig("foo"+str(num)+".png")

    