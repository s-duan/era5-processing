from pathlib import Path
import os
import glob
import xarray as xr
import numpy as np
import pandas as pd

PROJ_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJ_DIR / "data" / "raw"
PROC_DIR = PROJ_DIR / "data" / "processed"

def process_month(month,year):
    pattern = os.path.join(RAW_DIR,f"{year}",f"era_{year}_{month:02d}_*.nc")
    ncfiles = sorted(glob.glob(pattern))

    ds = xr.open_mfdataset(
        ncfiles,
        combine="by_coords",
        engine="h5netcdf"
    )

    # combine low and high vegetation
    total_lai = (ds['lai_hv']*ds['cvh']) +  (ds['lai_lv']*ds['cvl'])
    ds['lai'] = total_lai

    # mask out sea
    precip = ds['tp'] * ds['lsm']
    ds['tp'] = precip

    # Save Month Data
    output_file = RAW_DIR / f"era_{year}_{month:02d}.nc"
    encoding = {var: {"zlib": True, "complevel": 5} for var in ds.data_vars}
    ds.to_netcdf(output_file, engine="h5netcdf", encoding=encoding)
    ds.close()
  
def merge_months(year):
    month_files = sorted(RAW_DIR.glob(f"era_{year}_??.nc"))

    ds_year = xr.open_dataset(month_files[0], engine="h5netcdf")

    for month_file in month_files[1:]:
        ds_month = xr.open_dataset(month_file, engine="h5netcdf")
        ds_year = xr.concat([ds_year, ds_month],dim="time")
        ds_month.close()

    yearly_file = PROC_DIR / f"era5_{year}.nc"
    encoding = {var: {"zlib": True, "complevel": 5} for var in ds_year.data_vars}
    ds_year.to_netcdf(yearly_file, engine="h5netcdf", encoding=encoding)

