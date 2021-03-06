import terracentric_functions as f
import terracentric_config as c
# from invisiball import Ball
from rattlesnake import Snake2, Player
from matrix_stuff import Ball, calc_step
from random import randint
import numpy as np
import time
from datetime import datetime


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
    #window.update_idletasks()
    #window.update()

def invisiball_init():
    clr_m = np.array([255, 0, 0])
    clr_n = np.array([0, 255, 0])
    m = np.array([[[1, 3], [1, 4], [0, 0]]], dtype=float)
    n = np.array([[[0, 3], [1, 0.1], [0, 0]]], dtype=float)
    Ball(m, clr_m)
    Ball(n, clr_n)

def invisiball(
        canv,
        window
):
    def init():

        clr_m = np.array([255, 0, 0])
        clr_n = np.array([0, 255, 0])
        m = np.array([[[1, 3], [1, 4], [0, 0]]], dtype=float)
        n = np.array([[[0, 3], [1, 0.1], [0, 0]]], dtype=float)
        Ball(m, clr_m)
        Ball(n, clr_n)


    #while True:
    c.led_array[:, 3] = c.led_array[:, 3] * 0
    for bal in Ball.instances:
        bal.get_ortho_intersections()
        bal.get_reflection()

        for led in c.led_array:
            for sec in bal.intersections:
                x1, y1 = sec[:]
                x2, y2 = f.pol2cart(led[4], led[1])
                dx = x1-x2
                dy = y1-y2
                rad = np.sqrt(dx**2 + dy**2)
                if rad < 1:
                    pass
                    led[3] += bal.clr
        bal.vec = calc_step(bal.vec, 0.1)
    f.get_ltd_array(c.led_array, c.limit)
    f.redraw_canvas(canv, c.ltd_array)
        #window.update_idletasks()
        #window.update()


def rattlesnake(
        canv,
        window,
        lbl):

    #Snake()
    #Player()
    #while True:
        #c.theta = 0
        s0 = f.s(0)
        sum_led = np.array((0, 0, 0), dtype="float32")

        for led in c.led_array:
            sum_led = sum_led * 0

            for snake in Snake2.instances:
                #print(snake.segments)
                for ind, seg in zip(range(len(snake.segments)),snake.segments):
                    dif = f.smallest_angle(seg[0], seg[1])
                    if (f.smallest_angle(seg[0], led[1]) <= dif) and (f.smallest_angle(seg[1], led[1]) <= dif):
                        val = 1/(ind+1)**2
                    else:
                        val = 0
                    #val = f.get_val(snk, led[1], 0, led[2], s0)
                    if val != 0:
                        #if seg[2] == True:
                        if snake.activity == "red":
                            sum_led += np.array([60,20,50])* val
                        if snake.activity == "green":
                            sum_led += np.array([0, 60, 10]) * val
                        if snake.activity == "halfgreen":
                            if ind == 0:
                                sum_led += np.array([0, 60, 10]) * val
                            else:
                                sum_led += np.array([60, 60, 10]) * val
                        # else:
                        #     sum_led += np.array([0, 60, 10]) * val
            led[3] = np.clip(sum_led, 0, 255)

        for snake in Snake2.instances:
            # if randint(0,100) > 80:
            #     snake.active = True
            # else:
            #     snake.active = False
            snake.calc_step()


            lbl[0]['text'] = str(snake.timer)
        f.get_ltd_array(c.led_array, c.limit)
        f.redraw_canvas(canv, c.ltd_array)



        lbl[1]['text'] = "pwr: " + str(np.float16(c.pwr)) + "\nfac: " + str(np.float16(c.fac)) + "\nltd_pwr: " + str(np.float16(c.pwr * c.fac))
        #window.update_idletasks()
        #window.update()
        #time.sleep(0.01)


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
        #window.update_idletasks()
        #window.update()
        time.sleep(0.01)

def sample_program(
        canv,
        window,
        lbl):
    #activates random led with random value

    for led in c.led_array:
        led[3] = led[3]*0       #wipes every led
    index = randint(0, 359)
    chosen_led = c.led_array[index] #selects one led from array by index
    chosen_led[3] = np.array([255,0,0]) #changes rgb value of chosen led, [3] corresponds to color of led
    other_index = f.nm2ind(n=115, m=2, n_max=120) #gets index from row = n and column = m
    other_chosen_led = c.led_array[other_index]
    other_chosen_led[3] = np.array([0,255,0])
    f.get_ltd_array(c.led_array, c.limit) #manipulates led_array, so that maximum power never exceeds power limit
    f.redraw_canvas(canv, c.ltd_array) #draws limited led array on gui's canvas

    lbl[0]['text'] = "dt: " + str(datetime.fromtimestamp(c.tm)) + "\ntm: " + str(c.tm)
    lbl[1]['text'] = "pwr: " + str(np.float16(c.pwr)) + "\nfac: " + str(np.float16(c.fac)) + "\nltd_pwr: " + str(
        np.float16(c.pwr * c.fac))

def new_sample_program(
        canv,
        window,
        led_obj
):
    for row in range(led_obj.rows):
        for column in range(led_obj.columns):
            #led_obj.wipe()
            led_obj.led_raw_rgb_array[row, column] = 255, 200, 100
            led_obj.get_output_rgb_array(safety_mode=True)
            led_obj.print_to_canvas(canv)
            window.update_idletasks()
            window.update()
            #time.sleep(1)

def loading(
        canv,
        window,
        led_obj
):
    led_obj.wipe()
    for row in range(led_obj.rows):
        led_obj.wipe()
        for column in range(led_obj.columns):
            # led_obj.wipe()
            led_obj.led_raw_rgb_array[row, column] = 255, 200, 100

        led_obj.get_output_rgb_array(safety_mode=False)
        led_obj.print_to_canvas(canv)
        window.update_idletasks()
        window.update()
            # time.sleep(1)

def text(
        canv,
        window,
        led_obj
):
    led_obj.wipe()
    letter_dictionary = {}
    letter_list = []
    letter_dictionary["T"] = (255 * np.array([
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))
    letter_dictionary["T"] = (255 * np.array([
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))
    letter_list.append(255*np.array([
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))
    letter_list.append(255 * np.array([
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))
    letter_list.append(255 * np.array([
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))
    letter_list.append(255 * np.array([
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    ]))

    letter_list.append(np.array((0, 0, 255))*np.array(([
        [[1], [1], [1]],
        [[1], [1], [1]],
        [[0], [1], [0]],

    ])))
    letter_dictionary["T"] = (np.array((0, 0, 255))*np.array(([
        [[0], [1], [0]],
        [[0], [1], [0]],
        [[0], [1], [0]],
        [[0], [1], [0]],
        [[1], [1], [1]],
    ])))
    letter_dictionary["Y"] = (np.array((0, 0, 255)) * np.array(([
        [[0], [1], [0]],
        [[0], [1], [0]],
        [[1], [1], [1]],
        [[1], [0], [1]],
        [[1], [0], [1]],
    ])))


    letter_list.append(letter_dictionary["T"])
    letter_list.append(letter_dictionary["Y"])

    for ind_letter, letter in enumerate(letter_list):
        for row in range(letter.shape[0]):
            for column in range(letter.shape[1]):
                led_obj.led_raw_rgb_array[row + 6 * ind_letter, column] = letter[row, column]


    led_obj.get_output_rgb_array(safety_mode=False)
    led_obj.print_to_canvas(canv)
    window.update_idletasks()
    window.update()
            # time.sleep(1)

def text2(
        canv,
        window,
        led_obj
):
    led_obj.wipe()
    import terracentric_cryptix as cr

    char0 = cr.generate_letter_list("terracentric")

    offset_row = 0
    offset_column = 0

    for i in range(100):
        led_obj.wipe()

        text_array = cr.generate_array_from_letter_list(char0, i % 100)
        n_rows = text_array.shape[0]
        for row in range(n_rows):
            for column in range(text_array.shape[1]):
                led_obj.led_raw_rgb_array[(row + offset_row - int((n_rows - 1) / 2)) % led_obj.rows, (column + offset_column) % led_obj.columns] \
                    = text_array[row, column]

        led_obj.get_output_rgb_array(safety_mode=False)
        led_obj.print_to_canvas(canv)
        window.update_idletasks()
        window.update()
        time.sleep(0.01)

