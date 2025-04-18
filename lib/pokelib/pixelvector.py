import numpy as np
import matplotlib.pyplot as plt
from pokelib import ExPokeLibError, ExPokeNoHomeError, ExPokeLibFatal

class PixelVector():
    def __init__(self, phone, x_start, x_end, y_start, y_end, step, title = "none"):
        self.phone = phone
        # print("Init PixelVector")
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.step = step
        self.title = title
        self.x_data = []
        self.y_data = []
        self.len = 0
        self.update()
        
    def update(self):
        i = 0
        self.x_data = [] 
        self.y_data = []
        if self.x_start == self.x_end: # vertical
            for y in range(self.y_start, self.y_end, self.step):
                # print(self.phone.getRGB(self.x_start, y))
                self.y_data.append(self.phone.getRGB(self.x_start, y))
                self.x_data.append(y)
            self.len = self.y_end - self.y_start
            print("Length = {}",self.len)
        elif self.y_start == self.y_end: # horizontal
            for x in range(self.x_start, self.x_end, self.step):
                self.y_data.append(self.phone.getRGB(x, self.y_start))
                self.x_data.append(x)
            self.len = self.x_end - self.x_start
            print("Length = {}".format(self.len))
        else:
            print("Only vertical and horizontal supported")
            raise ExPokeLibFatal("Only vertical and horizontal supported")

    def x_set(self, xs, xe):
        self.x_start = xs
        self.x_end   = xe

    def y_set(self, ys, ye):
        self.y_start = ys
        self.y_end   = ye
          
    def set_step(self, s):
        self.step = s

    def x_start(self):
        return self.x_start
    def x_end(self):
        return self.x_end
    def y_start(self):
        return self.y_start
    def y_end(self):
        return self.y_end
        
        
    def plot_start(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r.-', label='Live Data')
        
    def rgb(self):
        return self.x_data, self.y_data
    
    def red(self):
        return self.x_data, list(map(lambda tup: tup[0], self.y_data))
       
    def green(self):
        return self.x_data, list(map(lambda tup: tup[1], self.y_data))

    def blue(self):
        return self.x_data, list(map(lambda tup: tup[2], self.y_data))
        
    def max_delta(self):
        rgbt = np.array(self.rgb()[1])
        return np.min(np.array(np.diff(rgbt, axis=0)), axis = 0)
    
    def max_blue(self):
        return max(self.blue()[1])
    
    def get_maxima(self, threshold=80):
        delta = np.diff(v.red()[1])
        maxima = (np.abs(delta) > threshold).sum()
        return maxima

