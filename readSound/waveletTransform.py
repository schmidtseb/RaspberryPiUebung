#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.io import wavfile
from matplotlib.colors import LogNorm
import waipy

INFILE = 'Barbastella_barbastellus_1_o.wav'

def main():
	'''
	d = np.genfromtxt(INFILE).T
	time, data = d
	'''

	fs, data = wavfile.read(INFILE)
	plt.plot(data)
	# plt.show()

	data = data[10000:11000]
	# data = scipy.signal.resample(data, len(data)//4)
	# time = np.arange(0, len(data), 1./fs)
	time = np.arange(len(data))

	data = waipy.normalize(data)
	result = waipy.cwt(data, 1, 1, 0.25, 2, 4/0.25, alpha, 6, mother='Morlet')
	waipy.wavelet_plot()

	wavelet(time, data, True)
	raw_input('')

def wavelet(x, data, show=False):
    left, right = x[0], x[-1]

    widths = np.arange(1, 100)
    cwtmatr = scipy.signal.cwt(data, scipy.signal.ricker, widths)
    cwtproj = cwtmatr.sum(axis=0)
    cwtproj /= sum( cwtproj )

    if show:
        fig, axes = plt.subplots(2, sharex=True)

        axes[0].plot(x, cwtproj, '-')
	mat = abs(np.square(cwtmatr))
	mat[mat == 0] = 1
	print mat
        axes[1].imshow(mat, extent=[left, right, 1, 10], cmap='viridis', aspect='auto', vmax=abs(cwtmatr).max(), vmin=1, norm=LogNorm())

        fig.show()

if __name__ == '__main__':
	main()

