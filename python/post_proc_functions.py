# Metadata for processing WRF output: reads raw WRF output files and writes to new files
# with a single file per variable, with all time steps in the same file.
# 
# James Ruppert
# jruppert@ou.edu
# 1 Nov 2024

import xarray as xr
from read_wrf_ideal import *
import numpy as np
from precip_class import *
from thermo_functions import *

##########################################
# Miscellaneous functions
##########################################

def vert_int(var, rho, dz):
    return np.sum(var*rho*dz, axis=1)

##########################################
# Write out variable to a NetCDF file
##########################################

def write_ncfile(file_out, dummyvar, var, var_name):#, dims_set, pres=None, do_pres=False): #, dim_names
    description, units = get_metadata(var_name)
    var = xr.DataArray(var, coords=dummyvar.coords, dims=dummyvar.dims, attrs=dummyvar.attrs, name=var_name)
    var.attrs['description'] = description
    var.attrs['units'] = units
    var.attrs['projection'] = str(dummyvar.attrs['projection'])
    var.to_netcdf(file_out)
    return None

##########################################
# Calculate cloud classification
##########################################

# def wrf_pclass(infile, dp):
def wrf_pclass(infile, rho, dz):
    # Read in and vertically integrate mixing ratios
    q_list = ['QCLOUD', 'QRAIN','QICE', 'QSNOW', 'QGRAUP']
    q_var = []
    for ivar in range(len(q_list)):
        ivar = wrf_var_read(infile,q_list[ivar]) # kg/kg
        q_var.append(ivar)
    q_var = np.stack(q_var, axis=0)
    q_int = np.sum(q_var*rho*dz, axis=2)
    return precip_class(q_int)

##########################################
# Full variable lists
##########################################

# 3D variables
def var_list_3d():
    return [
        # Variables that can be directly interpolated
        'qvapor',
        # 'qrain',
        # 'qcloud',
        # 'qice',
        # 'qsnow',
        # 'qgraupel',
        # 'u',
        # 'v',
        'w',
        'condh',
        'rthratlw',
        'rthratsw',
        'rthratlwc',
        'rthratswc',
        # Variables that require special care
        # 't',
        # 'hght',
        # 'rthratlwcrf',
        # 'rthratswcrf',
        # 'theta_e',
        # 'mse',
        # 'rho',
        ]

# 2D variables
def var_list_2d():
    return [
        # Variables that can be processed via CDO
        'hfx',
        'lh',
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
        # Variables that require special care
        # 'lwacre',
        # 'swacre',
        # 'pclass',
        # 'rain',
        # 'pw',
        # 'pw_sat',
        ]

##########################################
# Get variable metadata
##########################################

def get_metadata(var_name):#, nt, nz, nx1, nx2):

    #######################################################
    # Special 2D variables
    #######################################################
    if var_name == 'pclass':
        description = 'cloud classification (0 = nocloud,1=deepc,2=congest,3=shall,4=strat,5=anvil)'
        units = '-'
        # dims = ('nt','pclass','nx1','nx2')
        # dim_set = [dims, (nt,6,nx1,nx2)]
    elif var_name == 'rainrate':
        description = 'rainrate (centered diff)'
        units = 'mm/day'
        # dims = ('nt','nx1','nx2')
        # dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'pw':
        description = 'column integrated water vapor'
        units = 'mm'
        # dims = ('nt','nx1','nx2')
        # dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'pw_sat':
        description = 'column integrated saturation water vapor'
        units = 'mm'
        # dims = ('nt','nx1','nx2')
        # dim_set = [dims, (nt,nx1,nx2)]
    #######################################################
    # Basic 3D variables
    #######################################################
    # elif var_name == 'qvapor':
    #     description = 'water vapor mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'qrain':
    #     description = 'rain water mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'qcloud':
    #     description = 'cloud water mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'qice':
    #     description = 'ice water mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'qsnow':
    #     description = 'snow mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'qgraupel':
    #     description = 'graupel mixing ratio'
    #     units = 'kg/kg'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'u':
    #     description = 'zonal wind'
    #     units = 'm/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'v':
    #     description = 'meridional wind'
    #     units = 'm/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'w':
    #     description = 'vertical velocity'
    #     units = 'm/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'condh':
    #     description = 'condensation heating'
    #     units = 'K/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'rthratlw':
    #     description = 'longwave heating rate'
    #     units = 'K/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'rthratsw':
    #     description = 'shortwave heating rate'
    #     units = 'K/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'rthratlwc':
    #     description = 'longwave heating rate, clear sky'
    #     units = 'K/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'rthratswc':
    #     description = 'shortwave heating rate, clear sky'
    #     units = 'K/s'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    #######################################################
    # Special 3D variables
    #######################################################
    # elif var_name == 't':
    #     description = 'temperature'
    #     units = 'K'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'hght':
    #     description = 'height'
    #     units = 'm'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratlwcrf':
        description = 'longwave cloud-radiation forcing'
        units = 'K/s'
        # dims = ('nt','nz','nx1','nx2')
        # dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratswcrf':
        description = 'shortwave cloud-radiation forcing'
        units = 'K/s'
        # dims = ('nt','nz','nx1','nx2')
        # dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'theta_e':
        description = 'equivalent potential temperature'
        units = 'K'
        # dims = ('nt','nz','nx1','nx2')
        # dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'mse':
        description = 'moist static energy'
        units = 'J/kg'
        # dims = ('nt','nz','nx1','nx2')
        # dim_set = [dims, (nt,nz,nx1,nx2)]
    # elif var_name == 'rho':
    #     description = 'density'
    #     units = 'kg/m^3'
    #     dims = ('nt','nz','nx1','nx2')
    #     dim_set = [dims, (nt,nz,nx1,nx2)]

    return description, units#, dim_set

##########################################
# 
##########################################
