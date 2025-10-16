from numpy import pi
import numpy as np
import random as rd

f = 0.05
k = 1
s = 0.1

class Snake2:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.len = 5
        self.f = 0.05
        self.k = 0.5
        self.s = 0.1
        self.timer = 0
        self.activity = "red"
        self.dots = np.zeros(shape=self.len)
        self.segments = np.zeros(shape=(self.len-1, 2))
    def calc_step(self):
        c_arr = np.copy(self.dots)
        arr = self.dots
        segs = self.segments

        self.f += rd.randint(-3,3)/100

        if self.timer == 0:
            gamble = rd.randint(0,100)
            if gamble >=99:
                self.timer += 200
        if self.timer > 150:
            self.activity = "halfgreen"
            self.timer -= 1
        elif self.timer > 0:
            self.activity = "green"
            self.timer -= 1
        elif self.timer == 0:
            self.activity = "red"




        for ind, dot in enumerate(self.dots):
            if ind == 0:
                arr[0] = c_arr[0] + self.f
            else:
                arr[ind] = c_arr[ind] + (c_arr[ind-1] - c_arr[ind] - self.s)*self.k

        for ind, seg in enumerate(self.segments):
            if ind == 0:
                pass
            else:
                segs[ind-1] = arr[ind-1], arr[ind]
        print(arr)
        print(segs)


class Snake:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.len = 10
        self.vel = 0.05
        self.phi = 0
        self.last_pos = []
        self.acc = 0.01
        self.segments = []
        self.active = False
        #self.end = 0

    #def get_end(self):
    #    self.end = self.phi + self.len/120*2*pi


    def new_pos(self):

        self.phi += self.vel
        if self.phi >= 2*np.pi:
            self.phi -= 2*np.pi
        #self.vel += (rd()-0.5)/40
        self.last_pos.append(self.phi)
        try:
            self.segments.append([self.last_pos[0], self.last_pos[1], self.active])
        except:
            pass
        if len(self.last_pos) >= self.len:
            #self.last_pos.pop()
            self.last_pos.pop(0)
            self.segments.pop(0)
        #self.segments = []
        #for i in range(len(self.last_pos)):
        #    try:
        #        self.segments.append([self.last_pos[i], self.last_pos[i+1]])
        #    except:
        #        pass
        #print(self.segments)




        #print(self.last_pos)


class Player:
    def __init__(self):
        self.phi = 0

#Snake()

#for i in range(100):
#    for snk in Snake.instances:
#        snk.new_pos()

#sn = Snake2()
#for i in range(100):
#    sn.calc_step()



