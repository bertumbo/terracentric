# coding: utf-8
"""
====================================
Planetary Controller
====================================

The purpose of this demo is to demonstrate the ability of sunpy
to get the position of planetary bodies im the solar system.
"""


from astropy.coordinates import SkyCoord
from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
from astropy.coordinates import get_moon
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import numpy as np
import math as m
import random
import time
import datetime
from astral.sun import sun
from astral import LocationInfo


colors2 = {
    "moon":[255, 255, 0],
    "sun":[252, 212, 64],
    "mercury":[206, 204, 209],
    "venus":[248,226,176],
    "earth":[59, 93, 56],
    "mars":[193,68,14],
    "jupiter":[227,220,203],
    "saturn":[206,184,184],
    "uranus":[213, 251, 252],
    "neptune":[62, 102, 249]
}
colors2 = {
    "moon":[255, 0, 0],
    "sun":[255, 0, 0],
    "mercury":[255,0,0],
    "venus":[255, 0, 0],
    "earth":[255, 0, 0],
    "mars":[255, 0, 0],
    "jupiter":[255, 0, 0],
    "saturn":[255, 0, 0],
    "uranus":[255, 0, 0],
    "neptune":[255, 0, 0]
}

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

planet_list = [
    #"moon",
    'sun',
    'mercury',
    'venus',
    'earth',
    'mars',
    'jupiter',
    "saturn",
    'uranus',
    'neptune'
    ]

imList = []

class Center:
    def __init__(self, name, timestamp):
        self.name = name
        t = datetime.datetime.fromtimestamp(timestamp)
        t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
        coord = get_body_heliographic_stonyhurst(self.name, time=t)
        self.cr = coord.radius.value
        self.cphi = np.deg2rad(coord.lon.value)
        self.cx, self.cy = pol2cart(self.cr, self.cphi)

    def refresh_position(self, timestamp):
        t = datetime.datetime.fromtimestamp(timestamp)
        t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
        coord = get_body_heliographic_stonyhurst(self.name, time=t)
        self.cr = coord.radius.value
        self.cphi = np.deg2rad(coord.lon.value)
        self.cx, self.cy = pol2cart(self.cr, self.cphi)

class Satellite:
    instances = []
    def __init__(self, name = "empty", r = 0, phi = 0, timestamp = time.time()):
        self.name = name
        self.__class__.instances.append(self)
        #self.r = r
        #self.phi = phi

        #self.x, self.y = pol2cart(r, phi)

        ###colors###
        self.ir = random.randint(0, 255)
        self.ig = random.randint(0, 255)
        self.ib = random.randint(0, 255)
        if self.name in colors:
            color = colors[self.name]
            self.ir = color[0]
            self.ig = color[1]
            self.ib = color[2]

        self.refresh_position(timestamp)

        print("created Satellite:", self.name, self.r, self.phi, self.x, self.y)


    def refresh_position(self, timestamp):

        t = datetime.datetime.fromtimestamp(timestamp)
        t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
        t = t[:-3]
        t = Time(t)
        #print(t, obstime)
        moon = get_moon(time=t)

        coord = get_body_heliographic_stonyhurst(self.name, time=t)
        #print(coord.lon.value)
        self.r = moon.distance.value
        self.r = 10
        self.phi = np.deg2rad(moon.ra.value)
        self.x, self.y = pol2cart(self.r, self.phi)



        #Satellite("moon", 10, np.deg2rad(moon.ra.value))

class Planet:
    instances = []
    def __init__(self, name = "empty", r = 0, phi = 0, timestamp = time.time()):
        self.name = name
        self.__class__.instances.append(self)

        self.refresh_position(timestamp)

        #if self.r > 10000:
        #    self.r = self.r/1,496e+8

        self.ir = random.randint(0,255)
        self.ig = random.randint(0,255)
        self.ib = random.randint(0,255)
        if self.name in colors:
            color = colors[self.name]
            self.ir = color[0]
            self.ig = color[1]
            self.ib = color[2]
        #self.r, self.g, self.b = random.randint(0,255),random.randint(0,255),random.randint(0,255)

        print("created Planet:", self.name, self.r, self.phi, self.x, self.y)

    def refresh_position(self, timestamp):

        t = datetime.datetime.fromtimestamp(timestamp)
        t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')

        coord = get_body_heliographic_stonyhurst(self.name, time=t)

        self.r = coord.radius.value
        self.phi = np.deg2rad(coord.lon.value)
        self.x, self.y = pol2cart(self.r, self.phi)

        self.center = True
        if self.name != center:
            self.cx, self.cy = self.x - center.cx, self.y - center.cy
            self.cphi = np.arctan2(self.cy, self.cx)
            self.cr, self.cphi = cart2pol(self.cx, self.cy)
            self.center = False
            pass
        else:
            self.cx = 0
            self.cy = 0
            self.cr = 0
            self.cphi = 0
        pass


    def set_center(self):
        #print("me:", self.name, "setting myself to center")
        self.center = True
        for planet in self.__class__.instances:
            if planet != self:
                planet.cx, planet.cy = planet.x - self.x, planet.y - self.y
                planet.cphi = np.arctan2(planet.cy, planet.cx)
                planet.cr, planet.cphi = cart2pol(planet.cx, planet.cy)
                planet.cphi = planet.cphi
                #print(planet.name, planet.cx, planet.cy, planet.cphi)
                planet.center = False
                pass
            else:
                planet.cx = 0
                planet.cy = 0
                planet.cr = 0
                planet.cphi = 0

class Marker:
    instances = []
    def __init__(self, name = "empty", timestamp = time.time()):
        self.name = name
        self.__class__.instances.append(self)

        self.refresh_position(timestamp)


        self.ir = random.randint(0,255)
        self.ig = random.randint(0,255)
        self.ib = random.randint(0,255)
        if self.name in colors:
            color = colors[self.name]
            self.ir = color[0]
            self.ig = color[1]
            self.ib = color[2]
        #self.r, self.g, self.b = random.randint(0,255),random.randint(0,255),random.randint(0,255)

        print("created Marker:", self.name, self.r, self.phi)

    def refresh_position(self, timestamp):
        self.r = 10
        #noonphi = calculate_theta(timestamp)
        self.phi = calculate_theta_extended(timestamp, self.name)

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
        try:
            self.init_blender()
        except:
            print("did not init blender")
        print("created LED:", self.ID, self.IDD)
        pass

    def init_blender(self):
        x,y = pol2cart(self.r, self.phi)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(x, y, 0),
                                        rotation=(0, 0, self.phi), scale=(1, 1, 1))

        self.ob = bpy.context.active_object
        self.ob.name = self.IDD

        self.mat = bpy.data.materials.new(self.IDD)
        #self.mat.name = "enormepisse"

    def check_state(self, timestamp = time.time(), theta = 0):
        self.intensity = 0
        self.ir, self.ig, self.ib = 0,0,0
        #theta = m.pi/2
        #theta = calculate_theta(timestamp)
        for planet in Planet.instances:
            #if planet.center == False:
            if planet.name != center.name:

                #print(self.ID, "checking", planet.name, "not yet")
                #dphi = ((self.phi-planet.cphi)%(2*m.pi))
                #dphi = abs(self.phi - planet.cphi)%(2*m.pi)
                #print(planet.name, dphi)
                #if dphi < (m.pi/4):
                #val = int(25)
                #val = int(min(255, (255 / dphi ** 2) * 0.005))
                #self.intensity += abs(val)

                x1, y1 = pol2cart(self.r, self.phi)
                x2, y2 = pol2cart(10, planet.cphi + theta)
                dx = x1-x2
                dy = y1-y2
                r = np.sqrt(dx**2 + dy**2)

                if r < 500:
                    # print(this_planet, r2)
                    # color = int(255)
                    if r == 0:
                        self.ir, self.ig, self.ib = 255, 255, 255

                    val = int(min(255, (255 / r ** 2)*0.1))
                    self.intensity += val
                    self.ir = self.ir + (val * planet.ir/255)
                    self.ig = self.ig + (val * planet.ig/255)
                    self.ib = self.ib + (val * planet.ib/255)

        for satellite in Satellite.instances:

            x1, y1 = pol2cart(self.r, self.phi)
            x2, y2 = pol2cart(10, satellite.phi + theta)
            dx = x1 - x2
            dy = y1 - y2
            r = np.sqrt(dx ** 2 + dy ** 2)

            if r < 500:
                val = int(min(255, (255 / r ** 2) * 0.1))
                #self.intensity += val
                self.ir = self.ir + (val * satellite.ir / 255)
                self.ig = self.ig + (val * satellite.ig / 255)
                self.ib = self.ib + (val * satellite.ib / 255)

        for marker in Marker.instances:
            deltaphi = (self.phi - marker.phi)%(2*m.pi)

            deltaphi2 = min(deltaphi, 2*m.pi-deltaphi)
            #print(self.ID, marker.name, deltaphi)
            if abs(deltaphi2) < 0.03:
                val = int(min(255, (255 / abs(deltaphi2) ** 2) * 0.1))
                val = int(min(255, (255 / abs(deltaphi2) ** 2) * 3))
                self.ir = self.ir + (val * marker.ir / 255)
                self.ig = self.ig + (val * marker.ig / 255)
                self.ib = self.ib + (val * marker.ib / 255)



def draw_fig(timestamp = time.time()):
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

    theta = calculate_theta(timestamp)

    for led in LED.instances:
        #led.check_state()

        x, y = pol2cart(led.r, led.phi)
        draw.regular_polygon(bounding_circle=((x*sc + offx), (y*sc + offy), 8), n_sides=4, rotation=-np.rad2deg(led.phi),fill=(int(led.ir), int(led.ig), int(led.ib)), outline=None)
        #draw.regular_polygon(bounding_circle=(x * sc + offx, y * sc + offy, 4), n_sides=4, rotation=-np.rad2deg(led.phi), fill=(led.intensity, 0,0), outline=None)

    for planet in Planet.instances:
        x, y = pol2cart(15, planet.cphi + theta)
        color = (planet.ir, planet.ig, planet.ib)
        if planet.center != True:
            draw.ellipse((x*sc2 + offx - si, y*sc2 + offy- si, x*sc2 + offx+ si, y*sc2 + offy + si),
                     fill=color, outline="blue")


    for satellite in Satellite.instances:
        x, y = pol2cart(15, satellite.phi + theta)
        draw.ellipse((x*sc2 + offx - si, y*sc2 + offy- si, x*sc2 + offx+ si, y*sc2 + offy + si),
                     fill="green", outline="blue")

#    for marker in Marker.instances:
#        x, y

    t = datetime.datetime.fromtimestamp(timestamp)
    t = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
    t = t[:-3]
    t = Time(t)

    draw.text((10, 10), str(t), fill=(255, 255, 255, 128))
    #img.show()
    imList.append(img)

def calculate_theta(timestamp):
    city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=datetime.date.fromtimestamp(timestamp))
    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = datetime.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()

    theta_0 = noontime / 86400 * 2 * m.pi
    t = timestamp % 86400
    theta_1 = t / 86400 * 2 * m.pi
    theta = -(theta_0 - theta_1) + m.pi/2


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

def set_as_center(name):
    for planet in Planet.instances:
        if planet.name == name:
            planet.set_center()
            break

def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = m.sqrt(XsqPlusYsq + z**2)               # r
    elev = m.atan2(z,m.sqrt(XsqPlusYsq))     # theta
    az = m.atan2(y,x)                           # phi
    return r, elev, az

def cart2sphA(pts):
    return np.array([cart2sph(x,y,z) for x,y,z in pts])

def appendSpherical(xyz):
    np.hstack((xyz, cart2sphA(xyz)))

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)




###setup
t = time.time()

center = Center("earth", t)

for planet in planet_list:
    Planet(name = planet, timestamp = t)

Satellite("moon", t)

Marker("sunrise", t)
Marker("sunset", t)
Marker("noon", t)

#for dist in [9, 9.5, 10, 10.5, 11]:
for dist in [10, 10.5, 11]:
    for deg in range(0, 360, int(360/120)):
        rad = np.deg2rad(deg)
        LED(dist, rad)


###main
for i in range(365):
    starttime = time.time()
    print("start iteration:", i)
    #t = time.time()+i*1*60*60*0.01
    t = time.time()+i*(1*60*60*24 + 1*60*60*24/365)
    #t = time.time() + i * (1 * 60 * 60 * 24)
    #t = time.time()+1*60*60*0.5 - 13*60*60 + 45*60
    theta = calculate_theta(t)

    center.refresh_position(t)

    for planet in Planet.instances:
        planet.refresh_position(t)

    for satellite in Satellite.instances:
        satellite.refresh_position(t)

    for marker in Marker.instances:
        marker.refresh_position(t)

    for led in LED.instances:
        led.check_state(t, theta)
    draw_fig(t)

    endtime = time.time() - starttime
    print("end iteration, lasted:", endtime)


###finish
name = "testfull"
filename = "%s.gif" % name
out = imList[0].save(filename, save_all=True, append_images=imList[1:], optimize=True, duration=30, loop=0)


###test
'''
city = LocationInfo("Ilmenau", "Germany", "Europe/Ilmenau", 50 + 41 / 60, 10 + 55 / 60)
    s = sun(city.observer, date=datetime.date.fromtimestamp(timestamp))
    noon = time.strptime(s["noon"].strftime("%H:%M:%S").split(',')[0], '%H:%M:%S')
    noontime = datetime.timedelta(hours=noon.tm_hour, minutes=noon.tm_min, seconds=noon.tm_sec).total_seconds()
'''

print(calculate_theta_extended(time.time(), "sunrise"))
print(calculate_theta_extended(time.time(), "noon"))
print(calculate_theta_extended(time.time(), "sunset"))