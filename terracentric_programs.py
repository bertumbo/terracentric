import terracentric_functions as f
import terracentric_config as c
from random import randint
import numpy as np
import time
from datetime import datetime

def random_canv(
        canv,
        window,
        label):
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