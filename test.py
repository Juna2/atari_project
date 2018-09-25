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

a = np.array([[[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]]])

print(a.shape)
print(np.concatenate((a, a, a), axis=1).shape)