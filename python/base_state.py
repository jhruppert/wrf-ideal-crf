# Script to write out base state file needed for write_qvar_vint.py
#
# This script leverages the CDO (https://code.mpimet.mpg.de/projects/cdo/) module
# via subprocess (executes as a terminal command) to generate basic time series, which
# helps for checking for RCE. This should be available either by loading as a module or
# installing into the conda/mamba kernel you're running.
#
# James Ruppert  
# 21 April 2024

# from netCDF4 import Dataset
import subprocess
from read_wrf_ideal import *


### Directories and model output files

test_process='ctl'
# test_process='xcrf'

# wrfdir = "/glade/derecho/scratch/ruppert/wrf-ideal/largedom2/"
wrfdir = "/glade/campaign/univ/uokl0049/ideal/largedom2/"+test_process+"/"
workdir = "/glade/work/ruppert/wrf-ideal/"
wrftag = "wrfout_d01"
hftag = "hfout_d01"

figdir = "/glade/u/home/ruppert/figures/wrf-ideal/"

# WRFOUT files
wrffiles = get_wrf_file_list(wrfdir, wrftag)


### Generate base state file

basestate_file = " "+workdir+'python/largedom_base_state.nc'

# Generate mean base state file for single time step (doesn't change)
# First remove file if exists
process = subprocess.Popen(['rm -f '+basestate_file], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
# Generate file
process = subprocess.Popen(['cdo fldavg -selname,PHB,PB -seltimestep,1 '+wrffiles[0]+basestate_file], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
lines = process.stdout.readlines()
for iline in lines:
    print(iline)
