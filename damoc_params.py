
#only works with python2.7

import os
import damocleslib as model
import numpy as np
import matplotlib.pyplot as plt
import sys
import fileinput

import FUNCTIONS as fn   ##THIS IS FROM PACKAGE ON MY COMP, MAKE FUNCTIONS AVAILABLE...
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider




##########################################                            #############################################
##########################################  PARAMETERS WE'RE VARYING  #############################################
##########################################                            #############################################

#INITIAL PARAMETERS THAT MAKE OUR GRID OF GAS
v_max_init=7000.0 #maximum velocity at edge of shell
Rrat_init = 0.3 #radius of inner shell boundary divided by ratio of outer shell. Determines how 'thick' your gas shell is
rho_index_init=2   #density is proportional to radius^(-rho_index)



#put in the wavelength of the spectral line transition you want to create a model of in NANOMETRES
#set this to true if you're modelling a doublet (two close together lines that have blended into each other like OIII 4959,5007)
doublet= "false"
wavelength_peak_1= 500.7
#set this to 0 if you don't have a doublet
wavelength_peak_2= 0


### age and dust parameters, these are also fed into model 
#dust is coupled to gas
age=1000         #in years
mdust=1          #mass of dust in solar masses
grain_size=0.01    #size of dust grain in microns



age_d = age*365
age_s = 3.154e7

##no of grid cells in x,y,z direction
grid_divs = 20




###HERE WE'RE PUTTING IN THE PARAMETERS WE SET ABOVE INTO THE CODE, FEEDING THEM INTO THE INPUT FILES
#Read in input files as arrays
input_file = "input/input.in"
dust_file = "input/dust.in"
gas_file = "input/gas.in"
spec_file = "input/species.in"
inlines = fn.datafile_2_array(input_file,isint=False,zipped=False)
dustlines = fn.datafile_2_array(dust_file,isint=False,zipped=False)
gaslines = fn.datafile_2_array(gas_file,isint=False,zipped=False)
speclines = fn.datafile_2_array(spec_file,isint=False,zipped=False)

#USED in conjuction with the fileinput module, which then allows the changes we make to string to be printed back into the file
def replace_str(value,place,linetally):
    
        x = linetally.split()
        x[place] = str(value)
        newx = ' '.join(x)
        string = newx + '\n'
        return string

'''
#Replace values in files in input.in fortran file with values defined in this script

fi = fileinput.FileInput(files=(input_file,dust_file,gas_file,spec_file),inplace=True)
for line in fi:
   if 'day' in line:
       line=replace_str(age_d,0,line)
   if 'doublet?' in line:
       line=replace_str(doublet,0,line)
   if 'Msun' in line:
       line=replace_str(mdust,0,line)
   if "first doublet component" in line:
       line=replace_str(wavelength_peak_1,0,line)
   if "second doublet component" in line:
       line=replace_str(wavelength_peak_2,0,line)
   if  'dustData' in line:
       line=replace_str(grain_size,3,line)
       line=replace_str(grain_size,4,line)
   
   print line,   

fi.close()
'''






#creating a gridfile of the supernova here
#where we have 4 1d arrays; a list of x,y,z and density points


def make_Grid(v_max,Rrat,rho_index):
	
	v_min = v_max * Rrat
	Rout = v_max * age_d * 8.64e-6 * 1e15
	Rin = v_min* age_d * 8.64e-6 * 1e15
      
        #grid divisions for a uniform grid
	grid_arr = np.linspace(-Rout,Rout,grid_divs)

        #These values contain every point in a 40*40*40 grid from the limits of -Rout,Rout 
	Y,X,Z = np.meshgrid(grid_arr,grid_arr,grid_arr) 
        #turning these into 1d arrays
	Xf = X.flatten()
	Yf = Y.flatten()  
	Zf = Z.flatten()
	rads= [np.sqrt(Xf[i]**2 + Yf[i]**2 + Zf[i]**2) for i in range(len(Xf))]

	rho = np.zeros((len(Xf)))


	plotdens,plotx,ploty,plotz = [],[],[],[]

	#looping through radius of every grid point.
	#if rad is within Rout and Rin, set density using r^-(rho_index) law
	for j in range(len(rads)):
	    if abs(rads[j]) <= Rout and abs(rads[j]) >= Rin:
	        if Xf[j] > 0 and Yf[j] > 0 and Zf[j] > 0:
	            rho[j] = (abs(rads[j]))**(-rho_index)*1e20   #randomly rescaling the density to make it a reasonable number
	        else:
	           
	            rho[j] = (abs(rads[j]))**(-rho_index)*1e20
	            plotdens.append(rho[j])
	            plotx.append(Xf[j])
	            ploty.append(Yf[j])
	            plotz.append(Zf[j])

        '''
        ############## saving grid here to dust_grid.in file to be used as the gas density distrib in the damocles model
	outfile = "input/dust_grid.in"
	title_1 = (v_max,Rout/(1e+15), 1.0, '!vmax (km/s),rmax (e15 cm), v(r) index')
	title_2 = ('#', grid_divs,grid_divs,grid_divs)

	print(title_1)
	scaledgrid = list(zip(Xf,Yf,Zf,rho))
	scaledgrid.insert(0,title_2)
	scaledgrid.insert(0,title_1)
            
	x = np.savetxt(outfile,scaledgrid,"%s %s %s %s") 
        ###############
        '''
	return plotx,ploty,plotz,plotdens


#clear the subplots here

#if fig doesnt exist , then plot this, otherwise clear the existing subplot

fig2 = plt.figure(2,figsize=(10,10))

#set axis labels
fig = plt.figure(1,figsize=(15,15))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.25)



#function contains axis orientation, limits and labels
def setax():
	ax.view_init(elev=30, azim=50)
	ax.set_xlabel('X axis (cm)')
	ax.set_ylabel('Y axis (cm)')
	ax.set_zlabel('Z axis (cm)')
	ax.set_xlim([-2.3e19,2.3e19])
	ax.set_ylim([-2.3e19,2.3e19])
	ax.set_zlim([-2.3e19,2.3e19])
	ax.set_title("Model of O2+ gas distribution in a Supernova")



setax()
x,y,z,d = make_Grid(v_max_init,Rrat_init,rho_index_init)


#legend tells you params
#param_label = "vmax: "+str(v_max_init)+","+"Rrat: "+str(Rrat)+","+"rho_index: "+str(rho_index) dont need label as we have sliders
l = ax.scatter(x,y,z,c=d,cmap="nipy_spectral")
cbar = fig.colorbar(l)
cbar.set_label('density', rotation=270)




ax_vmax = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_r = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_rho = plt.axes([0.25, 0.2, 0.65, 0.03])
s_vmax = Slider(ax_vmax, 'vmax', 1000, 10000,valinit=v_max_init)
s_r = Slider(ax_r, 'Rin/Rout', 0.001, 1,valinit=Rrat_init)
s_rho = Slider(ax_rho, 'rho index', 0.001, 3,valinit=rho_index_init)




def update(val):
  #plt.cla()
  newv = s_vmax.val
  newr = s_r.val
  newrho = s_rho.val
  print(newr)
  
  #using the updated parameters, remake the grid points and save this grid to dust_grid.in file 
  x,y,z,d = make_Grid(newv,newr,newrho)
  
  plt.figure(1)
  ax.clear()
  setax()
  l= ax.scatter(x,y,z,c=d,cmap="nipy_spectral") # update the plot
  
  #writing values we've updated to shell version of damocles as something is going wrong in the code w. arbitrary setting
  fi2 = fileinput.FileInput(files=(dust_file),inplace=True)
  for lineo in fi2:	
  	if 'max dust velocity' in lineo:
  	     lineo=replace_str(newv,0,lineo)
  	if 'Rin/Rout' in lineo:
  	     lineo=replace_str(newr,0,lineo)
  	if 'rho~r^-q' in lineo:
  	     lineo=replace_str(newrho,0,lineo)
        print lineo,  

  fi2.close()

  mod = model.run_damocles_wrap()    

  
  outfile = "/home/maria/orbyts-damocles/damocles/output/integrated_line_profile.out"
  wav,vel,flux = fn.datafile_2_array(outfile,isint=False,zipped=True)
  plt.figure(2)
  plt.plot(vel,flux)
  fig2.canvas.draw()
 
  
  

s_vmax.on_changed(update)
s_r.on_changed(update)
s_rho.on_changed(update)



plt.show()

