import xarray as xr
import os
from pathlib import Path

PROC_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

filename = "era5_2010.nc"
filepath = os.path.join(PROC_DIR, filename)
ds = xr.open_dataset(filepath)
print(ds.data_vars)
