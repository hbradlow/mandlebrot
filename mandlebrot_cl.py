import pyopencl as cl
import numpy
from matplotlib import pyplot as plt
import time
import Tkinter

class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        
        self.w = 1000
        self.h = 1000

    def loadProgram(self,filename):
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        self.program = cl.Program(self.ctx, fstr).build()
    def popCorn(self):
        mf = cl.mem_flags

        #initialize client side (CPU) arrays
        self.width = numpy.array([self.w], dtype=numpy.float32)
        self.height = numpy.array([self.h], dtype=numpy.float32)
        self.c = numpy.zeros([self.h*self.w],dtype=numpy.float32)

        #create OpenCL buffers
        self.width_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, 
                                                            hostbuf=self.width)
        self.height_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, 
                                                            hostbuf=self.height)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, 
                                                            self.c.nbytes)
    def execute(self):
        self.program.mandlebrot(self.queue, self.c.shape, None, 
                                    self.width_buf, self.height_buf, self.dest_buf)
        cl.enqueue_read_buffer(self.queue, self.dest_buf, self.c).wait()

        return self.c.reshape(self.w,self.h)

m = CL()
m.loadProgram("mandlebrot.cl")
m.popCorn()

begin = time.time()
res = m.execute()
print "Total time: " + str(time.time()-begin)

fig, ax = plt.subplots()
ax.imshow(res, interpolation='nearest')

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('button_release_event', onclick)

plt.show()
