###functions###


import time
import datetime as dt
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation, get_body
from astral.sun import sun
from astral import LocationInfo

import numpy as np
import terracentric_config as c

def init_blender(led_array):
    mat_list = []
    for led in led_array:
        x, y = pol2cart(led[4], led[1])
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(x, y, 0),
                                        rotation=(0, 0, led[4]), scale=(0.2, 0.2, 0.2))

        ob = bpy.context.active_object
        ob.name = led[0]
        ob_name = led[0]

        mat_name = led[0]
        #self.mat_name = mat_name

        mat = bpy.data.materials.get(mat_name) or bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        #self.mat = mat

        try:
            mat.node_tree.nodes.remove(
                mat.node_tree.nodes.get('Principled BSDF'))  # title of the existing node when materials.new
        except:
            pass
        mat_output = mat.node_tree.nodes.get('Material Output')
        diffuse = mat.node_tree.nodes.new('ShaderNodeEmission')  # name of diffuse BSDF when added with shift+A

        diffuse.inputs['Color'].default_value = (1, 0, 0, 1)  # last value alpha

        # link diffuse shader to material
        mat.node_tree.links.new(mat_output.inputs[0], diffuse.outputs[0])

        # set activer material to your new material
        bpy.context.object.active_material = mat

def refresh_blender(self, led_array):
    for led in led_array:
        ob = bpy.data.objects.get(led[0])
        mat = bpy.data.materials.get(led[0])

        mat_output = mat.node_tree.nodes.get('Material Output')
        diffuse = mat.node_tree.nodes.new('ShaderNodeEmission')  # name of diffuse BSDF when added with shift+A

        diffuse.inputs['Color'].default_value = (255 / 255, 255 / 255, 255 / 255, 1)  # last value alpha
        diffuse.inputs['Strength'].default_value = 15
        # link diffuse shader to material
        mat.node_tree.links.new(mat_output.inputs[0], diffuse.outputs[0])

        # set activer material to your new material
        bpy.context.object.active_material = mat

def get_sun_event(timestamp, event):
    #city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    city = LocationInfo(latitude=50 + 41 / 60, longitude=10 + 55 / 60)
    sn = sun(city.observer, date=dt.date.fromtimestamp(timestamp))
    event_time = time.strptime(sn[event].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    event_time_seconds = dt.timedelta(
        hours=event_time.tm_hour,
        minutes=event_time.tm_min,
        seconds=event_time.tm_sec
    ).total_seconds()
    return event_time_seconds


def get_tm():
    st = datetime.utcnow()
    c.tm = datetime.timestamp(st) + c.dtm
    return


def calc_theta(timestamp):
    # city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    # s = sun(city.observer, date=dt.date.fromtimestamp(timestamp))
    t = timestamp % 86400

    # noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    # noontime = dt.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()
    noontime = get_sun_event(timestamp, "noon")
    c.theta = 2*np.pi * (((-t + noontime)/86400)+1/4)

    return


def get_pln_pos(timestamp, pln_array):
    # this returns planets location from planet_list @ timestamp in a numpy array as observed from earth

    t = Time(dt.datetime.fromtimestamp(timestamp), format="datetime")
    loc = EarthLocation.from_geodetic(lon=50 + 41 / 60, lat=10 + 55 / 60, height=450)

    with solar_system_ephemeris.set('builtin'):  #'builtin' or 'de432s' or 'de430s'
        for pln in pln_array:
            pln_coord = get_body(pln[0], t, loc)
            pln[1] = np.deg2rad(pln_coord.ra.value)
            # print("halllllllllo", pln_coord.ra.value)

    pln_array[:, 1] = (pln_array[:, 1] - pln_array[0, 1]) % (2*np.pi)
    return

def get_mrk_pos(timestamp, mrk_array):
    noontime = get_sun_event(timestamp, "noon")
    for mrk in mrk_array:
        secs = get_sun_event(timestamp, mrk[0])
        mrk[1] = 2*np.pi * (((-secs + noontime)/86400)+1/4)
    pass


def refresh(r_tm, r_theta, r_pln_pos):
    if r_tm == True:
        get_tm()
    if r_theta == True:
        calc_theta(timestamp=c.tm)
    if r_pln_pos == True:
        get_pln_pos(timestamp=c.tm, pln_array=c.pln_array)
    if True:
        get_mrk_pos(timestamp=c.tm, mrk_array=c.mrk_array)

def smallest_angle(phi1, phi2):
    phi_d = ((phi1 - phi2) % (2 * np.pi))
    phi_d_m = min(phi_d, 2 * np.pi - phi_d)
    return phi_d_m

def get_val(phi1, phi2, phase1, phase2, s0):
    phi_d = ((phi1 - phi2) % (2 * np.pi))
    phi_d_m = min(phi_d, 2 * np.pi - phi_d)
    if phi_d_m < c.a:
        d_now = (2 * c.d - np.pi) % (2 * np.pi) - np.pi
        val = v(phi_d_m, ((phase1*phase2) * d_now), s0)
    else:
        val = 0
    return val

def get_led_state(drw_pln, drw_mrk):
    s0 = s(0)
    sum_led = np.array((0, 0, 0), dtype="float32")
    # sum_led = np.array((0, 0, 0), dtype="int")

    for led in c.led_array:
        sum_led = sum_led*0

        if drw_pln == True:
            for pln in c.pln_array:
                val = get_val(pln[1] + c.theta,led[1], pln[2],led[2], s0)
                if val != 0:
                    sum_led += pln[3] * val

        if drw_mrk == True:
            for mrk in c.mrk_array:
                val = get_val(mrk[1], led[1], mrk[2], led[2], s0)
                if val != 0:
                    sum_led += mrk[3] * val


        #led[3] = sum_led
        led[3] = np.clip(sum_led, 0, 255)
    return

def led_limiter(led_array, lmt): #deprecated
    pwr_array = np.array((0,0,0), dtype="float32")
    for led in led_array:
        pwr_array += led[3]/255*0.02
    pwr = np.sum(pwr_array)
    if pwr > lmt:
        fac = lmt/pwr
        for led in led_array:
            led[3] = led[3]*fac
    else:
        fac=1
    return (pwr, fac)

def get_ltd_array(led_array, lmt):
    pwr_array = np.array((0, 0, 0), dtype="float32")
    ltd_array = np.copy(led_array)
    for led in led_array:
        pwr_array += led[3] / 255 * 0.02
    pwr = np.sum(pwr_array)
    c.pwr = pwr
    if pwr > lmt:
        fac = lmt / pwr
    else:
        fac = 1
    for led, ltd_led in zip(led_array, ltd_array):
        ltd_led[3] = led[3] * fac
        #ltd_led[3] = np.ndarray(led[3] * fac, dtype="int")
        #print(ltd_led[3])
    c.fac = fac
    c.ltd_array = (np.copy(ltd_array))
    #c.ltd_array = c.ltd_array[3].astype("int")
    #print(c.ltd_array)
    #c.ltd_array.astype(int)
    #c.ltd_array = np.ndarray.astype(ltd_array, "int")
    return ltd_array

def redraw_canvas(canv, led_array):

    width = 800
    height = 800
    offx = width / 2
    offy = height / 2
    sc = 30
    #get_led_state()
    canv.delete("all")
    for led in led_array:
        x, y = pol2cart(led[4], led[1])
        create_circle((x * sc + offx), (-y * sc + offy), 8, canv, col=led[3])

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def smallestSignedAngleBetween(x, y):
    a = (x - y) % (2*np.pi)
    b = (y - x) % (2*np.pi)
    return -a if a < b else b

def ind2nm(ind, n_max):
    (m, n) = divmod(ind, n_max)
    return n, m

def nm2ind(n, m, n_max):
    ind = n+m*n_max
    return ind


def create_circle(x, y, r, canvasName, col): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    #print(int(col[0]), int(col[1]), int(col[2]))
    return canvasName.create_oval(x0, y0, x1, y1, fill='#%02x%02x%02x' % (int(col[0]), int(col[1]), int(col[2])))

# def z(x):
#
#     #print("x, z", x, z)
#     return z

def s(x):
    z = 4 * abs(x / c.a) ** c.c - c.b
    s = np.tanh(z)
    return s

def l(x, s0):
    z = 4 * abs(x / c.a) ** c.c - c.b
    s = np.tanh(z)
    l = np.clip(((s+s0)/2*s0), 0, 1)
    return l

def v(x, phase, s0):
    if x <= 0:
        val = c.e*l(x-phase, s0)
    else:
        val = c.e*l(x+phase, s0)
        #print("val", val)
    return val

