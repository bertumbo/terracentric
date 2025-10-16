import numpy as np
# import tkinter as tk
import time

def clamp(x):
    return max(0, min(x, 255))


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return(x, y)

radius = 18
scale = 0.5

neighborhood = [
    [-6, -1, 5, 6],
    [-2, -1, 0, 2, 4, 5],
    [-3, -2, 1, 3, 4],
    [-3, 2, 8, 9],
    [1, 2, 3, 5, 7, 8],
    [0, 1, 4, 6, 7],
]

coordinates = [
    (0, 673.0),
    (0, 624.7),
    (0, 562.7),
    (-3, 532.0),
    (-3, 595.1),
    (-3, 651.6)
]

led_color_array = np.zeros(shape=(360, 3), dtype=np.int8)

class LED:
    instances = []

    def __init__(self, neighbors, coords):
        self.ID = len(self.__class__.instances)
        self.__class__.instances.append(self)
        self.neighbors = neighbors
        self.coords = coords
        self.color = led_color_array[self.ID, :]


for i in range(0, 360, 6):
    for j in range(6):
        neighbors = []
        coords = pol2cart(coordinates[j][1] - 90, coordinates[j][0] - i - 90)
        print(coords)
        for neighbor in neighborhood[j]:
            neighbors.append((i + neighbor) % 360)
        LED(neighbors, coords)
        print(i + j)

# root = tk.Tk()
# root.geometry("1000x1000")



# canvas = tk.Canvas(root, width=1000, height=1000, bg="#111111")
# canvas.pack()

# canvas.create_oval(0, 0, 10, 10, outline="#222222", fill="#555555")

# LED.instances[44].color = (50, 50, 50)
led_color_array[44, :] = (50, 50, 50)
led_color_array[89, :] = (255, 10, 80)


light_source = 15
led_color_array[light_source, :] = (255, 255, 255)
source_color = led_color_array[light_source]
for neighbor in LED.instances[light_source].neighbors:
    led_color_array[neighbor, :] = led_color_array[light_source, :] / 2

# def refresh_canvas():
#     canvas.delete("all")
#     for l in LED.instances:
#         print(f"{l.ID}: {l.neighbors}")
#         r, g, b = l.color
#         canvas.create_oval(
#             500 + (l.coords[0] - radius) * scale,
#             500 - (l.coords[1] - radius) * scale,
#             500 + (l.coords[0] + radius) * scale,
#             500 - (l.coords[1] + radius) * scale,
#             outline="#222222",
#             fill="#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
#         )
#     canvas.update()

# "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

# root.update()

# refresh_canvas()

time.sleep(2)

led_color_array[10, :] = (100, 0, 0)

for l in LED.instances:
    print(f"{l.ID}: {l.neighbors}")

# refresh_canvas()

# root.update()

# root.mainloop()
# print(-361 % 4)