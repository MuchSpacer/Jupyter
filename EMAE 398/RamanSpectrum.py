import numpy as np
import scipy.interpolate as itp

class RamanSpectrum:


    def __init__(self, path, L_cutoff = None, R_cutoff = None, deg = 2, divisions = 5):
        
        x0, y0 = np.loadtxt(path, skiprows = 14, unpack = True)

        if L_cutoff is None:
            L_cutoff = x[0]

        if R_cutoff is None:
            R_cutoff = x[-1]
        
        ind = np.logical_and(x0>=L_cutoff, x0<=R_cutoff)
        
        self.__x = np.copy(x0[ind])
        self.__y = np.copy(y0[ind])
        self.__bg = self.__background_approxspl(deg, divisions)
        self.__y1 = self.__y - self.__bg
        

    def __background_approxspl(self, deg, divisions):
        '''Approximate the fluorescent Raman background using a fitting spline.'''
        x = self.__x
        y = self.__y
        interval = (x[-1]-x[0]) / divisions
        knots = np.r_[(x[0],)*deg, np.arange(x[0], x[-1], interval), (x[-1],)*(deg+1)]
        
        b = itp.make_lsq_spline(x, y, knots, k = deg)
    
        return b(x)

    def plot_raw(self, axes, background = True):
        axes.plot(self.__x, self.__y)
        if background:
            axes.plot(self.__x, self.__bg)
            
    def plot_peaks(self, axes):
        axes.plot(self.__x, self.__y1)