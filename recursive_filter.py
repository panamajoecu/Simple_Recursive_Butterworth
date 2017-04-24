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
                self.filters[chan] = self.mov_avg_filt(samplerate,order)
        else:
            for chan in range(channels):
                self.filters[chan] = self.mov_avg_filt(samplerate,order)
        
        
        

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


class mov_avg_filt:

    def __init__(self,samplerate,order):

        self.y_prev = np.zeros((order,1)).flatten()
        self.dt_prev = np.ones((order,1)).flatten()/float(samplerate)
        self.samplerate = samplerate
        self.dt_min = .95/float(samplerate)  # Less than 1 to account for numerical precision

        pass


    def iter(self,y,dt):

        if (dt<self.dt_min):
            print 'Error!  Timestep less than initialized samplerate!'
            print 'Defaulting to original timestep.'
            print ''
            dt = self.dt_min
        

        self.y_prev = np.r_[y,self.y_prev[:-1]]
        self.dt_prev = np.r_[dt,self.dt_prev[:-1]]


        num = np.sum(self.y_prev*self.dt_prev)
        den = np.sum(self.dt_prev)
        y_out = num/den

        #print y_out
        return y_out



