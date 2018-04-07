'''
Class to output residual plot directly
'''
import libstempo as T
import matplotlib.pyplot as P
import numpy as N

class Tempo2Res(object):
    def __init__(self, timfile='test.tim', parfile='test.par'):
        self.timefile = timfile 
        self.parfile = parfile
        self.toas = None
        self.res = None
        self.toaerr = None

    def fit(self):
        psr = T.tempopulsar(parfile=self.parfile, timfile = self.timefile)
        i = N.argsort(psr.toas())
        self.toas = psr.toas()[i]
        self.res = psr.residuals()[i]
        self.toaerr = psr.toaerrs[i]

    def plot(self,*args,**kwargs):
        P.errorbar(self.toas,self.res,yerr=1e-6*self.toaerr,fmt='o',c='black',*args,**kwargs)
        P.xlabel('MJD')
        P.ylabel('Residuals [$\mu s$]')
        P.title('Residuals')

    def show(self,*args,**kwargs):
        self.fit()
        self.plot()
        P.show()

if __name__ == '__main__':
    # testing
    tr = Tempo2Res()
    tr.show()
