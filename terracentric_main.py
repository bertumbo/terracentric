###################
###terracentric####
###by bertumbo#####
###################

import terracentric_functions as f
import terracentric_config as c
import tkinter as tk
import numpy as np
from datetime import datetime

class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side="left", anchor="w"):
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
f.get_led_state()

window = tk.Tk()
width = 800
height = 800
offx = width/2
offy = height/2
sc = 30

entry_tm = tk.Entry()
time_label = tk.Label(text="frame")
time_label2 = tk.Label(text="time")
canv = tk.Canvas(width=width, height=height, bg="#000000")
sld_a = tk.Scale(resolution=0.01,  from_=0, to=2*np.pi, orient="vertical", length=500)
sld_b = tk.Scale(resolution=0.1,  from_=0, to=5, orient="vertical", length=500)
sld_c = tk.Scale(resolution=0.1,  from_=0, to=10, orient="vertical", length=500)
sld_d = tk.Scale(resolution=0.001, from_=-2*np.pi, to=2*np.pi, orient="vertical", length=500)
sld_e = tk.Scale(resolution=1, from_=0, to=255, orient="vertical", length=500)
sld_f = tk.Scale(resolution=1, from_=0, to=360, orient="vertical", length=500)
lng = Checkbar(window, ['r_tm', 'r_theta', 'r_pln_pos', 'r_led', 'r_canv'])


sld_a.set(str(c.a))
sld_b.set(str(c.b))
sld_c.set(str(c.c))
sld_d.set(str(c.d))
sld_e.set(str(c.e))
sld_f.set(str(c.f))

lng.pack(side="top")
time_label.pack(side="top")
time_label2.pack(side="top")
entry_tm.pack(side="top")
canv.pack(side="right")

sld_a.pack(side="left")
sld_b.pack(side="left")
sld_c.pack(side="left")
sld_d.pack(side="left")
sld_e.pack(side="left")
sld_f.pack(side="left")



for led in c.led_array:
    x, y = f.pol2cart(led[4], led[1])
    f.create_circle((x*sc + offx), (-y*sc + offy), 8, canv, col=led[3])

frame = 0
while True:
    if frame%1==0:
        start = datetime.utcnow()
        state = list(lng.state())
        c.a = np.float16(sld_a.get())
        c.b = np.float16(sld_b.get())
        c.c = np.float16(sld_c.get())
        c.d = np.float16(sld_d.get())
        c.e = np.float16(sld_e.get())
        c.f = np.float16(sld_f.get())
        #state = list(lng.state())
        window.update_idletasks()
        window.update()
        f.refresh(state[0], state[1], state[2])
        if state[3]==True:
            f.get_led_state()
        if state[4]==True:
            f.redraw_canvas(canv)
        #time_label.configure(text=str(frame))
        #print(state)
        #print(pln_array, led_array)
        time_label['text'] = str(datetime.fromtimestamp(c.tm))
        time_label2['text'] = str(c.tm)
        #print(state)
        print(state, datetime.utcnow()-start)
    frame += 1

