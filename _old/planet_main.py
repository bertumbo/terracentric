import planets_re1 as p
import time
from datetime import datetime
import numpy as np



imList = []
#str = "2021-11-19 18:38:11.137970"
#print(datetime.fromisoformat(str))


#create LED-Array
for dist in [10, 10.5, 11]:
    for deg in range(0, 360, int(360/120)):
        rad = np.deg2rad(deg)
        p.LED(dist, rad)



start = datetime.utcnow()
timestamp = datetime.timestamp(start)
pos = p.get_pln_pos(timestamp=timestamp)
theta = p.calculate_theta(timestamp=timestamp)
t_shift = 60*20
ind = 0
while ind <= 100:     #frame_counter
    tm = datetime.timestamp(datetime.utcnow())+ind*t_shift
    if ind % 1 == 0:   #every frame
        theta = p.calculate_theta(timestamp=tm)
        for led in p.LED.instances:
            led.check_state(pos, theta)
        p.draw_fig(timestamp=tm, imList=imList)
    if ind % 10 == 0:  # every 10th frame
        pos = p.get_pln_pos(timestamp=tm)
    print(ind, datetime.utcfromtimestamp(tm), datetime.timestamp(datetime.utcnow())+ind*t_shift-tm)
    ind += 1
name = "testfull"
filename = "%s.gif" % name
out = imList[0].save(filename, save_all=True, append_images=imList[1:], optimize=True, duration=1, loop=0)
