import time
import datetime as dt
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation, get_body
from astral.sun import sun
from astral import LocationInfo

import numpy as np

def get_pln_pos(timestamp, pln_array):
    # this returns planets location from planet_list @ timestamp in a numpy array as observed from earth

    t = Time(dt.datetime.fromtimestamp(timestamp), format="datetime")
    loc = EarthLocation.from_geodetic(lon=50 + 41 / 60, lat=10 + 55 / 60, height=450)

    with solar_system_ephemeris.set('builtin'):  #'builtin' or 'de432s' or 'de430s'
        for pln in pln_array:
            pln_coord = get_body(pln[0], t, loc)
            pln[1] = np.deg2rad(pln_coord.ra.value)
            print("halllllllllo", pln_coord.ra.value)

    pln_array[:, 1] = (pln_array[:, 1] - pln_array[0, 1]) % (2*np.pi)
    return

def calc_theta(timestamp):
    city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=dt.date.fromtimestamp(timestamp))
    t = timestamp % 86400
    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = dt.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()

    theta = 2*np.pi * (((-t + noontime)/86400)+1/4)

    return theta

def get_tm():
    st = datetime.utcnow()
    tm = datetime.timestamp(st)
    return tm

def get_led_state(disable_calc_theta, disable_get_pln_pos, timestamp, pln_array, led_array):
    global theta_buffed
    if disable_calc_theta == False:
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

    return


