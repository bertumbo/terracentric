import terracentric_functions as f
import terracentric_config as c
from random import randint
import numpy as np
import time
from datetime import datetime

def invisiball():
    pass

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