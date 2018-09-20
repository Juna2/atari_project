import copy
import torch as tc
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable


class Flatten(nn.Module):
    def forward(self, x):
        N, C, H, W = x.size()
        return x.view(N, -1)


class Neural_Net(Flatten):
    def __init__(self, lr=2.5e-4, dtype=tc.cuda.FloatTensor):
        super(Neural_Net, self).__init__()
        self.learning_rate = 1e-3
        self.dtype = dtype
        
        # x = Variable(tc.randn(1, 4, 84, 84).type(gpu_dtype), requires_grad=False)
        '''NN 수정해야함'''
        model = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=8, stride=4),
            nn.ReLU(inplace=True),

            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            Flatten(),

            nn.Linear(3136, 512),
            nn.Linear(512, 18)
        )

        self.main_model = model
        self.update_model = model

        self.criterion = nn.MSELoss()
        self.main_optimizer = tc.optim.RMSprop(self.main_model.parameters(), lr, alpha=0.95)
        self.update_optimizer = tc.optim.RMSprop(self.update_model.parameters(), lr, alpha=0.95)

    def train(self, state, y):
        self.update_optimizer.zero_grad()
        out = self.update_model(state)
        cost = self.criterion(out, y)
        cost.backward(retain_graph=True)
        self.update_optimizer.step
        return out, cost.data

    def test(self, state):
        self.main_optimizer.zero_grad()
        out = self.main_model(state)
        return out        
        

    def target_nn_update(self):
        self.main_model = self.update_model

        # criterion = nn.CrossEntropyLoss()
        # optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        # if mode == 'train':


        # elif mode == 'test':
        #     ~~~~

        # else:
        #     print('You need chose one of between train and test')
