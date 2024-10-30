# Notebook to read WRF high-frequency output and write out vertically integrated q-variables.
# 
# This script leverages the CDO (https://code.mpimet.mpg.de/projects/cdo/) module via subprocess (executes as a terminal command) to generate basic time series, which helps for checking for RCE. This should be available either by loading as a module or installing into the conda/mamba kernel you're running.
# 
# James Ruppert  
# 21 April 2024

from netCDF4 import Dataset
import numpy as np
from matplotlib import ticker, colors, rc
import matplotlib.pyplot as plt
from wrf import interplevel#, getvar, disable_xarray, ALL_TIMES
import subprocess
import pandas as pd
from scipy import interpolate
from read_wrf_ideal import *
import sys

# ## Main Settings

# Small domain model time specs
npd_wrf = 48 # time steps per day
npd_hf = 288 # time steps per day
# npfile = npd # time steps per output file
nd=50 # total n-days of small-domain run

# Vertical interpolation settings
dp_int = 20 # hPa
top_p = 100

# #### Directories and model output files

# test='ctl'
test='xcrf'

# wrfdir = "/glade/derecho/scratch/ruppert/wrf-ideal/largedom2/"
wrfdir = "/glade/campaign/univ/uokl0049/ideal/largedom2/"+test+"/"
workdir = "/glade/work/ruppert/wrf-ideal/"

figdir = "/glade/u/home/ruppert/figures/wrf-ideal/"

# High-frequency (HFOUT) files
hftag = "hfout_d01"
hffiles, times = get_wrf_file_list(wrfdir, hftag)
print(times)
sys.exit()
# Add a time step for corrected file
# nd_corrected = nd+1
# hffiles=hffiles[:nd_corrected]

# ## Conduct vertical integration

# #### NetCDF variable write function

def write_vars(outfile,q_int):

    file_out = outfile
    ncfile = Dataset(file_out,mode='w', clobber=True)

    nq = np.shape(q_int)[0]
    nq, nt, nx1, nx2 = q_int.shape

    q_dim = ncfile.createDimension('nq', nq)
    time_dim = ncfile.createDimension('nt', nt) # unlimited axis (can be appended to).
    x1_dim = ncfile.createDimension('nx1', nx1)
    x2_dim = ncfile.createDimension('nx2', nx2)

    q_int_nc = ncfile.createVariable('q_int', np.single, ('nq','nt','nx1','nx2',))
    q_int_nc.units = 'mm'
    q_int_nc.long_name = 'vertically integrated hydrometeor variables, calculated as 1/g(int)dp'
    q_int_nc[:,:,:,:] = q_int[:,:,:,:]

    ncfile.close()


gaccel=9.81 # m/s2

# Read base state variables
basestate_file = " "+workdir+'python/largedom_base_state.nc'
base_state_nc = Dataset(basestate_file)
p_base = base_state_nc.variables['PB'][:,:,:,:] # Pa
z_base = base_state_nc.variables['PHB'][:,:,:,:]/gaccel # m2/s2 --> m
base_state_nc.close()

shape_i = p_base.shape
p_base = np.reshape(p_base, (1,shape_i[1],1,1))
shape_i = z_base.shape
z_base = np.reshape(z_base, (1,shape_i[1],1,1))

# Output pressure levels
plevs_out = np.arange(1000, top_p-dp_int, -dp_int) # hPa

q_list = ['QCLOUD', 'QRAIN', 'QICE', 'QSNOW', 'QGRAUP']
nq = len(q_list)

for ifil in hffiles:
# for ifil in hffiles[20:21]:

    print()
    print("Processing: ",ifil)

    fileread_nc = Dataset(ifil)

    try:
        times_file = fileread_nc.dimensions['Time'].size # deg
    except:
        times_file = fileread_nc.dimensions['Times'].size # deg

    # q_int_write = np.zeros((nq, times_file, nx1, nx2))

    # for it in range(times_file):
    # for it in range(1,5):
        # print('IT: ',it)
    p_pert = varfil_main.variables['P'][:,:,:,:] # Pa
    p_tot = p_pert + p_base

    q_int_write = []
    for iqvar in range(nq):
        qvar = varfil_main.variables[q_list[iqvar]][:,:,:,:] # kg/kg
        qvar_interp = interplevel(qvar, p_tot*1e-2, plevs_out)
        q_int_write.append(np.sum(qvar_interp, axis=1)*dp_int/gaccel)

    outfile = wrfdir+'hfout_qint_'+ifil[-23:]
    write_vars(outfile, np.array(q_int_write))

    fileread_nc.close()
