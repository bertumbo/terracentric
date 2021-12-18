import terracentric_functions as f
import terracentric_config as c
# from invisiball import Ball
from matrix_stuff import Ball, calc_step
from random import randint
import numpy as np
import time
from datetime import datetime

def invisiball(
        canv,
        window
):
    clr_m = np.array([255, 0, 0])
    clr_n = np.array([0, 255, 0])
    m = np.array([[[1, 0], [1, 1], [0, 0]]], dtype=float)
    n = np.array([[[3, 3], [0, 1], [0, 1]]], dtype=float)
    Ball(m, clr_m)
    #Ball(n, clr_n)



    while True:
        for bal in Ball.instances:
            bal.get_ortho_intersections()
            bal.get_reflection()


            c.led_array[:, 3] = c.led_array[:, 3] * 0
            for led in c.led_array:
                for sec in bal.intersections:
                    x1, y1 = sec[:]
                    x2, y2 = f.pol2cart(led[4], led[1])
                    dx = x1-x2
                    dy = y1-y2
                    rad = np.sqrt(dx**2 + dy**2)
                    if rad < 1:
                        pass
                        led[3] = bal.clr

        f.get_ltd_array(c.led_array, c.limit)
        f.redraw_canvas(canv, c.ltd_array)
        window.update_idletasks()
        window.update()

        bal.vec = calc_step(bal.vec, 0.1)

def snake(
        canv,
        window,
        label
):
    c.led_array[:, 3] = c.led_array[:, 3] * 0
    for ind in range(360):
        pass
        #
        if ind > 0:
            pass
            #c.led_array[ind - 1, 3] = np.array((0, 0, 0), dtype="float32")
        c.led_array[ind, 3] += np.array((255, 0, 0), dtype="float32")
        # c.led_array[: ,3] = np.array(0,0,0)
        # c.led_array[ind ,3] = np.array((255,0,0))
        # f.refresh(True, True, True)
        f.get_ltd_array(c.led_array, c.limit)
        f.redraw_canvas(canv, c.ltd_array)
        label['text'] = "pwr: " + str(np.float16(c.pwr)) \
                        + "\nfac: " + str(np.float16(c.fac)) \
                        + "\nltd_pwr: " + str(np.float16(c.pwr * c.fac))

        window.update_idletasks()
        window.update()
        time.sleep(0.01)


def random_canv(
        canv,
        window,
        label):
    for led in c.led_array:
        led[3] = led[3] * 0
    while True:
        rnd = randint(0, 359)
        c.led_array[rnd][3] = np.array((randint(0, 255), randint(0, 255), randint(0, 255)))
        # f.led_limiter(c.led_array, c.limit)
        f.get_ltd_array(c.led_array, c.limit)
        f.redraw_canvas(canv, c.ltd_array)
        label['text'] = "pwr: " + str(np.float16(c.pwr)) \
                            + "\nfac: " + str(np.float16(c.fac)) \
                            + "\nltd_pwr: " + str(np.float16(c.pwr * c.fac))
        window.update_idletasks()
        window.update()
        time.sleep(0.01)

def terracentric(
        canv,
        window,
        lbl,
        ref,
        drw,
        rt
):
    f.refresh(ref[0], ref[1], ref[2])
    if rt[0] == False:
        try:
            c.tm = datetime.timestamp(
                             datetime.fromisoformat(lbl[2].get())
                         )
            f.calc_theta(c.tm)
        except: pass
    f.get_led_state(drw[1], drw[2])
    f.get_ltd_array(c.led_array, c.limit)
    f.redraw_canvas(canv, c.ltd_array)
    lbl[0]['text'] = "dt: "+str(datetime.fromtimestamp(c.tm))+"\ntm: "+str(c.tm)
    lbl[1]['text'] = "pwr: " + str(np.float16(c.pwr)) + "\nfac: " + str(np.float16(c.fac))+ "\nltd_pwr: " + str(np.float16(c.pwr * c.fac))
    window.update_idletasks()
    window.update()