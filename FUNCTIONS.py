#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 16:45:22 2018

@author: maria
"""
####saving small functions i always use in all my codes
import numpy as np

import sys
sys.path.append('/home/maria/PYTHONCODES/mazzyfuncts/modules')

from ASTROCONSTANTS import *

import re
import os
import matplotlib.pyplot as plt
import sys
####read in data file and split each column into arrays!! 



def appendline(read,start,stop):
    #each line of grid is read in as 1 string, this splits them into equal parts
    x = []    
    for line in read[start:stop]:    
        line = line.split()
        x.append(line)
    return x
 
def checkspacing(array):
    #returns True if spacing is equal between every point, used for grids
    y = []
    for first, second in zip(array, array[1:]):
        x = abs(second - first)
        print(x)
        if x != 0:
            y.append(second - first)
            
    if len(set(y)) <= 1:
        print("GRID SPACED EVENLY")   
    else:
        print("ITS NOT EQUAL TRY AGAIN")
        print(np.amin(y))
        #return(y)
        


def makeitfloat(array):    
    x = [float(j) for j in array]
    return x 

def inting(array):
    c = [int(j) for j in array]
    return c

def find_nearest(array, values):
    #tell the function a value, finds closest number to it in an array 
    #and returns index
    indices = np.abs(np.subtract.outer(array, values)).argmin()
    return array[indices]


def convert_wav_to_vel(wavarray,obspeak,labpeak):
    final_vel = []
    
  


    zpeak = (obspeak - labpeak)/obspeak
    radvel = AC.c * zpeak
  

    for i in range(0,len(wavarray)):
        
        z = ((wavarray[i] - labpeak)/wavarray[i])
        j = (AC.c * z) - radvel
        final_vel.append(j)
    return(final_vel)
    
    
    
def datafile_2_array(filename,isint=True,zipped=True):
    '''
    need to change to directory and specify datafile beforehand
    returns a list of lists where each list is a column in the datafile
    can then allocate each array after calling this function
    if isint=True then convert rows to ints, otherwise converts to float
    this is specifically for spectra (two/three rows), sometimes with a header
    '''
    
    opening = open(filename, 'r')
    reading = opening.readlines()
    
    obsdata = appendline(reading,0,len(reading))
    
    #x = re.search('[a-df-zA-DF-Z-#]', reading[0]) #checking whether theres a header
    
   
    #if x == None:
     #       obsdata = appendline(reading,0,len(reading))
    #else:
     #       obsdata = appendline(reading,1,len(reading))
      
    
    
    if zipped == False:
        return obsdata
    #row_size = list(set([len(i) for i in obsdata])) 
    
        
    no_rows = (len(obsdata[1]))

  
    ###IF ROW NUMBERS NOT ALL SAME LENGTH THEN RETURN ERROR....
        
    lists = [[] for _ in range(no_rows)]

    lists = list(zip(*obsdata))
    
    
    for i in range(0,no_rows):
        
        if isint == False:
                    lists[i] = [float(j) for j in lists[i]]
            
        else:            
                    lists[i] = [int(float(j)) for j in lists[i]]
                    
    return lists                
'''     
        if len(lists) > 5:
            arr_nos = input("enter array no. of rows you want to extract, or n if all ")
            
            if arr_nos == 'n':
                return lists
                break
            
            else:
                arr_nos = [int(float(j)) for j in arr_nos.split()]  #turning raw input of row number as string
            
                return(lists[arr_nos[0]],lists[arr_nos[1]])     
                break
        
        else:
            return lists
'''
                





def save_output_png(directory):
    
  
    x = os.listdir(directory)
    if x == []:
        out_name = "1"
        os.chdir(directory)
        
        plt.savefig(out_name,dpi=500)
        plt.close()
    else:
   
        os.chdir(directory)
    
        filenumbers = []
        for i in x:
            part1,part2 = i.split('.')
            filenumbers.append(part1)
    
    
        sort_file = sorted(filenumbers, key=int)
        print(sort_file)
        new_no = int(sort_file[-1]) + 1
        out_name = str(new_no)
        plt.savefig(out_name,dpi=500)
        plt.close()
    
    
def savedata_2file(filename,array,fmtarguments):
        np.savetxt(filename,array,fmt=fmtarguments)
        
        
def find_ind(dictionary,key,value):                    
    for index, dic in enumerate(dictionary):      
        if dic[key] == value:
            return index
    return None



def sigma_clip(array,degree):
    stdev = np.std(array)
    median = np.median(array)
    print(median - (degree * stdev))
    print(median + (degree * stdev))
    for k in range(len(array)):   
        if array[k] > (median + (degree * stdev)) or array[k] < (median - (degree * stdev)): 
              array[k] = 0
    #get new stdev
    return array

def get_WCS(file,degrees=True):
    
    hdulist = fits.open(file)         #("r3casa_p001.0014.sensdiv.fits")
    hdr = hdulist[0].header
    if degrees == True:
        RA = AC.ra_2_degrees(hdr['RA'])
        DEC = AC.dec_2_degrees(hdr['DEC'])
    else:
        RA = hdr['RA']
        DEC = hdr['DEC']
        
    return RA,DEC
    
#'''    
