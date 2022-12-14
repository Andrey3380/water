import numpy as np
import matplotlib.pyplot as plt
import turtle as t
import random
import math


class Common():
    def __init__(self, fd=80000, fs=21000, ti=0.1, Tc=2, d=0.2):
        self.fd = fd
        self.fs = fs
        self.ti = ti
        self.Tc = Tc
        self.d = d


class water(Common):
    def __init__(self, sub, obj, fd=80000, fs=21000, ti=0.1, Tc=2, d=0.2):
        Common.__init__(self)
        self.submarine = sub
        self.objects = obj


    def signal(self, r, phi):
        r = 500
        time = np.arange(0, self.Tc, 1/self.fd)

        signal_left = 10 * np.sin(2 * np.pi * self.fs * time) + np.random.randn(time.size)
        signal_right = 10 * np.sin(2 * np.pi * self.fs * time+np.pi/4) + np.random.randn(time.size)/10

        delay = r / 1000
        dt = self.d / 1000 * np.sin(phi / 180.0 * np.pi)

        for i in range(time.size):
            if time[i] > delay and time[i] < delay + self.ti:
                signal_left[i] += np.sin(2 * np.pi * self.fs * time[i])
                signal_right[i] += np.sin(2 * np.pi * self.fs * time[i] - dt)

        plt.plot(time, signal_left, time, signal_right)
        plt.show()

        return ((time, signal_left, signal_right))


class sonar(Common):
    def get_coordinates (self, signalLeft, signalRight):
        spectrumLeft = np.fft.fft(signalLeft)
        spectrumRight = np.fft.fft(signalRight)

        n = spectrumLeft.size

        zLeft = np.abs(np.fft.ifft(spectrumLeft))
        sigma = np.sqrt((np.sum(np.sqrt(zLeft))/n))
        detection_level = np.where(zLeft >= sigma)
        distance = ((detection_level[0][0])/self.fd)*1650

        print(distance)


        phi1 = np.angle(signal_left)
        phi2 = np.angle(signal_right)
        dphi = phi1 - phi2
        dphi = np.angle(np.exp( 1j * dphi) )


        dphi_mean = sum(dphi)/dphi.size
        peleng = np.arcsin( np.sin(dphi_mean) )

        print(dphi_mean)

        plt.figure(2)
        plt.plot( dphi * 180/np.pi )
        plt.show()


sub = 0
obj = []
water = water(sub, obj, fs=20000, Tc=2)
(time, signal_left, signal_right) = water.signal(1000, 40)
sonar = sonar()
sonar.get_coordinates(signal_left, signal_right)