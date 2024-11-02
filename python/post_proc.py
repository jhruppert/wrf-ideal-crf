# Script to post-process high-resolution WRF model output.

# Major tasks include computing the following for selected variables:
#   1. domain-averages to produce time series
#   2. vertical integrals
#   3. pressure-level vertical interpolation

import numpy as np
from wrf import getvar, disable_xarray, ALL_TIMES
from read_wrf_ideal import *
from post_proc_metadata import *
import os

# disable_xarray()

test_process = "ctl"

#### Directories and model output specs

datdir = "/glade/derecho/scratch/ruppert/wrf-ideal/smalldom/"
wrfdir = "/glade/campaign/univ/uokl0049/ideal/largedom2/"+test_process+"/"
outdir = wrfdir+"post_proc/"
os.makedirs(outdir, exist_ok=True)

# # Get WRF file list, dimensions
wrftag = "wrfout_d01"
wrffiles = get_wrf_file_list(wrfdir, wrftag)
lat, lon, nx1, nx2, nz = wrf_dims(wrffiles[0])

# New vertical dimension for pressure levels
dp = 25 # hPa
pres = np.arange(1000, 25, -dp)
nznew = len(pres)

# Get variable list
vars2d = var_list_2d()

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

# wrffile_read.close()