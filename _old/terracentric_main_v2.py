
##import statements
import numpy as np
import PIL

##classes
class String:
    def __init__(self):
        pass

class LED_Array:
    def __init__(self, rows=120, columns=3):

        # read and create variables
        self.rows = rows
        self.columns = columns
        self.led_polar_position_array = np.ones(shape=(rows, columns, 2))
        self.led_raw_rgb_array = 255*np.ones(shape=(rows, columns, 3))
        self.led_out_rgb_array = 255*np.ones(shape=(rows, columns, 3), dtype = "int32")
        self.led_xy_position_array = np.ones(shape=(rows, columns, 2))

        # maybe variables, constant atm
        self.power_limit = 5
        self.phi_array = np.linspace(2*np.pi + np.pi/2, np.pi/2, num=rows, endpoint=False)
        self.radius_array = np.linspace(10, 11, num=columns, endpoint=True)

        # operative variables
        self.current_power = 0

        # create (semi-)permanent arrays
        for ind, radius in enumerate(self.radius_array):
            self.led_polar_position_array[:, ind, 0] = radius
        for ind, phi in enumerate(self.phi_array):
            self.led_polar_position_array[ind, :, 1] = phi
        for row in range(self.rows):
            for column in range(self.columns):
                self.led_xy_position_array[row, column] = pol2cart(self.led_polar_position_array[row, column, 0], self.led_polar_position_array[row, column, 1])


    def get_output_rgb_array(self, safety_mode=True):

        self.led_out_rgb_array[:, :, :] = np.clip(self.led_raw_rgb_array[:, :, :], 0, 255)
        self.current_power = np.sum(self.led_out_rgb_array)/255*0.02

        if safety_mode == True:
            power_coefficient = self.power_limit / self.current_power
            rgb = self.led_out_rgb_array * power_coefficient
            self.led_out_rgb_array = np.rint(rgb)

    def print(self):
        ## print some things, mainly for debuggin and stuff
        #print(self.phi_array, self.radius_array)
        #print(self.led_polar_position_array)
        print(self.led_raw_rgb_array)
        print(self.led_out_rgb_array, self.current_power)
        #print(self.led_xy_position_array)
        #print(self.led_pos_array, self.led_rgb_array)


    def wipe(self):
        # short command for setting all rgb values to 0
        #print("test", self.led_raw_rgb_array[:, :])
        self.led_raw_rgb_array[:, :] = self.led_raw_rgb_array[:, :]*0
        #self.led_raw_rgb_array = np.rint(self.led_raw_rgb_array*0)

    def print_to_canvas(self, canv):
        ## print led_rgb_array to canvas
        width = 1024
        height = 1024
        offx = width / 2
        offy = height / 2
        sc = 40
        canv.delete("all")
        for row in range(self.rows):
            for column in range(self.columns):
                x, y = self.led_xy_position_array[row, column]
                x_true, y_true = x * sc + offx, -y * sc + offy
                create_circle(x_true, y_true, 8, canv, col=(self.led_out_rgb_array[row, column]).astype(int))
                # canv.create_text((x_true, y_true) ,fill="red",font="Times 8 italic",
                #         text=f"{row} {column}")
##functions
def create_circle(x, y, r, canvasName, col): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    #print(int(col[0]), int(col[1]), int(col[2]))
    return canvasName.create_oval(x0, y0, x1, y1, fill='#%02x%02x%02x' % ((col[0]), (col[1]), (col[2])))


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

##Test
if __name__ == "__main__":
    led_array = LED_Array()
    led_array.print()
    led_array.wipe()
    led_array.get_output_rgb_array(safety_mode=False)
    led_array.print()
    #redraw_canvas()

    print(led_array.led_raw_rgb_array[1])
    print(led_array.led_polar_position_array[1])


