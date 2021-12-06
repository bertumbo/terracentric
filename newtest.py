import numpy as np
import planets_re1 as p
import time
from datetime import datetime
import tkinter as tk

cfg={"a": 1.0, "b": -2.0, "c": 100.0, "d": 0.03, "e": 0, "f": 360}
theta_buffed = 0
state = [0,0,0,0]

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

def between(lowcut, value, highcut):

    end_value = max(lowcut, value)
    end_value = min(highcut, end_value)
    return end_value

def get_led_state(disable_calculate_theta = False, disable_get_pln_pos = False, timestamp=time.time(), pln_array=np.array((1,1)), led_array=np.array((1,1)), mode = "radial"):
    global theta_buffed
    if disable_calculate_theta == False:
        theta = p.calculate_theta2(timestamp=timestamp)
        theta_buffed = theta
    else:
        theta = theta_buffed
    if disable_get_pln_pos == False:
        p.get_pln_pos2(timestamp=timestamp, pln_array=pln_array)

    if state[3] == False:
        mode = "radial"
    else:
        mode = "xy"

    if mode == "radial":
        for led in led_array:
            sum_led = np.array((0, 0, 0), dtype=float)
            for pln in pln_array:
                phi_d = ((pln[1] - led[1] + theta) % (2 * np.pi))
                phi_d_m = min(phi_d, 2 * np.pi - phi_d)
                if phi_d_m <= (cfg["f"]/360*2*np.pi):
                    val = ((cfg["a"]*(phi_d_m + (pln[2] + led[2])*cfg["d"]) ** (cfg["b"])) / cfg["c"])
                    val = np.float16(between(0, val, 1))
                    sum_led += pln[3] * val

            led[3] = sum_led
            for ind in range(len(led[3])):
                led[3][ind] = between(0, led[3][ind], 255)
            if np.sum(led[3]) <= 3*cfg["e"]:
                led[3] = np.array((0, 0, 0), dtype=float)

    if mode == "xy":
        for led in led_array:
            sum_led = np.array((0, 0, 0), dtype=float)
            for pln in pln_array:
                x1, y1 = p.pol2cart(10, pln[1]+theta)
                x2, y2 = p.pol2cart(led[4], led[1])
                dx = x1 - x2
                dy = y1 - y2
                r = np.sqrt(dx ** 2 + dy ** 2)
                val = (cfg["a"] * r ** (cfg["b"])) / cfg["c"]
                val = np.float16(between(0, val, 1))

                sum_led += pln[3] * val
            led[3] = sum_led
            for ind in range(len(led[3])):
                led[3][ind] = between(0, led[3][ind], 255)
    return

def redraw_canvas(canv = "dummy", disable_calculate_theta = False, disable_get_pln_pos = False, timestamp=time.time(), realtime = False, pln_array=np.array((1,1)), led_array=np.array((1,1))):
    global entry_tm, entry_a, entry_b, entry_c, entry_d
    if realtime == True:
        start = datetime.utcnow()
        tm = datetime.timestamp(start)
        entry_tm.delete(0, "end")
        entry_tm.insert(0, tm)
    else:
        #tm = timestamp
        tm = float(entry_tm.get())

    #timestamp = float(entry_tm.get())
    # cfg["a"] = float(entry_a.get())
    # cfg["b"] = float(entry_b.get())
    # cfg["c"] = float(entry_c.get())
    # cfg["d"] = float(entry_d.get())

    cfg["a"] = np.float16(sld_a.get())
    cfg["b"] = np.float16(sld_b.get())
    cfg["c"] = np.float16(sld_c.get())
    cfg["d"] = np.float16(sld_d.get())
    cfg["e"] = np.float16(sld_e.get())
    cfg["f"] = np.float16(sld_f.get())

    get_led_state(disable_calculate_theta=disable_calculate_theta, disable_get_pln_pos=disable_get_pln_pos, timestamp=tm, pln_array=pln_array, led_array=led_array)
    canv.delete("all")
    for led in led_array:
        x, y = p.pol2cart(led[4], led[1])
        create_circle((x * sc + offx), (-y * sc + offy), 8, canv, col=led[3])


def create_circle(x, y, r, canvasName, col): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    #print(int(col[0]), int(col[1]), int(col[2]))
    return canvasName.create_oval(x0, y0, x1, y1, fill='#%02x%02x%02x' % (int(col[0]), int(col[1]), int(col[2])))


n_LED = 120
m_LED = 4
imList = []

led_array = np.zeros((n_LED*m_LED, 5), dtype=object)
key = {0: 9.5, 1: 10, 2: 10.5, 3: 9.0}
    #### [led ,   phi, phase, (r, g, b), rho]
for m in range(m_LED):
    for n in range(n_LED):
        ind = n+m*n_LED
        led_array[ind, 0] = "LED" + str(ind).zfill(4)
        led_array[ind, 1] = 2*np.pi*(n/n_LED)
        led_array[ind, 2] = 2*np.pi*(m/m_LED)
        led_array[ind, 3] = np.array((0,0,0))
        led_array[ind, 4] = key[m]

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
        ["neptune",   0, 0, np.array(( 43,  64, 255))]
    ],
    dtype=object,
)



start = datetime.utcnow()
timestamp = datetime.timestamp(start)#+60*60*10

get_led_state(timestamp=timestamp, pln_array=pln_array, led_array=led_array)
get_led_state(disable_get_pln_pos=True, timestamp=timestamp, pln_array=pln_array, led_array=led_array)
#p.draw_fig2(timestamp=timestamp, led_array=led_array, imList=imList)



window = tk.Tk()
width = 800
height = 800
offx = width/2
offy = height/2
sc = 30
canv = tk.Canvas(width=width, height=height, bg="#000000")


for led in led_array:
    x, y = p.pol2cart(led[4], led[1])
    create_circle((x*sc + offx), (-y*sc + offy), 8, canv, col=led[3])


button = tk.Button(
    text="Click me!",
    width=10,
    height=1,
    bg="blue",
    fg="yellow",
    command=lambda: redraw_canvas(
        canv=canv, disable_get_pln_pos=False, timestamp=0, pln_array=pln_array, led_array=led_array)
)
button.pack()

entry_tm = tk.Entry()
entry_a = tk.Entry()
entry_b = tk.Entry()
entry_c = tk.Entry()
entry_d = tk.Entry()
time_label = tk.Label(text="frame")

sld_a = tk.Scale(resolution=0.1,  from_=0, to=100, orient="vertical", length=500)
sld_b = tk.Scale(resolution=0.1,  from_=-5, to=5, orient="vertical", length=500)
sld_c = tk.Scale(resolution=0.1,  from_=0, to=500, orient="vertical", length=500)
sld_d = tk.Scale(resolution=0.001, from_=-0.1, to=1, orient="vertical", length=500)
sld_e = tk.Scale(resolution=1, from_=0, to=255, orient="vertical", length=500)
sld_f = tk.Scale(resolution=1, from_=0, to=360, orient="vertical", length=500)
#sld_e = tk.Scale(resolution=0.1, orient="vertical", length=500)

lng = Checkbar(window, ['calc_theta', 'get_pln_pos', 'realtime', 'xy'])

start = datetime.utcnow()
timestamp = datetime.timestamp(start)
entry_tm.insert(0, string=str(timestamp))
entry_a.insert(0, str(cfg["a"]))
entry_b.insert(0, str(cfg["b"]))
entry_c.insert(0, str(cfg["c"]))
entry_d.insert(0, str(cfg["d"]))

sld_a.set(str(cfg["a"]))
sld_b.set(str(cfg["b"]))
sld_c.set(str(cfg["c"]))
sld_d.set(str(cfg["d"]))
sld_e.set(str(cfg["e"]))
sld_f.set(str(cfg["f"]))
#

lng.pack(side="top")
canv.pack(side="right")
time_label.pack(side="top")
entry_tm.pack()

#entry_a.pack(side="bottom")
#entry_b.pack(side="bottom")
#entry_c.pack(side="bottom")
#entry_d.pack(side="bottom")

sld_f.pack(side="left")
sld_e.pack(side="left")
sld_d.pack(side="left")
sld_c.pack(side="left")
sld_b.pack(side="left")
sld_a.pack(side="left")
#sld_e.pack(side="left")



#lng.pack(side="left",  fill="x")


frame = 0
while True:
    if frame%1==0:
        state = list(lng.state())
        window.update_idletasks()
        window.update()
        time_label.configure(text=str(frame))
        print(state)
        #print(pln_array, led_array)
    if frame%1==0:
        redraw_canvas(
            canv=canv,
            disable_calculate_theta=not state[0],
            disable_get_pln_pos=not state[1],
            realtime=state[2],
            timestamp=time.time(),
            pln_array=pln_array,
            led_array=led_array
        )

    frame += 1
    #time.sleep(1/60)



window.mainloop()