# wrf-ideal-crf
Repo containing modified WRF code and analysis code for conducting convection-permitting idealized RCE simulations.

Using WRFv4.5.2

WRF modifications:
- mediation_integrate.F:
    1. updated this so that when write_hist_at_0h_rst = True, this will apply to all output streams (only applies to the main wrfout_ stream in the default WRF).
    2. XX (didn't work, revsered the change) took a fix from the wrf-help forum that resolves an issue where WRF prematurely completes when using adaptive time stepping.
- module_sf_sfclay.F: tested adding a minimum 1 m/s wind speed for surface flux calculation, but according to results (plotted in surface_flux_test.ipynb), it really had no impact, so retracted this and using the default.
- module_radiation_driver.F: added code to homogenize 3D shortwave and longwave radiative tendencies.
- XX (didn't work, revsered the change) adapt_timestep_em.F: took a fix from the wrf-help forum that resolves an issue where WRF prematurely completes when using adaptive time stepping.
