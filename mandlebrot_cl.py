import pyopencl as cl
import numpy
import time
import Tkinter
from PIL import Image, ImageTk

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        
        self.w = 1000
        self.h = 1000

        self.pressed = False
        self.rectangle = None

        self.x0 = -2
        self.y0 = -2
        self.x1 = 2
        self.y1 = 2

        self.fig = None

    def loadProgram(self,filename):
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        self.program = cl.Program(self.ctx, fstr).build()
    def run(self,x0,y0,x1,y1):
        mf = cl.mem_flags

        #initialize client side (CPU) arrays
        self.params = numpy.array([self.w,self.h,x0,y0,x1,y1], dtype=numpy.float32)
        self.c = numpy.zeros([self.h*self.w],dtype=numpy.float32)

        #create OpenCL buffers
        self.params_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, 
                                                            hostbuf=self.params)
        print self.params
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, 
                                                            self.c.nbytes)


        self.program.mandlebrot(self.queue, self.c.shape, None, 
                                    self.params_buf, self.dest_buf)
        cl.enqueue_read_buffer(self.queue, self.dest_buf, self.c).wait()

        return self.c.reshape(self.w,self.h)
    def on_release(self,event):
        self.release_x = event.xdata

        self.release_y = self.press_y + (self.release_x-self.press_x)
        #self.release_y = event.ydata

        self.tx0 = self.press_x * float(self.x1-self.x0)/self.w + self.x0
        self.ty0 = self.press_y * float(self.y1-self.y0)/self.h + self.y0
        self.tx1 = self.release_x * float(self.x1-self.x0)/self.w + self.x0
        self.ty1 = self.release_y * float(self.y1-self.y0)/self.h + self.y0

        self.x0 = self.tx0
        self.y0 = self.ty0
        self.x1 = self.tx1
        self.y1 = self.ty1

        self.pressed = False

        self.render()
    def on_press(self,event):
        self.press_x = event.xdata
        self.press_y = event.ydata

        self.pressed = True

    def clear_rectangle(self):
        if self.rectangle is not None:
            self.rectangle.remove()
            self.rectangle = None

    def on_move(self,event):
        if self.pressed:
            self.clear_rectangle()

            self.rectangle = self.ax.add_patch(Rectangle(
                                            (self.press_x,self.press_y), 
                                            event.xdata-self.press_x,
                                            event.xdata-self.press_x,
                                            facecolor="none"))
            self.fig.canvas.draw()
    def render(self):
        self.clear_rectangle()

        res = m.run(self.x0,self.y0,self.x1,self.y1)

        self.ax.imshow(res, interpolation='nearest')
        self.fig.canvas.draw()

    def prepare_plot(self):
        self.fig, self.ax = plt.subplots()

        cid = self.fig.canvas.mpl_connect('button_press_event', m.on_press)
        cid = self.fig.canvas.mpl_connect('button_release_event', m.on_release)
        cid = self.fig.canvas.mpl_connect('motion_notify_event', m.on_move)

        self.render()

        plt.show()

m = CL()
m.loadProgram("mandlebrot.cl")

m.prepare_plot()
