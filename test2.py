import time as t

for i in range(100):
    f = open('/home/juna/atari_project/plot/list.txt', 'a')
    f.write(str(i)+','+str(i*i))
    f.close()
    t.sleep(0.2)