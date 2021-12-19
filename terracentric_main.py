###################
###terracentric####
###by bertumbo#####
###################

import terracentric_functions as f
import terracentric_config as c
import terracentric_programs as p
import invisiball
import rattlesnake
import tkinter as tk
import numpy as np
from datetime import datetime
import time
#import matplotlib
#from matplotlib.pyplot import Figure
#matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint

class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side='left', anchor='w'):
      tk.Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = tk.IntVar()
         chk = tk.Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand="yes")
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)


f.refresh(
    r_tm=True,
    r_theta=True,
    r_pln_pos=True
)
f.get_led_state(True, True)

window = tk.Tk()
wtf = tk.Frame()
window.title("terracentric gui ;)")
width = 800
height = 800
offx = width/2
offy = height/2
sc = 30


p1 = tk.PanedWindow()
p1.pack(fill='both', expand=1, side="left")

p2 = tk.PanedWindow(p1, orient='vertical')
p1.add(p2)
p2.pack(side="top")

p3 = tk.PanedWindow(p1, orient="horizontal")
p1.add(p3)
p3.pack(side="left", anchor="s")
#p2.pack(side="top", anchor="n")

entry_tm = tk.Entry()
time_label = tk.Label(text="frame", height=3)
#time_label2 = tk.Label(text="time")
pwr_label = tk.Label(text="pwr", height=4)
canv = tk.Canvas(width=width, height=height, bg="#000000")
canv2 = tk.Canvas(width=300, height=200, bg="#000000")
sld_a = tk.Scale(resolution=0.01,  from_=0, to=2*np.pi, orient="vertical", length=500)
sld_b = tk.Scale(resolution=0.1,  from_=0, to=5, orient="vertical", length=500)
sld_c = tk.Scale(resolution=0.1,  from_=0, to=10, orient="vertical", length=500)
sld_d = tk.Scale(resolution=0.001, from_=-2*np.pi, to=2*np.pi, orient="vertical", length=500)
sld_e = tk.Scale(resolution=0.001, from_=0, to=1, orient="vertical", length=500)
sld_f = tk.Scale(resolution=1, from_=0, to=360, orient="vertical", length=500)
lng = Checkbar(window, ["r_tm", 'r_theta', 'r_pln_pos'])
lng2 = Checkbar(window, ['r_led', 'drw_pln', 'drw_mrk'])
lng3 = Checkbar(window, ['use_realtime', 'use_dtm'])
lng4 = Checkbar(window, ['terracentric', 'rattlesnake'])

sld_a.set(str(c.a))
sld_b.set(str(c.b))
sld_c.set(str(c.c))
sld_d.set(str(c.d))
sld_e.set(str(c.e))
sld_f.set(str(c.f))

#lng.pack(side="top")
#lng2.pack(side="top")
#lng3.pack(side="top")
#time_label.pack(side="top", expand=1)
#time_label2.pack(side="top")
#entry_tm.pack(side="top")
canv.pack(side="right")
#pwr_label.pack(anchor="w")

# sld_a.pack(side="left")
# sld_b.pack(side="left")
# sld_c.pack(side="left")
# sld_d.pack(side="left")
#sld_e.pack(side="left")
#sld_f.pack(side="left")

p2.add(lng)
p2.add(lng2)
p2.add(lng3)
p2.add(lng4)
p2.add(time_label)
#p2.add(time_label2)
p2.add(entry_tm)
p2.add(pwr_label)

#p2.add(canv2)
#p2.add(wtf)
p3.add(sld_a)
p3.add(sld_b)
p3.add(sld_c)
p3.add(sld_d)
p3.add(sld_e)

#time_label.pack(side="left")

entry_tm.insert(0, str(datetime.fromtimestamp(c.tm)))

for led in c.led_array:
    x, y = f.pol2cart(led[4], led[1])
    f.create_circle((x*sc + offx), (-y*sc + offy), 8, canv, col=led[3])


#p.random_canv(canv, window, pwr_label)

#mainloop-structure:
#--read and refresh user-param
#--refresh variables (tm, theta, pln_array, led_array)
#--refresh led-state
#--limit led-state into ltd_array
#--render leds


#p.snake(canv, window, pwr_label)

#p.invisiball(canv, window)
#p.snake2(canv, window, pwr_label)
rattlesnake.Snake()
rattlesnake.Player()
#Ball()
frame = 0
while True:
    if frame%1==0:
        start = datetime.utcnow()
        ref = list(lng.state())
        drw = list(lng2.state())
        rt = list(lng3.state())
        mode = list(lng4.state())
        c.a = np.float16(sld_a.get())
        c.b = np.float16(sld_b.get())
        c.c = np.float16(sld_c.get())
        c.d = np.float16(sld_d.get())
        c.e = np.float16(sld_e.get())
        c.f = np.float16(sld_f.get())
        #state = list(lng.state())
        window.update_idletasks()
        window.update()
        lbl = [time_label, pwr_label, entry_tm]
        if mode[1] == True:
            p.snake2(
                canv,
                window,
                lbl
            )
        if mode[0] == True:
            p.terracentric(
                canv,
                window,
                lbl,
                ref,
                drw,
                rt
            )
    if frame%1==0:
        if rt[1] == True:
            c.dtm += 1800
        else:
            c.dtm = 0

    frame += 1

