import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import scipy.signal as sig

import psd

# Example FIR low pass filter
fs = 1000

b = sig.firwin(21, 300, fs=fs)

# Frequency response
f, H = sig.freqz(b, fs=fs)

# Magnitude
psd.plot_filt_mag(f, H, title="Magnitude response")
plt.show()

# Complete response
psd.plot_filt_resp(f, H)
plt.show()

# Pole-zero map
z, p, k = sig.tf2zpk(b, [1])
psd.plot_pzmap(z, p)
plt.show()