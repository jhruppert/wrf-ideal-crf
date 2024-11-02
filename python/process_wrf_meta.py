# Metadata for processing WRF output: reads raw WRF output files and writes to new files
# with a single file per variable, with all time steps in the same file.
# 
# James Ruppert
# jruppert@ou.edu
# 1 Nov 2024

def get_metadata(var_name, nt, nz, nx1, nx2):

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