import numpy as np
from matplotlib import pyplot as plt
import time

class Mandlebrot:
    def __init__(self,height=1000,width=1000):
        self.height = height
        self.width = width
        self.data = np.zeros( (self.width,self.height,3), dtype=np.uint8 )

    def transform(self,x,y):
        """Transformes from height,width to -2->2."""
        return (x*4./self.width-2.,y*4./self.height-2.)

    def test(self,x,y,iterations=10):
        zx = 0.
        zy = 0.

        scaling = 255./iterations

        for i in range(iterations):
            if zx*zx + zy*zy > 2*2:
                return [i*scaling,i*scaling,i*scaling]

            xtemp = zx*zx - zy*zy + x
            zy = 2*zx*zy + y
            zx = xtemp

        return [255,255,255]

    def calculate(self,iterations=10):
        for i in range(self.width):
            for j in range(self.height):
                x,y = self.transform(i,j)
                self.data[i,j] = self.test(x,y,iterations=iterations)

    def show(self):
        plt.imshow(self.data, interpolation='nearest')
        plt.show()

m = Mandlebrot()
begin = time.time()
m.calculate(iterations=100)
print "Total time: " + str(time.time()-begin)
m.show()
