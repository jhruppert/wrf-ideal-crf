# Metadata for processing WRF output: reads raw WRF output files and writes to new files
# with a single file per variable, with all time steps in the same file.
# 
# James Ruppert
# jruppert@ou.edu
# 1 Nov 2024

from read_wrf_ideal import *
import numpy as np
from precip_class import *
from thermo_functions import *

##########################################
# Write out variable to a NetCDF file
##########################################

def write_ncfile(file_out, var, var_name, description, units, dims_set, pres=None, do_pres=False): #, dim_names
    ncfile = Dataset(file_out,mode='w', clobber=True)
    # Add dimensions to file
    for idim in range(len(dims_set)):
        dim = ncfile.createDimension(dims_set[0][idim], dims_set[1][idim]) # unlimited axis (can be appended to).
    if do_pres:
        pres_nc = ncfile.createVariable('Pressure', np.single, len(pres))
        pres_nc.units = 'hPa'
        pres_nc[...] = pres
    # Write variables
    writevar = ncfile.createVariable(var_name, np.single, dims_set[0])
    writevar.units = units
    writevar.description = description
    writevar[...] = var
    ncfile.close()
    return None

##########################################
# Calculate cloud classification
##########################################

def wrf_pclass(infile, dp):
    # Read in and vertically integrate mixing ratios
    q_list = ['QCLOUD', 'QRAIN','QICE', 'QSNOW', 'QGRAUP']
    q_var = []
    for ivar in range(len(q_list)):
        ivar = wrf_var_read(infile,q_list[ivar]) # kg/kg
        q_var.append(ivar)
    q_var = np.stack(q_var, axis=0)
    g = 9.81 # m/s^2
    q_int = np.sum(q_var*dp, axis=1)/(-g)
    return precip_class(q_int)

##########################################
# Calculate precipitable water (PW)
##########################################

def wrf_pw(infile, dp):
    # Read in hydrostatic pressure to get dp for integral
    p_hyd = wrf_var_read(infile,'P_HYD') # Pa
    # p_hyd = np.ma.masked_where((p_hyd < 100e2), p_hyd, copy=False) # Mask out levels above 100 hPa
    dp = np.gradient(p_hyd, axis=0, edge_order=1) # [Pa] Uses second order centered differencing
    # Read in and vertically integrate mixing ratios
    qv = wrf_var_read(infile, 'QVAPOR') # kg/kg
    g = 9.81 # m/s^2
    return np.sum(qv*dp, axis=1)/(-g)

##########################################
# Calculate saturation PW
##########################################

def wrf_pw_sat(infile, p_hyd, dp):
    T0 = 300 # K
    rd=287.04 # J/K/kg
    cp=1004. # J/K/kg
    rocp = rd/cp
    theta = wrf_var_read(infile,'T') + T0 # K
    tmpk = theta*(1e5/p_hyd)**(-rocp) # K
    # Read in and vertically integrate mixing ratios
    qv_sat = rv_saturation(tmpk, p_hyd) # kg/kg
    g = 9.81 # m/s^2
    return np.sum(qv_sat*dp, axis=1)/(-g)

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

def get_metadata(var_name, nt, nz, nx1, nx2):

    #######################################################
    # Basic 2D variables
    #######################################################
    if var_name == 'hfx':
        description = 'surface sensible heat flux'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lh':
        description = 'surface latent heat flux'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwupt':
        description = 'upward longwave flux at top of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swupt':
        description = 'upward shortwave flux at top of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwuptc':
        description = 'upward longwave flux at top of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swuptc':
        description = 'upward shortwave flux at top of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwupb':
        description = 'upward longwave flux at bottom of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swupb':
        description = 'upward shortwave flux at bottom of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwupbc':
        description = 'upward longwave flux at bottom of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swupbc':
        description = 'upward shortwave flux at bottom of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwdnt':
        description = 'downward longwave flux at top of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swdnt':
        description = 'downward shortwave flux at top of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwdntc':
        description = 'downward longwave flux at top of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swdntc':
        description = 'downward shortwave flux at top of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwdnb':
        description = 'downward longwave flux at bottom of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swdnb':
        description = 'downward shortwave flux at bottom of atmosphere'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lwdnbc':
        description = 'downward longwave flux at bottom of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swdnbc':
        description = 'downward shortwave flux at bottom of atmosphere, clear sky'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    #######################################################
    # Special 2D variables
    #######################################################
    elif var_name == 'lwacre':
        description = 'longwave column ACRE'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'swacre':
        description = 'shortwave column ACRE'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'pclass':
        description = 'cloud classification (0 = nocloud,1=deepc,2=congest,3=shall,4=strat,5=anvil)'
        units = '-'
        dims = ('nt',6,'nx1','nx2')
        dim_set = [(dims[0],'pclass',dims[1],dims[2]), (nt,6,nx1,nx2)]
    elif var_name == 'rain':
        description = 'rain rate (centered diff)'
        units = 'mm/day'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'pw':
        description = 'column integrated water vapor'
        units = 'mm'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'pw_sat':
        description = 'column integrated saturation water vapor'
        units = 'mm'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    #######################################################
    # Basic 3D variables
    #######################################################
    elif var_name == 'qvapor':
        description = 'water vapor mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'qrain':
        description = 'rain water mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'qcloud':
        description = 'cloud water mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'qice':
        description = 'ice water mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'qsnow':
        description = 'snow mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'qgraupel':
        description = 'graupel mixing ratio'
        units = 'kg/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'u':
        description = 'zonal wind'
        units = 'm/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'v':
        description = 'meridional wind'
        units = 'm/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'w':
        description = 'vertical velocity'
        units = 'm/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'condh':
        description = 'condensation heating'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratlw':
        description = 'longwave heating rate'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratsw':
        description = 'shortwave heating rate'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratlwc':
        description = 'longwave heating rate, clear sky'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratswc':
        description = 'shortwave heating rate, clear sky'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    #######################################################
    # Special 3D variables
    #######################################################
    elif var_name == 't':
        description = 'temperature'
        units = 'K'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'hght':
        description = 'height'
        units = 'm'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratlwcrf':
        description = 'longwave cloud-radiation forcing'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratswcrf':
        description = 'shortwave cloud-radiation forcing'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'theta_e':
        description = 'equivalent potential temperature'
        units = 'K'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'mse':
        description = 'moist static energy'
        units = 'J/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rho':
        description = 'density'
        units = 'kg/m^3'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]

    return description, units, dim_set

##########################################
# 
##########################################
