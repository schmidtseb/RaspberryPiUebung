import RPi.GPIO as GPIO
import time
import numpy as np

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Variablen
    adcChannel = 0

    # Pins
    SPI_SCLK = 18
    SPI_MOSI = 24
    SPI_MISO = 23
    SPI_CS = 25

    GPIO.setup(SPI_SCLK, GPIO.OUT)
    GPIO.setup(SPI_MOSI, GPIO.OUT)
    GPIO.setup(SPI_MISO, GPIO.IN)
    GPIO.setup(SPI_CS, GPIO.OUT)

    # Start Messung
    messdauer = 10      # Zeit in Sekunden
    startTime = time.time()

    timeList = []
    amplitudeList = []
    while time.time() - startTime < messdauer:
        timeList.append( time.time() - startTime )
        adcVal = readADC(adcChannel, SPI_SCLK, SPI_MOSI, SPI_MISO, SPI_CS)
        amplitudeList.append( adcToPercent(adcVal) )
    # Ende Messung

    # Speicherung Amplitudendaten
    amplitudeData = np.asarray( [timeList, amplitudeList] ).T
    np.savetxt('amplitudeData.dat', amplitudeData, header='Time (s)\tAmplitude (\%)')

    # Erzeugung und Speicherung der Freuqenzdaten
    freq, freqAmplitude = calculateFFT(timeList, amplitudeList)
    frequencyData = np.asarray( [freq, abs(freqAmplitude), np.real(freqAmplitude), np.imag(freqAmplitude)] ).T
    np.savetxt('frequencyData.dat', frequencyData, header='Frequency (Hz)\tAmplitude (a.u.)\tRealteil\tImaginaerteil')
    
def readADC(adcChannel, SCLKPin, MOSIPin, MISOPin, CSPin):
    # Selektiere den ADC
    GPIO.output(CSPin, True)
    GPIO.output(CSPin, False)
    GPIO.output(SCLKPin, False)

    cmd = adcChannel
    cmd |= 0b11000
    cmdLength = 5

    # Senden des Kommandos
    for i in range(cmdLength):
        if cmd & (1 << (cmdLength - i - 1)):
            GPIO.output(MOSIPin, True)
        else:
            GPIO.output(MOSIPin, False)

        # Ein Clockpuls
        GPIO.output(SCLKPin, True)
        GPIO.output(SCLKPin, False)

	# Empfangen von Daten
    response = 0
    responseLength = 12
    
    # Empfange Nullbit
    GPIO.output(SCLKPin, True)
    GPIO.output(SCLKPin, False)

    # Empfange Daten
    for i in range(responseLength):
        GPIO.output(SCLKPin, True)
        GPIO.output(SCLKPin, False)

        if GPIO.input(MISOPin):
            response |= (1 << (responseLength - i - 1))

    return response

def adcToPercent(adcVal):
    adcResolution = float(2**12 - 1)
    voltVal = adcVal/adcResolution * 3.3

    # Spannung relativ zum halben Maximum
    voltVal = voltVal - 3.3 / 2

    # Normierung
    voltVal /= (3.3 / 2)

    return voltVal

def calculateFFT(time, amplitude):
    # Mittlere Zeitdifferenz zwischen zwei Datenpunkten
    tMean = np.mean(np.diff(time))
    
    # Erzeuge neue Zeiten
    timeNew = np.arange(min(time), max(time), tMean)
    
    # Interpolation
    amplitudeNew = np.interp(timeNew, time, amplitude)

    # Calculate FFT
    freq = np.fft.rfftfreq(timeNew.size, tMean)
    freqAmplitude = np.fft.rfft(amplitudeNew)
    
    return freq, freqAmplitude

if __name__ == '__main__':
    main()

