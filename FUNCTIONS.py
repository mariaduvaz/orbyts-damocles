#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 16:45:22 2018

@author: maria
"""

###SMALL MISCELLANEOUS FUNCTIONS USED IN ALL MY CODES###


import numpy as np

import sys
#sys.path.append('/home/maria/PYTHONCODES/mazzyfuncts/modules')


import re
import os
import matplotlib.pyplot as plt
import sys
####read in data file and split each column into arrays!! 



def appendline(read,start,stop):
    
    x = []    
    for line in read[start:stop]:    
        line = line.split()
        x.append(line)
    return x
 
def checkspacing(array):
    #returns True if spacing is equal between every point, used to test meshgrids have been made properly
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
        

def find_nearest(array, values):
    #tell the function a value, finds closest number to it in an array 
    #and returns index
    indices = np.abs(np.subtract.outer(array, values)).argmin()
    return array[indices]


def convert_wav_to_vel(wavarray,obspeak,labpeak):
	#used for spectra to convert
    final_vel = []
    
    
    zpeak = (float(obspeak) - float(labpeak))/float(obspeak)
    print(zpeak)
    radvel = 299792 * zpeak
  

    for i in range(0,len(wavarray)):
        
        z = ((wavarray[i] - labpeak)/wavarray[i])
        j = (299792 * z) - radvel
        final_vel.append(j)
    return(final_vel)
  


  
def snip_spect(x_axis,flux_axis,*args):
	#args are values you want to snip between, from left to right
	#you're creating a straight line of x = y betweeen the two points 
	#eg. to interpolate between narrow line regions, to snip cosmic rays etc
	#only works on a list
        
        

                
        for first, second in zip(args, args[1:]):
               
           if (args.index(first)) % 2 == 0:
                             
               x1 = find_nearest(x_axis,first)
               		
               x2 = find_nearest(x_axis,second) 
         		
               ind1 = x_axis.index(x1)
               
               ind2 = x_axis.index(x2)
               	
               
               y1 = flux_axis[ind1]
               y2 = flux_axis[ind2]
             
               arraysize = ind2 - ind1
             
               y_replacementpoints = np.linspace(y1,y2,arraysize)
               flux_axis[ind1:ind2] = y_replacementpoints
               
        return flux_axis  




    
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
    
    
    if zipped == False:
        return obsdata
    
    
        
    no_rows = (len(obsdata[1])) #just incase theres a header in first line

  
    ###ROWS NEED TO BE ALL SAME LENGTH FOR THIS TO WORK
    lists = [[] for _ in range(no_rows)]

    lists = list(zip(*obsdata))
    
    
    for i in range(0,no_rows):
        
        if isint == False:
                    lists[i] = [float(j) for j in lists[i]]
            
        else:            
                    lists[i] = [int(float(j)) for j in lists[i]]
                    
    return lists                

                





def save_output_png(directory):
    #used in loops running models many times to save output plot as a .png file
  
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
        
        


def sigma_clip(array,degree):
	#used to remove cosmic rays etc from spectra
    stdev = np.std(array)
    median = np.median(array)
    print(median - (degree * stdev))
    print(median + (degree * stdev))
    for k in range(len(array)):   
        if array[k] > (median + (degree * stdev)) or array[k] < (median - (degree * stdev)): 
              array[k] = 0
    
    return array

def get_WCS(file,degrees=True):
    #used for fits file to extract the coordinates
    hdulist = fits.open(file)         #("r3casa_p001.0014.sensdiv.fits")
    hdr = hdulist[0].header
    if degrees == True:
        RA = AC.ra_2_degrees(hdr['RA'])
        DEC = AC.dec_2_degrees(hdr['DEC'])
    else:
        RA = hdr['RA']
        DEC = hdr['DEC']
        
    return RA,DEC

def trim_wav_flux(lambd_points,flux_points,point1,point2):
        #given two points on the x axis of a 1d spectra, 
        #we trim both the x and y axis to be only between these two points
        x = []
        lambd_points = list(lambd_points)
        
        x1 = find_nearest(lambd_points,point1)
        x2 = find_nearest(lambd_points,point2) 
                      
        ind1 = lambd_points.index(x1)
        ind2 = lambd_points.index(x2)
        
        new_lam = lambd_points[ind1:ind2]
        new_fl = flux_points[ind1:ind2]
        
        return new_lam, new_fl 


def snip_spect(x_axis,flux_axis,*args):
	#args are values you want to snip between, from left to right
	#you're creating a straight line of x = y betweeen the two points 
	#eg. to interpolate between narrow line regions, to snip cosmic rays etc
	#only works on a list
        
        

                
        for first, second in zip(args, args[1:]):
               
           if (args.index(first)) % 2 == 0:
                             
               x1 = find_nearest(x_axis,first)
               		
               x2 = find_nearest(x_axis,second) 
         		
               ind1 = x_axis.index(x1)
               
               ind2 = x_axis.index(x2)
               	
               
               y1 = flux_axis[ind1]
               y2 = flux_axis[ind2]
             
               arraysize = ind2 - ind1
             
               y_replacementpoints = np.linspace(y1,y2,arraysize)
               flux_axis[ind1:ind2] = y_replacementpoints
               
        return flux_axis
    
#'''    
