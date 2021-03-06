
#only works with python2.7

import os
import damocleslib as model
import numpy as np
import matplotlib.pyplot as plt
import sys
import fileinput

import FUNCTIONS as fn 
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,Button


#get directory root
path = os.path.dirname(os.path.realpath(__file__))
print(path)



is_obsfile = True






##########################################                            #############################################
##########################################  PARAMETERS WE'RE VARYING  #############################################
##########################################                            #############################################

#INITIAL PARAMETERS THAT MAKE OUR GRID OF GAS

v_max_init=7000.0 #maximum velocity at edge of shell
Rrat_init = 0.3 #radius of inner shell boundary divided by ratio of outer shell. Determines how 'thick' your gas shell is
rho_index_init=2   #density is proportional to radius^(-rho_index)
mdust_init=0         #mass of dust in solar masses
grain_size_init=0.01    #size of dust grain in microns



#put in the wavelength of the spectral line transition you want to create a model of in NANOMETRES
#set this to true if you're modelling a doublet (two close together lines that have blended into each other like O2+ 4959,5007)
doublet= "false"
wavelength_peak_1= 656.3
#set this to 0 if you don't have a doublet
wavelength_peak_2= 0


### age and dust parameters, these are also fed into model 
#age of supernova remnant at the time that observational data was taken, in days.
#this is important because the older the supernova is, the larger its radius would be as its had more time to expand. A larger supernova means you need more dust to get the same amount of light being absorbed

age_d = 1000                                    #INSERT AGE HERE!!!
##no of grid cells in x,y,z direction. higher grid number means higher
grid_divs = 20
photno = 70000


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

#Replace values in files in input.in fortran file with values defined in this script


fi = fileinput.FileInput(files=(input_file,dust_file,gas_file,spec_file),inplace=True)
for line in fi:
   if 'day' in line:
       line=replace_str(age_d,0,line)
   if  'number of photons' in line:
       line=replace_str(photno,0,line)
   if 'doublet?' in line:
       line=replace_str(doublet,0,line)
   if 'Msun' in line:
       line=replace_str(mdust_init,0,line)
   if "first doublet component" in line:
       line=replace_str(wavelength_peak_1,0,line)
   if "second doublet component" in line:
       line=replace_str(wavelength_peak_2,0,line)
   if  'dustData' in line:
       line=replace_str(grain_size_init,3,line)
       line=replace_str(grain_size_init,4,line)
   
   print line,   

fi.close()






#creating a gridfile of the supernova here
#where we have 4 1d arrays; a list of x,y,z and density points
#this allows us to plot what the model looks like 


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

  
	return plotx,ploty,plotz,plotdens


#clear the subplots here





fig2 = plt.figure(2,figsize=(10,10))
plt.xlabel("Velocity km/s")
plt.ylabel("Brightness")

resetax = plt.axes([0.25, 0.0, 0.65, 0.04])
button = Button(resetax, 'Clear')
plt.subplots_adjust(left=0.25, bottom=0.25)

ax = fig2.add_subplot(111)
ax.set_xlim([-10000,10000])
#ax.set_ylim([0,3])

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
	ax.set_xlim([-3e17,3e17])
	ax.set_ylim([-3e17,3e17])
	ax.set_zlim([-3e17,3e17])
	ax.set_title("Model of O2+ gas distribution in a Supernova")



setax()
x,y,z,d = make_Grid(v_max_init,Rrat_init,rho_index_init)


#legend tells you params
#param_label = "vmax: "+str(v_max_init)+","+"Rrat: "+str(Rrat)+","+"rho_index: "+str(rho_index) dont need label as we have sliders
l = ax.scatter(x,y,z,c=d,cmap="nipy_spectral")
cbar = fig.colorbar(l)
cbar.set_label('density', rotation=270)




ax_vmax = plt.axes([0.25, 0.0, 0.65, 0.02])
ax_r = plt.axes([0.25, 0.05, 0.65, 0.02])
ax_rho = plt.axes([0.25, 0.1, 0.65, 0.02])
ax_dm = plt.axes([0.25, 0.15, 0.65, 0.02])
ax_gs = plt.axes([0.25, 0.2, 0.65, 0.02])

s_vmax = Slider(ax_vmax, 'vmax', 1000, 10000,valinit=v_max_init)
s_r = Slider(ax_r, 'Rin/Rout', 0.001, 1,valinit=Rrat_init)
s_rho = Slider(ax_rho, 'rho index', 0.001, 3,valinit=rho_index_init)
s_dm = Slider(ax_dm, 'dustmass', 0.0, 0.0005,valfmt='%9.7f',valinit=mdust_init)
s_gs = Slider(ax_gs, 'grain size', 0.005, 0.5,valinit=grain_size_init)




def update(val):
  #plt.cla()
  newv = s_vmax.val
  newr = s_r.val
  newrho = s_rho.val
  newdm = s_dm.val
  newgs	= s_gs.val
  
  
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
	if 'Total dust mass' in lineo:
  	     lineo=replace_str(newdm,0,lineo)
        print lineo,  

  fi2.close()

  fi3 = fileinput.FileInput(files=(spec_file),inplace=True)
  for lineo in fi3:	
       if  'dustData' in lineo:
          lineo=replace_str(newgs,3,lineo)
          lineo=replace_str(newgs,4,lineo)
       print lineo,  

  fi3.close()

  mod = model.run_damocles_wrap()    

  outfile = path + "/output/integrated_line_profile.out"
  wav,vel,flux = fn.datafile_2_array(outfile,isint=False,zipped=True)
  
  
  
  

  def reset(event):
    plt.cla()
  button.on_clicked(reset)

  obs_file = path +"/2012aw-2017-cc"
  obswav,obsflux= fn.datafile_2_array(obs_file,isint=False,zipped=True)


  obsvels = fn.convert_wav_to_vel(obswav,6582,6563)



  obsvels,obsflux = fn.trim_wav_flux(obsvels,obsflux,-12000,12000)
  obsflux = fn.snip_spect(obsvels,obsflux,-188,362,601,1286)

  
  scale = np.amax(flux)/np.nanmax(obsflux)
  obsflux = [(i*scale) for i in obsflux]	
  print(np.amax(flux),np.nanmax(obsflux))
  plt.figure(2)
  plt.plot(vel,flux)
  plt.plot(obsvels,obsflux)
      
 
	
  plt.xlabel("Velocity km/s")
  plt.ylabel("Brightness")
         
  
	
  fig2.canvas.draw()

 
  
  

s_vmax.on_changed(update)
s_r.on_changed(update)
s_rho.on_changed(update)
s_dm.on_changed(update)
s_gs.on_changed(update)




plt.show()
#'''
