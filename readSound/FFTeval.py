#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

f, A, Ar, Ai = np.genfromtxt('testFile.dat').T
t = 1./(f[1] - f[0])

A[f > 100] = 0
Ar[f > 100] = 0
Ai[f > 100] = 0

print t
plt.plot( np.linspace(0, t, 1000), np.fft.irfft( Ar + 1j*Ai ) )
plt.show()

f = 50 # in Hz
t = np.linspace(0, 0.2, 1000) # in s
# A = np.sin(2*np.pi*f*t)
# A = signal.square(2*np.pi*f*t, duty=0.5) 
A = sum([1./f * np.sin(2*np.pi*f * t) for f in np.arange(50, 2550, 50)])

freqVal = np.fft.rfft( A )
freq = np.fft.rfftfreq(t.size, t[1] - t[0])

np.savetxt('testFile.dat', np.asarray([freq, np.abs(freqVal), np.real(freqVal), np.imag(freqVal)]).T, header='time (s)\tAmplitude (a.u.)')

plt.plot(freq, freqVal)
plt.grid(which='both')
plt.ylim(1.e-4, 1.1 * max(freqVal))
plt.show()

plt.plot(t, A)
plt.axhline(y=0, ls='--', color='k', alpha=.5)
plt.xlabel('t (s)')
plt.ylabel('Amplitude (a.u.)')
plt.show()

