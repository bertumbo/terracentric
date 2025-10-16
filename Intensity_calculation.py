import numpy as np
import math
import sys

np.set_printoptions(linewidth=3000, threshold=sys.maxsize)

i = np.zeros(shape=3)
i_0 = np.zeros(shape=3)
sigma = np.zeros(shape=3)

r_s = 1
theta_s = np.radians(90)
r_p = 0
theta_p = 0

i_0[:] = (1, 1, 1)
sigma[:] = (0.3, 0.61, 1)

angular = np.linspace(0, 2*np.pi, 120)
radial = np.array([0, 0.218, 0.447, 0.657, 0.848, 1])

led_position_array = np.zeros(shape=(360, 2), dtype=float)

led_color_array = np.zeros(shape=(360, 3), dtype=np.int16)

cols = 3
rows = 120

for row in range(rows):
    angle = angular[row]
    for col in range(cols):
        if row % 2 == 0:
            radius = radial[5 - 2 * col]
        else:
            radius = radial[2 * col]
        led_position_array[row * 3 + col, :] = (angle, radius)
print(led_position_array)


def calculate_smallest_angle(angle1, angle2):
    # Calculate the absolute difference
    difference = abs(angle1 - angle2)

    # Adjust if the difference is greater than pi (180 degrees)
    if difference > math.pi:
        difference = 2 * math.pi - difference

    return difference

def calculate_exponential_intensity(r_s, theta_s, r_p, theta_p):
    c = abs((r_p + r_s) / 2) / 2
    d = calculate_smallest_angle(theta_s, theta_p)
    i_1 = i_0 * np.e**(-sigma * c * d)

    return i_1

def calculate_intensity(r_s, theta_s, r_p, theta_p):
    # calculating the integral of vertical density
    # rho = abs((r_p - r_p**2/2) - (r_s - r_s**2/2))
    rho = abs((r_p + r_s)/2)/2

    # calculating the integral of horizontal density
    delta_theta = calculate_smallest_angle(theta_s, theta_p)

    # multiplying density factors
    intensity_decrease = 2/np.pi * rho * delta_theta

    print(r_s, r_p, theta_s, theta_p, rho, delta_theta, intensity_decrease)

    return intensity_decrease

for index, led in enumerate(led_position_array):
    # delta_i = calculate_intensity(r_s, theta_s, led[1], led[0])
    # delta_theta = calculate_smallest_angle(theta_s, led[0])
    # i[:] = i_0 * (1 - sigma * delta_i)

    i[:] = calculate_exponential_intensity(r_s, theta_s, led[1], led[0])

    # scattered_part = abs(np.sin(delta_theta)) * sigma
    # through_part = abs(np.cos(delta_theta)) * (1 - sigma)

    scattered_part = 1 - np.cos(theta_)

    # led_color_array[index, :] = (i * (scattered_part + through_part) * 255)
    led_color_array[index, :] = i[:] * 255

print(np.vstack((np.array(range(360)), led_color_array.T)))

# delta_i = calculate_intensity(r_s, theta_s, r_p, theta_p)
#
# delta_theta = calculate_smallest_angle(theta_s, theta_p)
#
# # print(i_0 * (1 - (sigma * delta_i)))
#
# i[:] = i_0 * (1 - (sigma * delta_i))
#
# scattered_part = np.sin(delta_theta) * sigma
# through_part = np.cos(delta_theta) * (1 - sigma)
#
# rescat = i * (scattered_part + through_part)
#
#
# print(i)
#
# print(scattered_part, through_part)
# print(rescat)



# i[:] = i_0[:] * ((1, 1, 1) - delta_i * sigma[:])