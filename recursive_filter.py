import numpy as np
from scipy import signal

class DAQ_filts:
    
    def __init__(self,cut_off,samplerate,order,channels,filt_type):
        self.filters = [[]]*channels
        
        if filt_type:
            for chan in range(channels):
                #self.filters[chan] = self.kalman_filt(cut_off,samplerate,order)
                print 'Regressive filters not yet supported!'
                print 'Reverting to simple filter.'
                self.filters[chan] = self.recursive_filt(cut_off,samplerate,order)
        else:
            for chan in range(channels):
                self.filters[chan] = self.recursive_filt(cut_off,samplerate,order)
        
        
        

class recursive_filt:
    Wc = 0.5

    def __init__(self,cut_off,samplerate,order):
        self.Wc = float(cut_off)/float(samplerate/2)
        [b,a] = signal.butter(order,self.Wc)
        self.b = b.flatten()
        self.a = a.flatten()

        #print self.b
        #print self.a

        self.y_prev = np.zeros((order,1)).flatten()
        self.y_out_prev = np.zeros((order,1)).flatten()


        #self.TF = np.c_[self.b,self.a].T
        #print self.TF

        pass


    def iter(self,y,dt):
        #print y
        x_vec = np.r_[y,self.y_prev]
        y_out_vec = np.r_[0,self.y_out_prev]

        #print 'In iter'
        #print x_vec
        #print y_out_vec
        #print '----'
        #print ''

        b_vec = self.b*x_vec
        a_vec = self.a*y_out_vec
        y_out_delta =  np.sum(b_vec) - np.sum(a_vec)
        y_out = y_out_delta

        #print y_out
        self.y_prev = np.r_[y,self.y_prev[:-1]]
        self.y_out_prev = np.r_[y_out,self.y_out_prev[:-1]]
        return y_out




