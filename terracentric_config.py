###config###

import numpy as np

tm = 0
theta = 0
a = 0.1
b = 2
c = 1
d = 0
e = 0
f = 360


pln_array = np.array(
    [### pln        phi|phase |  g |  b |  a |
        ["sun",       0, 0, np.array((255, 212,  60))],
        ["moon",      0, 0, np.array((182, 182, 182))],
        ["mercury",   0, 0, np.array((198, 153,  86))],
        ["venus",     0, 0, np.array((255, 185, 185))],
        ["mars",      0, 0, np.array((203,  50,  50))],
        ["jupiter",   0, 0, np.array((212, 197, 157))],
        ["saturn",    0, 0, np.array((255,   0,   0))],
        ["uranus",    0, 0, np.array(( 81, 180, 255))],
        ["neptune",   0, 0, np.array(( 43,  64, 255))],
        #["notaplanet",0, 0, np.array(( 43,  64, 255))]
    ],
    dtype=object,
)

mrk_array = np.array(
    [
        ["sunrise", 0, 0, np.array((50,0,0))],
        ["sunset", 0, 0, np.array((0,0,50))],
        ["noon", 0, 0, np.array((50,50,50))],
    ]
)

n_LED = 120
m_LED = 3

led_array = np.zeros((n_LED*m_LED, 5), dtype=object)

key = {0: 9.5, 1: 10, 2: 10.5}
    #### [led ,   phi, phase, (r, g, b), rho]
for m in range(m_LED):
    for n in range(n_LED):
        ind = n+m*n_LED
        led_array[ind, 0] = "LED" + str(ind).zfill(4)
        led_array[ind, 1] = np.float32(2*np.pi*(n/n_LED))
        led_array[ind, 2] = np.float32(1*(m/m_LED))
        #led_array[ind, 2] = 2 * np.pi * (m / m_LED)
        led_array[ind, 3] = np.array((0,0,0), dtype="float32")
        led_array[ind, 4] = np.float32(key[m])



print(pln_array)
print(led_array)