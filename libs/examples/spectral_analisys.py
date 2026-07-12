import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import psd

fs = 1000
t, x = psd.sin(vmax=1, ff=100, nn=2000, fs=fs)

# FFT
X = psd.fft(x, window="hann")
f = psd.freq_axis(x, fs)

plt.figure(figsize=(10, 5))
plt.plot(f, abs(X))

plt.xlim(0, 300)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.title("FFT example")
plt.grid()

plt.show()


# Blackman-Tukey PSD
f_psd, Pxx = psd.blackman_tukey(x, fs=fs)

plt.figure(figsize=(10,5))
plt.plot(f_psd, 10*psd.power_db(Pxx))

plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [dB]")
plt.title("Blackman-Tukey PSD")
plt.grid()

plt.show()