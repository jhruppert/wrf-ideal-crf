# Read functions for WRF-ideal simulations.
# 
# James Ruppert
# 15 Oct 2024

import netCDF4 as nc
import numpy as np
import subprocess
import subprocess

# Read WRF file list
def get_wrf_file_list(filedir, tag):
    process = subprocess.Popen(['ls '+filedir+tag+'_*'],shell=True,
        stdout=subprocess.PIPE,universal_newlines=True)
    files = process.stdout.readlines()
    for ifile in range(len(files)):
        files[ifile] = files[ifile].strip()
    # times = get_times_wrffiles(files)
    return files#, times

def get_times_wrffiles(files):
    # def slicer_vectorized(a,start,end):
    #     b = a.view((str,1)).reshape(len(a),-1)[:,start:end]
    #     return np.frombuffer(b.tobytes(),dtype=(str,end-start))
    for ifile in range(len(files)):
        files[ifile] = files[ifile].strip()
        filenc=nc.Dataset(files[ifile])
        char_var = filenc.variables['Time']
        # try:
        #     char_var = filenc.variables['Time']
        # except:
        #     char_var = filenc.variables['Times']
        try:
            itime = nc.chartostring(char_var[:])
            itime = [t.replace("_", "T") for t in itime]  # Replace underscore with space
        except:
            if char_var.shape[0] == 1:
                split = files[ifile].split('_')
                itime = split[-2]+'T'+split[-1]
            else:
                print('Need another fix here')
        filenc.close()
        itime_dt = np.array(itime, dtype='datetime64[m]')
        if ifile == 0:
            times_sav=itime_dt
        else:
            try:
                times_sav=np.concatenate((times_sav, itime_dt))
            except:
                times_sav=np.concatenate((times_sav, itime_dt[np.newaxis]))
    return times_sav