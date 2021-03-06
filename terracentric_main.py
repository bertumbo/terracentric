'''
====================================
terracentric
====================================
'''
__author__ = "umberto"
__version__ = "0.1"

import terracentric_functions as f  #common functions of terracentric clock
import terracentric_config as c     #configuration of terracentric clock
import terracentric_programs as p   #programs
import terracentric_main_v2 as f2
import invisiball
import rattlesnake
import tkinter as tk
import numpy as np
from datetime import datetime
import time
from PIL import ImageGrab

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

def refresh_input():
    #refreshes checkboxes and slider values
    global ref, drw, rt, mode
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

def save_led_array(led_array):
    #output = np.copy(led_array)
    #output = np.delete(output, [0, 1, 2, 4], 1)
    output = np.zeros(shape=(np.shape(led_array)[0], 3))
    for output_led, led in zip(output, led_array):
        rgb = led[3]
        output_led[:] = rgb[:]
    output = np.rint(output)
    print(output)
    np.savetxt("foo.csv", output, delimiter=",")

def getter(widget):
    # x=window.winfo_rootx()+widget.winfo_x()
    # y=window.winfo_rooty()+widget.winfo_y()
    # #x1=x+widget.winfo_width()
    # x1 = x+width
    # #y1=y+widget.winfo_height()
    # y1 = y+height
    # ImageGrab.grab().crop((x,y,x1,y1)).save("output.bmp")
    my_data = np.genfromtxt('foo.csv', delimiter=',')
    print(my_data)

#tkinter stuff, initialisation...

window = tk.Tk()
wtf = tk.Frame()
window.title("terracentric gui ;)")

width = 1024
height = 1024
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

entry_tm = tk.Entry()
time_label = tk.Label(text="frame", height=3)
pwr_label = tk.Label(text="pwr", height=4)
canv = tk.Canvas(width=width, height=height, bg="#000000")
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
button = tk.Button(master=window, text='save canvas as png', command= lambda: getter(canv))
button2 = tk.Button(master=window, text='save ltd_array as csv', command= lambda: save_led_array(c.led_array))

sld_a.set(str(c.a))
sld_b.set(str(c.b))
sld_c.set(str(c.c))
sld_d.set(str(c.d))
sld_e.set(str(c.e))
sld_f.set(str(c.f))

canv.pack(side="right")

p2.add(lng)
p2.add(lng2)
p2.add(lng3)
p2.add(lng4)
p2.add(time_label)
p2.add(entry_tm)
p2.add(pwr_label)
p2.add(button)
p2.add(button2)

p3.add(sld_a)
p3.add(sld_b)
p3.add(sld_c)
p3.add(sld_d)
p3.add(sld_e)


entry_tm.insert(0, str(datetime.fromtimestamp(c.tm)))

lbl = [time_label, pwr_label, entry_tm]

#p.invisiball(canv, window)
#p.snake2(canv, window, pwr_label)

'''=====================setup========================'''

#rattlesnake.Snake2()
#rattlesnake.Player()
#p.invisiball_init()
#Ball()

led_array_new = f2.LED_Array()


frame = 0
while True:
    '''==================mainloop==================='''
    if frame%1==0:  #do every frame
        led_array_new.print()
        refresh_input()
        start = datetime.utcnow()

        #p.sample_program(canv, window, lbl)
        # p.invisiball(
        #     canv,
        #     window
        # )

        led_array_new.wipe()
        led_array_new.led_raw_rgb_array[1, 1] = 600, 122, 100
        led_array_new.led_raw_rgb_array[:, 1] = 500, 122, 300
        led_array_new.led_raw_rgb_array[1, :] = 0, 400, 400
        led_array_new.print_to_canvas(canv)
        led_array_new.get_output_rgb_array()


        if mode[1] == True:
            # p.rattlesnake(
            #     canv,
            #     window,
            #     lbl
            # )
            p.text2(canv, window, led_array_new)
            #quit()
        if mode[0] == True:
            p.terracentric(
                canv,
                window,
                lbl,
                ref,
                drw,
                rt
            )
            if rt[1] == True:
                c.dtm += 60*60*24
            else:
                c.dtm = 0



        window.update_idletasks()
        window.update()

    frame += 1

