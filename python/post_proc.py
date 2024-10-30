# Script to post-process high-resolution WRF model output.

# Major tasks include computing the following for selected variables:
#   1. domain-averages to produce time series
#   2. vertical integrals
#   3. pressure-level vertical interpolation

from netCDF4 import Dataset
import numpy as np
from matplotlib import ticker, colors, rc
import matplotlib.pyplot as plt
from wrf import getvar, disable_xarray, ALL_TIMES

npd=24*2 # time steps per day
nd_avg=20 # n-days to average over
sst=300 # K, this is the prescribed SST for the model simulation

#### Directories and model output specs
datdir = "/glade/derecho/scratch/ruppert/wrf-ideal/smalldom/"
wrffile = datdir+"wrfout_d01_2007-06-01_00:00:00"

figdir = "/glade/u/home/ruppert/figures/wrf-ideal/"

disable_xarray()

# def get_dims_files(wrffile):
wrffile_read = Dataset(wrffile)

# General specs
nt_file = wrffile_read.dimensions['Time'].size
# times = wrffil_read.variables['Times']
lat = wrffile_read.variables['XLAT'][:][0] # deg
lon = wrffile_read.variables['XLONG'][:][0] # deg
lat1d = lat[:,0]
lon1d = lon[0,:]
nx1 = lat1d.size
nx2 = lon1d.size
nz = wrffile_read.dimensions['bottom_top'].size
# pres = wrffil_read.variables['PB'][0,:,0,0]*1e-2 # Pa --> hPa

# Main variables
nt_read = np.min([nt_file, npd*nd_avg])
nt_read=5

# Need to loop over time steps (uggghh)
# dims2d=(nt_read,nx1,nx2)
# dims3d=(nt_read,nz,nx1,nx2)

# psfc_sav = np.zeros(dims2d)
# # T-sfc is prescribed SST
# qv2m_sav = np.zeros(dims2d) # 2-m mixing ratio (model will use saturation surface value for fluxes)

# z_sav = np.zeros(dims3d)
# th_sav = np.zeros(dims3d)
# qv_sav = np.zeros(dims3d)
# # u_sav = np.zeros(dims)
# # v_sav = np.zeros(dims)

# for it in range(nt_read):
#     psfc_sav[it,...] = getvar(wrffile_read, 'slp', units="hPa", timeidx=nt_file-nt_read+it) # hPa
#     qv2m_sav[it,...] = getvar(wrffile_read, 'Q2', timeidx=nt_file-nt_read+it)*1e3 # kg/kg --> g/kg
#     z_sav[it,...] = getvar(wrffile_read, 'z', units="m", timeidx=nt_file-nt_read+it) # m
#     th_sav[it,...] = getvar(wrffile_read, 'th', units="K", timeidx=nt_file-nt_read+it) # K
#     qv_sav[it,...] = getvar(wrffile_read, 'QVAPOR', timeidx=nt_file-nt_read+it)*1e3 # kg/kg --> g/kg
#     # u_sav[it,...] = getvar(wrffile_read, 'ua', timeidx=nt_file-nt_read+it)
#     # v_sav[it,...] = getvar(wrffile_read, 'va', timeidx=nt_file-nt_read+it)

# psfc_sav = np.ma.mean(psfc_sav)
# qv2m_sav = np.ma.mean(qv2m_sav)
# z_sav = np.ma.mean(z_sav, axis=(0,2,3))
# th_sav = np.ma.mean(th_sav, axis=(0,2,3))
# qv_sav = np.ma.mean(qv_sav, axis=(0,2,3))

# # Variables for complete time series
# # olr = getvar(wrffile_read, 'OLR', timeidx=ALL_TIMES) # W/m2
# # pw = getvar(wrffile_read, 'pw', timeidx=ALL_TIMES) # mm
# # precip = getvar(wrffile_read, 'RAINNC', timeidx=ALL_TIMES) # mm

# # Rain rate as centered difference
# # for it in range(1,nt_file-1):
# #     precip[it,...] = (precip[it+1,...] - precip[it-1,...]) * 0.5 # mm / time step
# # precip[nt_file-1,...] = np.nan
# # precip *= npd/24 # mm/dt --> mm/hr

# # psfc_sav = np.ma.mean(psfc_sav, axis=(1,2))
# # qv2m_sav = np.ma.mean(qv2m_sav, axis=(1,2))

# # olr = np.ma.mean(olr, axis=(1,2))
# # pw = np.ma.mean(pw, axis=(1,2))
# # precip = np.ma.mean(precip, axis=(1,2))

wrffile_read.close()