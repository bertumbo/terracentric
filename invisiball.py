import numpy as np
from numpy import cos, sin, array, pi, tan, sqrt, arctan2

dt = 0.01

class Ball:
    def __init__(self, vec):
        ###vec: array([[x,y][v_x, v_y],[a_x, a_y][...])
        self.vec = vec
        self.intersections = array([[]])

    def get_intersections(self):
        o = ortho(self.vec)
        self.intersections = intersect(o, 10)

    def get_heading(self):
        self.heading = intersect(self.vec, 10)

    def calc_step(self):
        self.vec[0] = self.vec[0] + self.vec[1] * dt ###add velocity to position
        self.vec[1] = self.vec[1] + self.vec[2] * dt ###add acceleration to velocity

    def get_reflection(self):
        beta_in = arctan2(self.vec[1],self.vec[0])
        theta_in = arctan2(self.vec[1],self.vec[0])

def rot(vec, ang):
    r_mat = np.array(((cos(ang), -sin(ang),
                       sin(ang),  cos(ang)
                       )))
    vec_n = np.dot(r_mat,np.copy(vec))
    return vec_n

def rotate(vec, ang):
    print("rotating\n")
    v_x, v_y = vec[:]
    # print(vec, v_x, v_y)
    out_vec = array([
        v_x * cos(ang) - v_y * sin(ang),
        v_x * sin(ang) + v_y * cos(ang)
    ], dtype=float)
    # out_vec = vec*rotation_matrix
    print(out_vec)
    return out_vec


def ortho(vec):
    print("getting ortho\n")
    out_vec = np.copy(vec)
    # print("out_vec", out_vec[:1])
    out_vec[1] = rotate(vec[1], pi / 2)
    print(out_vec)
    return out_vec


def intersect(vec, rho):
    print("\nintersecting\n")
    # print("test")
    x, y = vec[0, :]
    v_x, v_y = vec[1, :]
    print(x, y, v_x, v_y)
    a = array(v_x ** 2 + v_y ** 2)
    b = array(2 * (x * v_x + y * v_y))
    c = array(x ** 2 + y ** 2 - rho ** 2)
    p = b / a
    q = c / a
    print(a, b, c)
    # sec_1 = ((-b+sqrt(b**2 - 4*a*c))/2*a)
    # sec_2 = ((-b-sqrt(b**2 - 4*a*c))/2*a)
    sec_1 = (-p / 2 + sqrt((p / 2) ** 2 - q))
    sec_2 = (-p / 2 - sqrt((p / 2) ** 2 - q))
    print(sec_1, sec_2)
    out_arr = array([vec[0] + sec_1 * vec[1], vec[0] + sec_2 * vec[1]], dtype=float)

    if np.isnan(out_arr[0, 0]):
        print("shit, imaginary root, overwriting")
        out_arr = array([[vec[0, 0], vec[0, 1]]], dtype=float)
    print(out_arr)
    return (out_arr)


def tang(vec, rho):
    pass



# m = np.array([[3, 2], [1, 0], [0, 1], [0, 0]], dtype=float)

# for ind in range(1000):
# for dt in [1]:
#     m = np.array([[3, 2], [1, 0], [0, 1], [0, 0]], dtype=float)
#     while True:
#         if m[0, 0] > 20:
#             print(m[0], m[1], m[2], m[3])
#             break
#         m[0] = m[0] + m[1] * dt
#         m[1] = m[1] + m[2] * dt
#         m[3, 0] += dt

# test = array([
#     [1, 3],
#     [-2, 3]
# ])
# print(test)
# print(rotate(test,1/2*pi))
# m = array([
#     [7, 7], [2, 1], [0, 0]
# ], dtype=float)
#print(m)
#o = (ortho(m))
#i = intersect(o, array(10))
# print(m, o, i, sep="\n")

# emil = Ball(m)
# emil.get_intersections()
#
# for intersection in emil.intersections:
#     print(intersection)
#     print(intersection[0])

