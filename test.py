import cv2
import torch as tc
import torch.nn as nn
import torch.optim as optim
import neural_net as neunet
import numpy as np
import random
import time
from sys import getsizeof
from torch.autograd import Variable

b = tc.Tensor([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
c = tc.Tensor([[[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]], [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]])
e = tc.Tensor([])
f = tc.Tensor([1, 2, 3, 4, 5, 6, 7, 8, 9]).long()

b = np.array([1, 2, 3, 4, 5])

s = '10000'
print(int(s))