import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import psd

imp = psd.signals.kronecker_delta(1000) #impulse signal, to get impulse transfer
fs = 1000

N = 20  # taps
C = 2   # num of cascade promediators
L = 4   # interpolation factor

# Lyons recursive High pass filter
h = psd.filters.lyons_highpass(imp, N, C=C, interpolation=L)

delay = psd.filters.delay_lyons_filter(N, C, L, fs=fs)

H = np.fft.rfft(h)
f = np.fft.rfftfreq(len(h), 1/fs)

plt.grid()
psd.plot.plot_filt_mag(f, H)
plt.show()

plt.grid()
psd.plot.plot_filt_phase(f, H)
plt.show()

plt.grid()
psd.plot.plot_filt_delay(f, H)
plt.ylim([0,delay*1.1])
plt.yticks(np.arange(0, delay*1.1, delay*.11))
plt.show()

fpass = [1, 20, 30]
fstop = [10, 15, 40]

attepass = [10, 1]
attestop = [20, 20]

plt.xlim(-10, 50)
plt.ylim(-50, 10)
psd.plot.plot_template(fpass, fstop, attepass, attestop)
plt.legend()
plt.show()