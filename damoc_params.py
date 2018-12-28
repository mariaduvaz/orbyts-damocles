
#only works with python2.7

import os
import damocleslib as model
import numpy as np
import matplotlib.pyplot as plt
import sys
import fileinput
sys.path.append("/home/maria/PYTHONCODES")

from mazzyfuncts import FUNCTIONS as fn   ##THIS IS FROM PACKAGE ON MY COMP, MAKE FUNCTIONS AVAILABLE...
from mpl_toolkits import mplot3d
#variable parameters


#input params to vary
v_max=2000.0
Rrat = 0.3 #rin/rout
rho_index=2
mdust=0
grain_size=0.01


##constants
age=1000         #in years
age_d = age*365
age_s = 3.154e7
gridsize = 4000.0  #in km/s, want it to be larger than v_max by about 2
grid_divs = 40

##Get radii
v_min = v_max * Rrat

Rout = v_max * age_d * 8.64e-6 * 1e15
Rin = v_min* age_d * 8.64e-6 * 1e15
print(Rout)



print(Rout,Rin)


#Read in input files
input_file = "input/input.in"
dust_file = "input/dust.in"
gas_file = "input/gas.in"
spec_file = "input/species.in"
inlines = fn.datafile_2_array(input_file,isint=False,zipped=False)
dustlines = fn.datafile_2_array(dust_file,isint=False,zipped=False)
gaslines = fn.datafile_2_array(gas_file,isint=False,zipped=False)
speclines = fn.datafile_2_array(spec_file,isint=False,zipped=False)

#Replace values in files with values used here
#putting parameters we specified in this code about the geometry into the model

#input.in file
inlines[12][0] = str(age_d)

#writing back to file
dustlines[1][0] = str(mdust)
#dustlines[7][0] = str(v_max)
#dustlines[9][0] = str(Rrat)
#dustlines[11][0] = str(rho_index)

speclines[3][3] = str(grain_size)
speclines[3][4] = str(grain_size)
#


#making the shell datapoints
grid_arr = np.linspace(-Rout,Rout,grid_divs)

Y,X,Z = np.meshgrid(grid_arr,grid_arr,grid_arr) 
Xf = X.flatten()
Yf = Y.flatten()  
Zf = Z.flatten()
rads= [np.sqrt(Xf[i]**2 + Yf[i]**2 + Zf[i]**2) for i in range(len(Xf))]

rho = np.zeros((len(Xf)))


plotdens,plotx,ploty,plotz = [],[],[],[]

for j in range(len(rads)):
    if abs(rads[j]) <= Rout and abs(rads[j]) >= Rin:
        if Xf[j] > 0 and Yf[j] > 0 and Zf[j] > 0:
            rho[j] = (abs(rads[j]))**(-rho_index)*1e20
        else:
           
            rho[j] = (abs(rads[j]))**(-rho_index)*1e20
            plotdens.append(rho[j])
            plotx.append(Xf[j])
            ploty.append(Yf[j])
            plotz.append(Zf[j])


#plot the shell
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X axis (cm)')
ax.set_ylabel('Y axis (cm)')
ax.set_zlabel('Z axis (cm)')

plt.title("Gas model of Supernova")

param_label = "vmax: "+str(v_max)+","+"Rrat: "+str(Rrat)+","+"rho_index: "+str(rho_index)
ax.scatter(plotx,ploty,plotz,c=plotdens,cmap="nipy_spectral",label=param_label)
plt.legend()
'''


#save the grid to use in dust_grid.in
outfile = "input/dust_grid.in"
title_1 = (v_max,Rout/(1e+15), 1.0, '!vmax (km/s),rmax (e15 cm), v(r) index')
title_2 = ('#', grid_divs,grid_divs,grid_divs)

print(title_1)
scaledgrid = list(zip(Xf,Yf,Zf,rho))
scaledgrid.insert(0,title_2)
scaledgrid.insert(0,title_1)
            
x = np.savetxt(outfile,scaledgrid,"%s %s %s %s") 


##run model

mod = model.run_damocles_wrap()


##post processing...get the spectra
#run plotting script here


outfile = "/home/maria/orbyts-damocles/damocles/output/integrated_line_profile.out"
wav,vel,flux = fn.datafile_2_array(outfile,isint=False,zipped=True)

plt.plot(vel,flux,label="arbitrary")
plt.legend()
plt.show(block=True)
#'''

