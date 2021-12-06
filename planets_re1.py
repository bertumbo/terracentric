

###import section
import time
import datetime
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
import numpy as np
import math as m
from astral.sun import sun
from astral import LocationInfo
from PIL import Image, ImageDraw


planet_list = [
    'sun',
    "moon",
    'mercury',
    # 'earth',
    'venus',
    'mars',
    'jupiter',
    "saturn",
    'uranus',
    'neptune'
    ]

colors = {
    "moon":[182, 182, 182],
    "sun":[255, 212, 60],
    "mercury":[198,153,86],
    "venus":[255, 185, 185],
    "earth":[255, 0, 0],
    "mars":[203, 50, 50],
    "jupiter":[212, 197, 157],
    "saturn":[255, 0, 0],
    "uranus":[81, 180, 255],
    "neptune":[43, 64, 255],

    "sunrise":[255, 0, 0],
    "sunset":[0,0,255]
}

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def between(lowcut, value, highcut):

    end_value = max(lowcut, value)
    end_value = min(highcut, end_value)
    return end_value

def get_pln_pos(timestamp = time.time()):
    # this returns planets location from planet_list @ timestamp in a numpy array as observed from earth

    t = Time(datetime.datetime.fromtimestamp(timestamp), format="datetime")
    loc = EarthLocation.from_geodetic(lon=50 + 41 / 60, lat=10 + 55 / 60, height=450)

    with solar_system_ephemeris.set('de432s'):  #'builtin' or 'de432s' or 'de430s'
        pln_matrix = np.zeros([len(planet_list), 3])
        for ind, pln in zip(range(len(pln_matrix)), planet_list):
            pln_coord = get_body(pln, t, loc)
            pln_matrix[ind] = [
                pln_coord.distance.value,
                pln_coord.ra.value,
                pln_coord.dec.value
            ]
    #theta = calculate_theta(timestamp)
    #pln_matrix[:,1] = (pln_matrix[:,1] - pln_matrix[0,1] + theta)%360
    pln_matrix[:, 1] = (pln_matrix[:, 1] - pln_matrix[0, 1]) % 360
    #print(pln_matrix)
    return pln_matrix

def get_pln_pos2(timestamp = time.time(), pln_array = np.array((1,1))):
    # this returns planets location from planet_list @ timestamp in a numpy array as observed from earth

    t = Time(datetime.datetime.fromtimestamp(timestamp), format="datetime")
    loc = EarthLocation.from_geodetic(lon=50 + 41 / 60, lat=10 + 55 / 60, height=450)

    with solar_system_ephemeris.set('de432s'):  #'builtin' or 'de432s' or 'de430s'
        for pln in pln_array:
            pln_coord = get_body(pln[0], t, loc)
            pln[1] = np.deg2rad(pln_coord.ra.value)
            print("halllllllllo", pln_coord.ra.value)

    pln_array[:, 1] = (pln_array[:, 1] - pln_array[0, 1]) % (2*np.pi)
    #theta = calculate_theta(timestamp)
    #pln_matrix[:,1] = (pln_matrix[:,1] - pln_matrix[0,1] + theta)%360
    #pln_matrix[:, 1] = (pln_matrix[:, 1] - pln_matrix[0, 1]) % 360
    #print(pln_matrix)
    return

def calculate_theta(timestamp):
    city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=datetime.date.fromtimestamp(timestamp))
    t = timestamp % 86400
    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = datetime.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()

    theta = 360/86400*(noontime-t)+90
    #theta = 0

    return theta

def calculate_theta2(timestamp):
    city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=datetime.date.fromtimestamp(timestamp))
    t = timestamp % 86400
    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = datetime.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()

    theta = 2*np.pi * (((-t + noontime)/86400)+1/4)
    #theta = 0

    return theta

def calculate_theta_extended(timestamp, name):
    city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=datetime.date.fromtimestamp(timestamp))

    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = datetime.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()

    s_time = time.strptime(s[name].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    sunrisetime = datetime.timedelta(hours=s_time.tm_hour, minutes=s_time.tm_min, seconds=s_time.tm_sec).total_seconds()

    theta_0 = (sunrisetime-noontime) / 86400 * 2 * m.pi
    #t = timestamp % 86400
    theta_1 = 0
    theta =  (theta_0 - theta_1) - m.pi/2

    return theta

def draw_fig(timestamp = time.time(), imList = []):
    width = 1000
    height = 1000
    img = Image.new('RGB', (width, height), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img, "RGB")
    draw.line((500, 0, 500, 1000), width=1, fill=(10, 10, 10, 255))
    draw.line((0, 500, 1000, 500), width=1, fill=(10, 10, 10, 255))

    sc = 30
    sc2 = 15
    si = 5
    offx = width/2
    offy = height/2

    t = datetime.datetime.utcfromtimestamp(timestamp)
    t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
    t = t[:-3]
    t = Time(t)

    draw.text((10, 10), str(t), fill=(255, 255, 255, 128))

    for led in LED.instances:

        x, y = pol2cart(led.r, led.phi)
        draw.regular_polygon(bounding_circle=((x*sc + offx), (-y*sc + offy), 8), n_sides=4, rotation=np.rad2deg(led.phi),fill=(int(led.ir), int(led.ig), int(led.ib)), outline=None)
    imList.append(img)
    #img.show()

def draw_fig2(timestamp = time.time(), led_array = np.array((1,1)), imList = []):
    width = 1000
    height = 1000
    img = Image.new('RGB', (width, height), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img, "RGB")
    draw.line((500, 0, 500, 1000), width=1, fill=(10, 10, 10, 255))
    draw.line((0, 500, 1000, 500), width=1, fill=(10, 10, 10, 255))

    sc = 30
    sc2 = 15
    si = 5
    offx = width/2
    offy = height/2

    t = datetime.datetime.utcfromtimestamp(timestamp)
    t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
    t = t[:-3]
    t = Time(t)

    draw.text((10, 10), str(t), fill=(255, 255, 255, 128))

    for led in led_array:

        x, y = pol2cart(led[4], led[1])
        #print(led[1])
        draw.regular_polygon(bounding_circle=((x*sc + offx), (-y*sc + offy), 8), n_sides=4, rotation=np.rad2deg(led[1]),fill=(int(led[3][0]), int(led[3][1]), int(led[3][2])), outline=None)
    imList.append(img)
    img.show()

class LED:
    instances = []
    def __init__(self, r, phi):
        self.ID = len(self.__class__.instances)
        self.IDD = str(self.ID).zfill(4)
        self.__class__.instances.append(self)
        self.phi = phi
        self.r = r
        self.intensity = 0
        self.ir = 0
        self.ig = 0
        self.ib = 0
        print("created LED:", self.IDD)

    def check_state(self, pln_array, theta):
        self.intensity = 0
        self.ir, self.ig, self.ib = 0,0,0

        for ind_pln, coord in zip(range(len(pln_array)), pln_array):

            x1, y1 = pol2cart(self.r, self.phi)
            x2, y2 = pol2cart(10, np.deg2rad(pln_array[ind_pln, 1]+theta))
            dx = x1-x2
            dy = y1-y2
            r = np.sqrt(dx**2 + dy**2)

            color = colors[planet_list[ind_pln]]

            if r < 2:

                # print(this_planet, r2)
                # color = int(255)
                if r == 0:
                    self.ir, self.ig, self.ib = 255, 255, 255

                val = int(min(255, (255 / r ** 2)*0.1))
                self.intensity += val
                self.ir = self.ir + (val * color[0]/255)
                self.ig = self.ig + (val * color[1]/255)
                self.ib = self.ib + (val * color[2]/255)