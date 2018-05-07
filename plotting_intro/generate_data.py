#!/usr/bin/env python
import numpy as np

def normal(x, A, mu, sigma):
	return A*np.exp(-(x - mu)**2 / (2*sigma**2))

A = 10		# Amplitude
mu = 5		# Mittelwert
sigma = 3	# Standardabweichung
N = 100		# Anzahl der Datenpunkte

x = np.linspace(mu-5*sigma, mu+5*sigma, N)
y = normal(x, A, mu, sigma) + np.random.normal(0, 1, N)

f = open('sample.dat', 'w')
for i in range( len(x) ):
	f.write(str(x[i]) + '\t' + str(y[i]) + '\n')
f.close()

