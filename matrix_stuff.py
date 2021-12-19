import numpy as np


class Ball:
    instances = []
    def __init__(self, vec, clr):
        self.__class__.instances.append(self)
        ###vec: array([[x,y][v_x, v_y],[a_x, a_y][...])
        self.vec = vec
        self.dist = radial_distance(self.vec)
        self.clr = clr
        self.ind = 0
        self.cooldown = False

    def get_ortho_intersections(self):
        self.intersections = intersect(ortho(self.vec), 10)[self.ind]

    def get_reflection(self):
        self.dist = radial_distance(self.vec)
        print(self.dist)
        for distance in self.dist:
            if distance >= 11:
                if self.cooldown == False:
                    self.vec = reflect(self.vec)
                    self.cooldown = True
            else:
                self.cooldown = False




        #self.vec = reflect(self.vec)






def root():
    pass


def rotate(vec, phi):
    c = np.cos(phi)
    s = np.sin(phi)
    vec_n = np.copy(vec)
    rot = np.array(
        [[c, -s],
         [s, c]]
    )
    vec_n[:, 1] = np.dot(vec[:, 1], np.swapaxes(rot, 0, 1))
    return vec_n


def ortho(vec):
    return rotate(vec, np.pi / 2)


def ortho_intersect(vec, rho):
    intersects = intersect(ortho(vec), rho)
    #print(intersects)
    return intersects


def intersect(vec, rho):
    vec_n = np.zeros((np.shape(vec)[0], 2, 2), dtype=float)
    for vec_sub, vec_n_sub in zip(vec, vec_n):
        x, y = vec_sub[0, :]
        v_x, v_y = vec_sub[1, :]
        a = v_x ** 2 + v_y ** 2
        p = (2 * (x * v_x + y * v_y)) / a
        q = (x ** 2 + y ** 2 - rho ** 2) / a
        t_1 = (-p / 2 + np.sqrt((p / 2) ** 2 - q))
        t_2 = (-p / 2 - np.sqrt((p / 2) ** 2 - q))
        trans = np.array([
            [1, t_1],
            [1, t_2]
        ])
        #print(trans)
        vec_n_sub[:] = np.dot(trans, np.mat(vec_sub[:2]))
    if np.isnan(vec_n[0,0,0]):
        vec_n = np.zeros((np.shape(vec)[0], 1, 2), dtype=float)
        vec_n[:] = vec[:,0]

    print(vec_n)
    return vec_n

def reflect(vec):
    vec_n = np.copy(vec)
    for vec_sub, vec_n_sub in zip(vec, vec_n):
        x, y = vec_sub[0, :]
        v_x, v_y = vec_sub[1, :]
        dbeta = np.pi + 2*np.arctan2(y,x) - 2*np.arctan2(v_y, v_x)
        print(dbeta, np.arctan2(y,x), np.arctan2(v_y, v_x))
        c = np.cos(dbeta)
        s = np.sin(dbeta)

        rot = np.array(
            [[c, -s],
             [s, c]]
        )

        vec_n_sub[1] = np.dot(vec_sub[1], np.swapaxes(rot, 0, 1))
    return vec_n


def radial_distance(vec):
    vec_n = np.zeros((np.shape(vec)[0]))
    vec_n[:] = np.sqrt(vec[:, 0, 0] ** 2 + vec[:, 0, 1] ** 2)
    return vec_n


def radial_angle(vec):
    vec_safe = np.copy(vec)
    vec_n = np.zeros((np.shape(vec_safe)[0]))
    vec_n[:] = np.tan(vec_safe[:, 0, 1], vec_safe[:, 0, 0])
    return vec_n


def calc_step(vec, dt):
    vec_n = np.zeros((np.shape(vec)))
    trans = np.array([
        [1, dt, dt ** 2],
        [0, 1, dt],
        [0, 0, 1]
    ])
    for vec_sub, vec_n_sub in zip(vec, vec_n):
        vec_n_sub[:] = np.dot(trans, np.mat(vec_sub[:]))
    return vec_n

#
# m = np.array(
#     [[[10, 10],
#       [1, 1],
#       [0, 0]],
#      [[0, 10],
#       [1, 1],
#       [0, 0]],
#      [[-5, 5],
#       [-1, 1],
#       [0, 0]],
#      ], dtype=float
# )

m = np.array(
    [
     [[10, 0],
      [3, 1],
      [2, 0]],
     ], dtype=float
)

print(m)
#print(rotate(m, np.pi / 2))
# print(m)
# print(m[1])
# print(rot
# n = np.zeros((3, 4, 2))
# print(n)
#print("shape\n", np.shape(m))
#print("intersect\n", intersect(m, 5))
#print("ortho\n", ortho(m))
#print("ortho_intersect\n", ortho_intersect(m, 5))
# print("radial_dist\n", radial_distance(m))
# print("radial_angle\n", radial_angle(m))
print(ortho_intersect(m, 10))
#print(radial_angle(m)[0])
print(reflect(m))
#print(m)
#print(calc_step(m, 0.1))

