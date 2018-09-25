import cv2
import torch as tc
import torch.nn as nn
import torch.optim as optim
import neural_net as neunet
import numpy as np
import random
import time as t
from sys import getsizeof
import matplotlib.pyplot as plt
from torch.autograd import Variable


import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    pullData = open('/home/juna/atari_project/plot/list.txt', 'r').read()
    dataArray = pullData.split('\n')
    xarr = []
    yarr = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xarr.append(int(x))
            yarr.append(int(y))
    ax1.clear()
    ax1.plot(xarr, yarr)
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
