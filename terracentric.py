from datetime import datetime
import datetime as dt
from astropy.coordinates import get_body, EarthLocation, solar_system_ephemeris
from astropy.time import Time
import time
import numpy as np
from astral.sun import sun
from astral import LocationInfo
from numpy import pi

longitude = 10 + 55 / 60
latitude = 50 + 41 / 60

print(longitude)
print(latitude)


loc = EarthLocation.from_geodetic(lat=latitude, lon=longitude, height=450)
city = LocationInfo(latitude=latitude, longitude=longitude)

# t = Time(datetime.fromtimestamp(time.time()), format="datetime")

solar_system_ephemeris.set('builtin')


class Clock:
    def __init__(self):
        self.dawn_off = None
        self.sunrise_off = None
        self.noon_off = None
        self.sunset_off = None
        self.dusk_off = None
        self.midnight_off = None
        self.noon_offset = None

        self.sun_events = None

        self.planets = None
        self.planets_axial_angle = None
        self.planets_coord = {}
        self.planets_render_coord = None

        self.sun_offset = None
        self.mars_offset = None
        self.venus_offset = None
        self.mercury_offset = None
        self.moon_offset = None

        self.date = datetime.utcnow()
        self.second_of_day = None
        self.pi_of_day = None

    def get_date(self, time_offset_in_days=0, time_offset_in_seconds=0):
        real_date = datetime.utcnow()
        self.date = real_date + dt.timedelta(days=time_offset_in_days, seconds=time_offset_in_seconds)

    def get_second_of_day(self):
        # self.date = datetime.utcnow()
        self.second_of_day = (datetime.timestamp(self.date) + self.noon_offset) % 86400
        self.pi_of_day = (86400 - self.second_of_day) / 43200 * pi
        # print(f"Date: {self.date}")
        print(f"second of day: {self.second_of_day}")
        print(f"angle: {self.pi_of_day}")
        # pass

    def get_planet_angles(self):
        if self.planets is None:
            self.planets = ["mars", "venus", "mercury", "moon", "jupiter", "saturn"]
        if self.planets_coord is None:
            self.planets_coord = {}
        if self.planets_render_coord is None:
            self.planets_render_coord = {}
        if self.planets_axial_angle is None:
            self.planets_axial_angle = {}

        sun_coord = get_body("sun", Time(self.date), loc)
        # print(sun_coord)
        self.sun_offset = np.deg2rad(sun_coord.ra.value)

        self.planets_axial_angle.update({"sun": np.deg2rad(sun_coord.dec.value)})
        self.planets_coord.update({"sun": 0})
        self.planets_render_coord.update({"sun": self.pi_of_day})

        for planet in self.planets:
            body = get_body(planet, Time(self.date), loc)
            angle = (np.deg2rad(body.ra.value) - self.sun_offset)
            dec_angle = np.deg2rad(body.dec.value)
            render_coord = angle + self.pi_of_day

            # cleaning angles
            if angle >= 2 * pi:
                angle -= 2 * pi
            elif angle < 0:
                angle += 2 * pi
            if render_coord >= 2 * pi:
                render_coord -= 2 * pi
            elif render_coord < 0:
                render_coord -= 2 * pi

            self.planets_axial_angle.update({planet: dec_angle})
            self.planets_coord.update({planet: angle})
            self.planets_render_coord.update({planet: render_coord})

        # print(f"relative planet coordinates: \n{self.planets_coord}")
        # print(f"planet render angle: \n{self.planets_render_coord}")


    def get_sun_event(self):
        midnight_date = dt.datetime(self.date.year, self.date.month, self.date.day, 0, 0, 0, 0)
        event_directory = sun(city.observer, date=midnight_date)

        dawn = datetime.timestamp(event_directory["dawn"])
        sunrise = datetime.timestamp(event_directory["sunrise"])
        noon = datetime.timestamp(event_directory["noon"])
        sunset = datetime.timestamp(event_directory["sunset"])
        dusk = datetime.timestamp(event_directory["dusk"])

        self.noon_offset = 43200 - noon % 86400

        self.dawn_off = (dawn + self.noon_offset) % 86400  # / 43200 * pi
        self.sunrise_off = (sunrise + self.noon_offset) % 86400  # / 43200 * pi
        self.noon_off = (noon + self.noon_offset) % 86400  # / 43200 * pi
        self.sunset_off = (sunset + self.noon_offset) % 86400  # / 43200 * pi
        self.dusk_off = (dusk + self.noon_offset) % 86400  # / 43200 * pi
        self.midnight_off = 0  # / 43200 * pi

        self.sun_events = {
            "midnight": (86400 - self.midnight_off) / 43200 * pi,
            "dawn": (86400 - self.dawn_off) / 43200 * pi,
            "sunrise": (86400 - self.sunrise_off) / 43200 * pi,
            "noon": (86400 - self.noon_off) / 43200 * pi,
            "sunset": (86400 - self.sunset_off) / 43200 * pi,
            "dusk": (86400 - self.dusk_off) / 43200 * pi
        }

        # print(self.sun_events)


if __name__ == "__main__":
    alex = Clock()
    alex.get_date()
    alex.get_sun_event()
    alex.get_second_of_day()
    alex.get_planet_angles()

    i = 0
    while True:
        alex.get_date(time_offset_in_seconds=i*0)
        alex.get_sun_event()
        alex.get_second_of_day()
        alex.get_planet_angles()

        output = {}
        output.update(alex.sun_events)
        output.update(alex.planets_render_coord)
        print(f"date: {alex.date}")
        print(f"output: {output}")
        print(f"decline: {alex.planets_axial_angle}")

        i += 1

        time.sleep(1)

# print(time.time())
