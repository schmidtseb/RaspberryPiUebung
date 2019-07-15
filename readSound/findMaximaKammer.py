import numpy as np

f, A  = np.genfromtxt('kammertonA_frequency.dat').T

# Herausfiltern der 0 Hz - Linie
A = A[f > 0]
f = f[f > 0]

# Mittelwert und Standardabweichung
AMean = np.mean( A )
AStd = np.std( A )

# Endlosschleifen
print '# f (Hz)\t A (a.u.)'
while True:
	# Finden des Maximums
	idx = np.argmax( A )
	f_, A_ = f[idx], A[idx]

	# Hebt sich das Maximum signifikant vom Rest des Spektrums ab?
	if abs(AMean - A_) > 5 * AStd:
		print '%.2f\t%.2f' % (f_, A_)

		# Zuruecksetzen des Peaks
		A[idx] = 0
	else:
		break

