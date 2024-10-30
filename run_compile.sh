#!/bin/bash

export wrfdir="/glade/work/ruppert/wrf-ideal/WRF"
cd $wrfdir

source ../bashrc_wrf_der

./clean -a
# configure #50
mv configure.wrf.backup configure.wrf
./compile -j 6 em_convrad > compile.out 2>&1 &
