import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import clock
from collections import deque
import myo as libmyo

fig, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7)) = plt.subplots(2, 4, sharey=True)

line0, = ax0.plot(np.zeros(100))
ax0.set_ylim(-100, 100)

line1, = ax1.plot(np.zeros(100), color='#D4A190')
line2, = ax2.plot(np.zeros(100), color='g')
line3, = ax3.plot(np.zeros(100), color='r')
line4, = ax4.plot(np.zeros(100), color='c')
line5, = ax5.plot(np.zeros(100), color='m')
line6, = ax6.plot(np.zeros(100), color='y')
line7, = ax7.plot(np.zeros(100), color='k')

libmyo.init()
try:
    hub = libmyo.Hub()
except MemoryError:
    print("Myo Hub could not be created. Make sure Myo Connect is running.")

if hub:
    feed = libmyo.device_listener.Feed()
    # hub.run_once(1, feed)
    hub.run(1, feed)

    print("Waiting for a Myo to connect ...")
    myo = feed.wait_for_single_device(2)
    myo.set_stream_emg(libmyo.lowlevel.enums.StreamEmg.enabled)

    if not myo:
        print("No Myo connected after 2 seconds.")
    
    print("Hello, Myo!")


def update_line(new_data):
    line0.set_ydata(new_data[0])
    line1.set_ydata(new_data[1])
    line2.set_ydata(new_data[2])
    line3.set_ydata(new_data[3])
    line4.set_ydata(new_data[4])
    line5.set_ydata(new_data[5])
    line6.set_ydata(new_data[6])
    line7.set_ydata(new_data[7])
    
    return line0, line1, line2, line3, line4, line5, line6, line7,

def data_gen():
    global myo, hub, feed
    emgSamples = [[0 for x in range(100)] for y in range(8)]
    while True:
        # hub.run_once(1, feed)
        if myo.emg:
            for i in range(8):
                emgSamples[i].append(myo.emg[i])
                if len(emgSamples[i]) > 100:
                    emgSamples[i].pop(0)

            yield emgSamples

    return

ani = animation.FuncAnimation(fig, update_line, data_gen, interval=1, blit=True)
plt.show()
hub.shutdown()