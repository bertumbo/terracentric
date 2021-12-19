from numpy import pi
import numpy as np
from random import random as rd



class Snake:
    instances = []
    def __init__(self):
        self.__class__.instances.append(self)
        self.len = 50
        self.vel = 0.05
        self.phi = 0
        self.last_pos = []
        self.acc = 0.01
        self.segments = []
        #self.end = 0

    #def get_end(self):
    #    self.end = self.phi + self.len/120*2*pi


    def new_pos(self):

        self.phi += self.vel
        if self.phi >= 2*np.pi:
            self.phi -= 2*np.pi
        self.vel += (rd()-0.5)/40
        self.last_pos.append(self.phi)
        if len(self.last_pos) >= self.len:
            #self.last_pos.pop()
            self.last_pos.pop(0)
        self.segments = []
        for i in range(len(self.last_pos)):
            try:
                self.segments.append([self.last_pos[i], self.last_pos[i+1]])
            except:
                pass
        #print(self.segments)




        #print(self.last_pos)


class Player:
    def __init__(self):
        self.phi = 0

#Snake()

#for i in range(100):
#    for snk in Snake.instances:
#        snk.new_pos()




