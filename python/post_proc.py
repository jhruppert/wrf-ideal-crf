# Script to post-process high-resolution WRF model output.

# Major tasks include computing the following for selected variables:
#   1. domain-averages to produce time series
#   2. vertical integrals
#   3. pressure-level vertical interpolation

import numpy as np
from wrf import getvar, disable_xarray, ALL_TIMES
from read_wrf_ideal import *

disable_xarray()

#### Directories and model output specs

test_process = "ctl"

datdir = "/glade/derecho/scratch/ruppert/wrf-ideal/smalldom/"
wrfdir = "/glade/campaign/univ/uokl0049/ideal/largedom2/"+test_process+"/"
outdir = wrfdir+"post_proc/"

wrftag = "wrfout_d01"
wrffiles = get_wrf_file_list(wrfdir, wrftag)
lat, lon, nx1, nx2, nz = wrf_dims(wrffiles[0])

# Variables to process
out_var_names = [
    'pclass_area',
    'rain',
    'qrain',
    'qtotal',
    'pw',
    'pw_sat',
    'vmfu',
    'vmfd',
    'condh',
    'mse_vint',
    'lwacre',
    'swacre',
    'theta_e',
    'w',
    'rho',
]

################################################
#### NetCDF variable metadata

def var_process_metadata(nt,nz,nx1,nx2):

    out_var_names_3d = [
        'qv',
        'qrain',
        'qcloud',
        'qice',
        'qsnow',
        'qgraupel',
        # 'u',
        # 'v',
        'w',
        'condh',
        'mse',
        'tmpk',
        'hght',
        'rthratlw',
        'rthratsw',
        'rthratlwc',
        'rthratlwcrf',
        'rthratswc',
        'rthratswcrf',
        'theta_e',
        'rho',
        ]
    out_var_names_2d = [
        'pclass_area',
        'rain',
        'hfx',
        'lh',
        'pw',
        'pw_sat',
        'lwupt',
        'swupt',
        'lwuptc',
        'swuptc',
        'lwupb',
        'swupb',
        'lwupbc',
        'swupbc',
        'lwdnt',
        'swdnt',
        'lwdntc',
        'swdntc',
        'lwdnb',
        'swdnb',
        'lwdnbc',
        'swdnbc',
        'lwacre',
        'swacre',
        ]

    descriptions = [
        'precip class area',
        'rain rate (centered diff)',
        'column integrated rain water mixr',
        'rain water mixr at lowest vertical level',
        'total integrated hydrometeor mixr',
        'precipitable water (aka CWV)',
        'saturation PW or CWV',
        'upward-masked mass flux vertically integrated (up to 100 hPa)',
        'downward-masked mass flux vertically integrated (up to 100 hPa)',
        'condensation heating from H_DIABATIC vertically int (up to 100 hPa), converted to rainfall units',
        'vertically int moist static energy, calculated as 1/g*integral(mse)dp up to 100 hPa',
        'LW column ACRE',
        'SW column ACRE',
        'equivalent potential temperature',
        'vertical motion',
        'density',
    ]
    units = [
        '%',
        'mm/day',
        'mm',
        'kg/kg',
        'mm',
        'mm',
        'mm',
        'kg/m/s',
        'kg/m/s',
        'mm/day',
        'J/kg',
        'W/m^2',
        'W/m^2',
        'K',
        'm/s',
        'kg/m^3',
    ]
    dims2d = (nt,nx1,nx2)
    dims3d = (nt,nz,nx1,nx2)
    dim_names = ('nt','nx1','nx2')
    dim_names3d = ('nt','nz','nx1','nx2')
    dims_set = [
        [(dim_names[0],'pclass',dim_names[1],dim_names[2]), (dims2d[0],6,dims2d[1],dims2d[2])],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names,dims2d],
        [dim_names3d,dims3d],
        [dim_names3d,dims3d],
        [dim_names3d,dims3d],
    ]

    len1=len(var_names); len2=len(descriptions); len3=len(units); len4=len(dims_set) #len4=len(dim_names)
    if (len1 != len2) or (len1 != len3) or (len1 != len4):
        raise ValueError("Variable info counts are off")

    return var_names, descriptions, units, dims_set

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