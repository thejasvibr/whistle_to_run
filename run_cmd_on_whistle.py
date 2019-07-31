# -*- coding: utf-8 -*-
""" Detects a whistle pattern and runs a given command 

MIT License

Copyright (c) 2019 Thejasvi Beleyur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Wed Jul 31 17:22:36 2019

@author: tbeleyur
"""

import argparse 
import numpy as np 
import os
#import matplotlib.pyplot as plt
#plt.rcParams['agg.path.chunksize'] = 10000
import sounddevice as sd


my_parser = argparse.ArgumentParser(description='Listen for a sound with a peak frequency and run commands if detected')

my_parser.add_argument('-fs', dest='fs',
                       type=int,
                       help='Sampling rate in Hz',
                       default=22050)
my_parser.add_argument('-target',
                       dest='target_freq',
                       type=float,
                       default=1000,
                       help='Target frequency in Hz')
my_parser.add_argument('-tolerance',
                       dest='tolerance',
                       type=float,
                       help='Tolerance of peak frequency in Hz',
                       default=500)

my_parser.add_argument('-command',
                       dest='command',
                       type=str,
                       help='Commands to be run')


args = my_parser.parse_args()

def rms(X):
    X_rms = np.sqrt(np.mean(X**2))
    return(X_rms)

def dBrms(X):
    return(20*np.log10(rms(X)))

def does_signal_match(audio_block, **kwargs):
    ''' Checks if the peak frequency of an audio buffer
    is within a range of a given target frequency. 
    
    Parameters
    -----------
    audio_block : 1 x nsamples np.array
                The audio coming from a single channel

	Keyword Arguments
	-----------------
    
    fs : int. 
         Sampling rate in Hz. 
         Defaults to 22.05 kHz

    target_freq : float >0.
                target frequency of the sound in Hz
                Defaults to 1 kHz

    tolerance : float.
                The range within which the peak frequency of 
                the sound should be. 
                if the peak frequency is +/- tolerance 
                then a True is passed, else not. 

    Returns
    -------
        Boolean.
        True if the peak frequency is within acceptable range
        False if not. 
        If the audio block is not loud enough then False is returned too. 

    '''
    fs = kwargs.get('fs', 22050)
    target_freq = kwargs.get('target_freq', 1000)
    tolerance = kwargs.get('tolerance', 500)
    
    audio_block -= np.mean(audio_block)
        
    if dBrms(audio_block) < -30:
        return(False)
    else: 
        audio_powerspectrum = 20*np.log10(np.abs(np.fft.rfft(audio_block.flatten())))
        freqs = np.fft.rfftfreq(audio_block.size, 1/fs )
        max_freq = freqs[np.argmax(audio_powerspectrum)]
        
        if target_freq - tolerance <= max_freq <= target_freq + tolerance:
            return(True)
            
        
    
def run_command_if_triggered(CMD, **kwargs)    :
    '''
    '''
    #def open_audio_stream():
    fs = kwargs.get('fs',22050)

    block_size = int(fs*0.5)
    S = sd.Stream(fs, blocksize=block_size, channels=1,
                  latency=0.5)
    S.start()

    while True:
        audio_block, overflow = S.read(block_size)
        
        signal_match = does_signal_match(audio_block, **kwargs)
        
        if signal_match:
            print('Target PEAK FREQUENCY REACHED! -- executing command!!! ')
            os.popen(CMD)
            S.stop
            break

if __name__ == '__main__':
    #command = 'start activate theCPN && spyder'
    kwargs = args.__dict__
    for i,j in kwargs.items():
        print(i,j)
    run_command_if_triggered(kwargs['command'], **kwargs)
        
    

    



    
    
        