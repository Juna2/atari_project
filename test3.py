import paramiko
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('115.145.172.222', port='2048', username='mind-222', password='mind_passwd')
sftp_client = ssh.open_sftp()


def values(line, x, y):
    for i in range(len(line)):
        if line[i] == ',':
            x.append(int(line[:i]))
            y.append(int(line[i+1:]))
            return x, y
    return x, y

def animate(i):
    remote_file = sftp_client.open('/home/juna/atari_project/plot/list.txt')
    xarr = []
    yarr = []
    try:
        for dataArray in remote_file:
            if len(dataArray) > 2:
                xarr, yarr = values(dataArray, xarr, yarr)
            ax1.clear()
            ax1.plot(xarr, yarr)
    finally:
        remote_file.close()


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()






# fig = plt.figure()
# ax1 = fig.add_subplot(1, 1, 1)

# def animate(i):
#     pullData = open('/home/juna/atari_project/plot/list.txt', 'r').read()
#     dataArray = pullData.split('\n')
#     xarr = []
#     yarr = []
#     for eachLine in dataArray:
#         if len(eachLine) > 1:
#             x, y = eachLine.split(',')
#             xarr.append(int(x))
#             yarr.append(int(y))
#     ax1.clear()
#     ax1.plot(xarr, yarr)
# ani = animation.FuncAnimation(fig, animate, interval=100)
# plt.show()
