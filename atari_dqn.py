import sys
sys.path.insert(0, 
'/home/juna/Documents/Projects/atari_project/Arcade-Learning-Environment/ale_python_interface')

import cv2
import random
import numpy as np
import time as t
import neural_net as nn
import torch as tc
import torchvision as tv
from ale_python_interface import ALEInterface



def impre(name_of_the_game, image):
    image = cv2.resize(image, (84, 110))
    image = tc.from_numpy(image).long()

    if name_of_the_game == 'Breakout':
        image = image[18:18+84, :]
    elif name_of_the_game == 'enduro':
        image = image[0:0+84, :]
    elif name_of_the_game == 'pong':
        image = image[17:17+84, :]
    elif name_of_the_game == 'qbert':
        image = image[10:10+84, :]
    elif name_of_the_game == 'Seaquest':
        image = image[13:13+84, :]
    elif name_of_the_game == 'space_invaders':
        image = image[18:18+84, :]
    return image


def ep_greedy(ep, state, minimal_actions, nn):

    Qvalues = nn.test(state)[0, minimal_actions]
    num = random.random()

    index = tc.argmax(Qvalues).type(tc.long)
    Qmax = Qvalues[index]
    Amax = tc.Tensor([minimal_actions[index]]).long()

    if num < ep + (1-ep)/len(minimal_actions):
        action_index = random.randrange(0, len(minimal_actions)-1)
        if action_index >= index:
            action_index = action_index + 1
        # del Qvalues, num, Qmax, index
        return tc.Tensor([minimal_actions[action_index]]).long()
    else:
        return Amax
        


def get_Qmax(state, minimal_actions, nn):
    Qvalues = nn.test(state)[0, minimal_actions]
    index = tc.argmax(Qvalues)
    # print('index :\n', index)
    # print('type(Qvalues :\n', Qvalues)
    Amax = tc.Tensor([minimal_actions[index]]).long()
    Qmax = Qvalues[index]
    # print('Qmax :\n', Qmax)
    return Amax, Qmax

def starting_frame_num(model_path):
    for i in range(len(model_path)):
        if model_path[i:i+3] == '.h5':
            for j in range(i):
                if model_path[i-j] == '_':
                    starting_frame_num = int(model_path[i-j+1:i])
                    return starting_frame_num

count_5e4 = 0
count_1e6 = 0
count_target_nn_update = 0

load_model = False
model_path = '/home/juna/Documents/Projects/atari_project/models/atari_10000.h5'
sample_num = 32
memory_size = int(2e4)
replay_memory_size = int(1e4)
gamma = 0.99
ep = 1
action = None
ale = ALEInterface()
vf = nn.Neural_Net()
vf.cuda()
if load_model == True:
    vf.main_model.load_state_dict(tc.load(model_path))
    vf.update_model.load_state_dict(tc.load(model_path))
gpu_dtype = tc.cuda.FloatTensor
cpu_dtype = tc.FloatTensor
# device = tc.device("cuda:0" if tc.cuda.is_available() else "cpu")
# vf = nn.Neural_Net().to(device)


# get screen or not
USE_SDL = False
if USE_SDL:
    ale.setBool(b'display_screen', True)

# load game rom file
name_of_the_game = 'space_invaders'
game_path = '/home/juna/Documents/Projects/atari_project/Arcade-Learning-Environment/roms/'+name_of_the_game+'.bin'
ale.loadROM(game_path.encode())

minimal_actions = ale.getMinimalActionSet()

print('minimal_actions :\n', minimal_actions)

screen_data = None


#initialize the state
image = ale.getScreenGrayscale(screen_data)
image = impre(name_of_the_game, image)
state = tc.stack((image, image, image, image), dim=0).unsqueeze(0).type(gpu_dtype)
del image

memory_buffer = []
# state_m = tc.zeros(sample_num, 4, 84, 84).type(gpu_dtype)
y = tc.zeros([sample_num, 18]).type(gpu_dtype)


frame_num = ale.getFrameNumber()

# start = t.time()

# iteration loop
while frame_num < 1e7:


    # reset_game if the game is over
    if ale.game_over() == True:
        ale.reset_game()
        image = ale.getScreenGrayscale(screen_data)
        image = impre(name_of_the_game, image)
        state = tc.stack((image, image, image, image), dim=0).unsqueeze(0).type(gpu_dtype)
        del image

    # take action!!!!!
    if frame_num % 4 != 0:
        pass
    else:
        action = ep_greedy(ep, state, minimal_actions, vf)
    reward = tc.Tensor([ale.act(action)]).long().type(gpu_dtype)
    frame_num = ale.getFrameNumber()
    ep -= 9e-7

    # preprocess new state
    '''you should check how screen looks when the game is over'''
    image = ale.getScreenGrayscale(screen_data)
    image = impre(name_of_the_game, image).unsqueeze(0).unsqueeze(0).type(gpu_dtype)
    
    # make the image black when the game is over
    if ale.game_over() == True:
        print('@@@@@game_over@@@@@')
        image = tc.zeros_like(image)
    new_state = tc.cat([state, image], dim=1)[:, 1:5, :, :]

    '''When it gets to the frame_limit,
    you have to finish the game and save weights!!!!!!!'''
    
    # Save information in memory buffer
    memory_buffer.append((state, action, reward, new_state)) ####################
    # state = state.type(gpu_dtype)
    state = new_state.type(gpu_dtype)
    del new_state, image, reward
    
    if frame_num % 100 == 0:
        print('frame_num :', frame_num)

    if frame_num >= replay_memory_size:
        if count_5e4 == 0:
            count_5e4 += 1
            print('==============='+str(replay_memory_size)+'_frames===============')

        if frame_num >= memory_size:
            memory_buffer = memory_buffer[1:]
            ep = 0.1
        
        # update frequency is 4
        if frame_num % 4 == 0:
            point = t.time()
            minibatch = random.sample(memory_buffer, sample_num)
            random_sample_t = t.time() - point
            print('random_sample_t :', random_sample_t)

            state_m = []
            # get Qmax value at new state
            point = t.time()
            for i in range(sample_num):
                # print('minibatch[i][0] :\n', minibatch[i][0])
                # print('tc.sum(minibatch[i][0]) :\n', tc.sum(minibatch[i][0]))
                # print('minibatch[i][0].size() :\n', minibatch[i][0].size())
                # point = t.time()
                state_m.append(minibatch[i][0])
                action_m = minibatch[i][1]
                reward_m = minibatch[i][2]
                next_state_m = minibatch[i][3]
                # seperate_t = t.time() - point
                # print('seperate_t :', seperate_t)

                if tc.sum(next_state_m[0,-1,30,:]) == 0 and tc.sum(next_state_m[0,-1,:,:]) == 0:
                    Qmax = 0
                else:
                    # print('state_m[i].unsqueeze(0).size() :\n', state_m[i].size())
                    _, Qmax = get_Qmax(state_m[i], minimal_actions, vf)

                # print('reward_m.size() :\n', reward_m.size())
                # print('Qmax :\n', Qmax)
                y[i] = vf.test(state_m[i])
                y[i, action] = reward_m + gamma * Qmax
                
            making_y_t = t.time() - point
            print('making_y_t :', making_y_t)
            
            state_m = tc.cat(state_m, dim=0).type(gpu_dtype)
            # print('state_m.size() :\n', state_m.size())
            point = t.time()
            vf.train(state_m.detach(), y.detach())
            train_t = t.time() - point
            print('train_t :', train_t)

            if frame_num % 1e4 == 0:
                vf.target_nn_update()
                
                if load_model == True:
                    num = starting_frame_num(model_path)
                    
                    tc.save(vf.update_model.state_dict(), \
                        '/home/juna/Documents/Projects/atari_project/models/atari_'+str(frame_num+num-replay_memory_size)+'.h5')
                
                tc.save(vf.update_model.state_dict(), \
                    '/home/juna/Documents/Projects/atari_project/models/atari_'+str(frame_num)+'.h5')
                print('===============main_model_updated===============')



    # image_save = np.stack((image, image, image), axis=2)
    # print('image.shape :\n', image.shape)
    # cv2.imwrite('/home/juna/Documents/Projects/atari_project/screenshot/'+name_of_the_game+'_'+str(step)+'.jpg', image_save)

