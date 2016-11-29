# Copyright (c) 2015  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import myo as libmyo
from myo import StreamEmg
from time import clock
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from pythonosc import osc_message_builder
from pythonosc import udp_client

fig, ((ax0, ax1), (ax2, ax3), (ax4, ax5), (ax6, ax7)) = plt.subplots(nrows=4, ncols=2)
ax0.set_ylim([-50, 50])
ax1.set_ylim([-50, 50])
ax2.set_ylim([-50, 50])
ax3.set_ylim([-50, 50])
ax4.set_ylim([-50, 50])
ax5.set_ylim([-50, 50])
ax6.set_ylim([-50, 50])
ax7.set_ylim([-50, 50])

x = np.zeros(20)
x = np.resize(x, (8, 20))
y = np.arange(0,20)

lines=[]
lines.extend(ax0.plot(y,x[0]))
lines.extend(ax1.plot(y,x[1]))
lines.extend(ax2.plot(y,x[2]))
lines.extend(ax3.plot(y,x[3]))
lines.extend(ax4.plot(y,x[4]))
lines.extend(ax5.plot(y,x[5]))
lines.extend(ax6.plot(y,x[6]))
lines.extend(ax7.plot(y,x[7]))

#### MYO INIT
libmyo.init()
try:
    hub = libmyo.Hub()
except MemoryError:
    print("Myo Hub could not be created. Make sure Myo Connect is running.")

hub.set_locking_policy(libmyo.LockingPolicy.none)
feed = libmyo.device_listener.Feed()
hub.run(1000, feed)
myos = feed.get_connected_devices()
feed.wait_for_single_device(10)
myos[0].set_stream_emg(StreamEmg.enabled)

#### OSC init
client = udp_client.SimpleUDPClient("172.19.2.89", 5005)

#### ANIMATION Functions
def animate(i):
    global x
    myos = feed.get_connected_devices()

    if myos:
        if myos[0].emg:
            for i in range(8):
                newx = np.append(x[i][1:20], [myos[0].emg[i]])
                x[i] = newx
                lines[i].set_ydata(x[i])
            # Send emg via OSC
            client.send_message("/myo", myos[0].emg)

    return tuple(lines)

#Init only required for blitting to give a clean slate.
def init():
    for i in range(8):
        lines[i].set_xdata(y)
    return tuple(lines)

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
    interval=25, blit=True)

plt.show()

hub.stop(True)
hub.shutdown()
