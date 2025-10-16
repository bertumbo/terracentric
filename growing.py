import numpy as np
import time
import random

def clamp(x):
    return max(0, min(x, 255))


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return(x, y)

radius = 18
scale = 0.5

neighborhood = [
    [-6, -1, 5, 6],
    [-2, -1, 0, 2, 4, 5],
    [-3, -2, 1, 3, 4],
    [-3, 2, 8, 9],
    [1, 2, 3, 5, 7, 8],
    [0, 1, 4, 6, 7],
]

coordinates = [
    (0, 673.0),
    (0, 624.7),
    (0, 562.7),
    (-3, 532.0),
    (-3, 595.1),
    (-3, 651.6)
]

class LED:
    instances = []

    def __init__(self, neighbors):
        self.ID = len(self.__class__.instances)
        self.__class__.instances.append(self)
        self.neighbors = neighbors
        self.LED_neighbors = []
        self.color = np.array([0, 0, 0])

    def set_real_neighbors(self):
        for neighbor in self.neighbors:
            self.LED_neighbors.append(LED.instances[neighbor])


    def grow(self):
        print(self.color)
        self.color[0] = min(self.color[0] * 1.1, 255)
        self.color[1] = min(self.color[1] * 1.1, 255)
        self.color[2] = min(self.color[2] * 1.1, 255)

    def expand(self):
        random_neighbor = random.choice(self.LED_neighbors)
        if random_neighbor.color[0] == 0 and random_neighbor.color[1] == 0 and random_neighbor.color[2] == 0:
            random_neighbor.color = self.color * 0.1
            self.color = self.color * 0.9



for i in range(0, 360, 6):
    for j in range(6):
        neighbors = []
        for neighbor in neighborhood[j]:
            neighbors.append((i + neighbor) % 360)
        LED(neighbors)
        print(i + j)

for led in LED.instances:
    led.set_real_neighbors()

time.sleep(2)

LED.instances[100].color[:] = (20, 0, 0)

for l in LED.instances:
    print(f"{l.ID}: {l.neighbors}")

for i in range(12):
    for l in LED.instances:
        l.grow()

for l in LED.instances:
    l.expand()

for i in range(12):
    for l in LED.instances:
        l.grow()