import matplotlib.pyplot as plt
import psd

fs = 1000	# Sampling Frequency
nn = 2000	# Number of points
freq = 10	# Frequency of the signal		

# Generate signals
t, sine = psd.signals.sin(vmax=2,dc=0.5,ff=freq, ph=0, nn=nn, fs=fs,)
_, square = psd.signals.square(vmax=1, ff=freq, duty=0.5, nn=nn, fs=fs,)
_, triangle = psd.signals.triangle(vmax=1, ff=freq, nn=nn, fs=fs,)
_, noise = psd.signals.noise_generator(var=0.2, nn=nn, fs=fs,)
quantized = psd.utils.quantizer(sine, 3)

plt.figure(figsize=(10, 6))
plt.plot(t, sine, label="Sine")

plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Signal generation examples")
plt.grid()
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t, square, label="Square")

plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Signal generation examples")
plt.grid()
plt.legend()

plt.show()
plt.figure(figsize=(10, 6))
plt.plot(t, triangle, label="Triangle")

plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Signal generation examples")
plt.grid()
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t, noise, label="Noise")

plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Signal generation examples")
plt.grid()
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t, quantized, label="Quantized sine")

plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.xlim([0, 3/freq])
plt.title("Signal generation examples")
plt.grid()
plt.legend()

plt.show()
