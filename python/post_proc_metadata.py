# Metadata for processing WRF output: reads raw WRF output files and writes to new files
# with a single file per variable, with all time steps in the same file.
# 
# James Ruppert
# jruppert@ou.edu
# 1 Nov 2024

##########################################
# Full variable lists
##########################################

def proc_var_list():
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
    return out_var_names_3d, out_var_names_2d

##########################################
# Get metadata for a single variable
##########################################

def get_metadata(var_name, nt, nz, nx1, nx2):

    # 2D variables
    if var_name == 'pclass':
        description = 'cloud classification (0 = nocloud,1=deepc,2=congest,3=shall,4=strat,5=anvil)'
        units = '-'
        dims = ('nt',6,'nx1','nx2')
        dim_set = [(dims[0],'pclass',dims[1],dims[2]), (nt,6,nx1,nx2)]
    elif var_name == 'rain':
        description = 'rain rate (centered diff)'
        units = 'mm/day'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'hfx':
        description = 'surface sensible heat flux'
        units = 'W/m^2'
        dims = ('nt','nx1','nx2')
        dim_set = [dims, (nt,nx1,nx2)]
    elif var_name == 'lh':
        description = 'surface latent heat flux'
        units = 'W/m^2'
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

    # 3D variables
    elif var_name == 'qv':
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
    elif var_name == 'mse':
        description = 'moist static energy'
        units = 'J/kg'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'tmpk':
        description = 'temperature'
        units = 'K'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'hght':
        description = 'height'
        units = 'm'
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
    elif var_name == 'rthratlwcrf':
        description = 'longwave cloud-radiation forcing'
        units = 'K/s'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]
    elif var_name == 'rthratswc':
        description = 'shortwave heating rate, clear sky'
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
    elif var_name == 'rho':
        description = 'density'
        units = 'kg/m^3'
        dims = ('nt','nz','nx1','nx2')
        dim_set = [dims, (nt,nz,nx1,nx2)]

    return description, units, dim_set

##########################################
# 
##########################################
