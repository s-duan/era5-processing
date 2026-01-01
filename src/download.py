from pathlib import Path
import os
import calendar
import cdsapi
import configparser

RAW_DIR = Path(__file__).resolve().parents[1]/"data"/"raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

c = cdsapi.Client()
dataset = "derived-era5-single-levels-daily-statistics"

mean_variables = [
    "10m_u_component_of_wind",      # u10
    "10m_v_component_of_wind",      # v10
    "2m_dewpoint_temperature",      # d2m
    "2m_temperature",               # t2m
    "surface_pressure",             # sp
    "geopotential",                 # z
    "land_sea_mask",                # lsm
    "leaf_area_index_high_vegetation", # lai_hv
    "leaf_area_index_low_vegetation",  # lai_lv
    "low_vegetation_cover",         # cvl
    "high_vegetation_cover",        # cvh
]
sum_variables = [
    "total_precipitation",          # tp
]

v = {
    "10m_u_component_of_wind": "u10",
    "10m_v_component_of_wind": "v10",
    "2m_dewpoint_temperature": "d2m",
    "2m_temperature": "t2m",
    "surface_pressure": "sp",
    "geopotential": "z",
    "land_sea_mask": "lsm",
    "leaf_area_index_high_vegetation": "lai_hv",
    "leaf_area_index_low_vegetation": "lai_lav",
    "low_vegetation_cover": "cvl",
    "high_vegetation_cover": "cvh",
    "total_precipitation": "tp"
}


def download_era(var, month, year, stat):
    filename = RAW_DIR / f"{year}" / f"era_{year}_{month:02}_{v[var]}.nc"
    
    c.retrieve(
            dataset,
            {
            "product_type": "reanalysis",
            "variable": var,
            "year": f"{year}",
            "month": [f"{month:02d}"],
            "day": [f"{d:02d}" for d in range(1, calendar.monthrange(year, month)[1] + 1)],
            "daily_statistic": f"daily_{stat}",
            "time_zone": "utc+00:00",
            "frequency": "1_hourly",
            "area": [51.69, -125, 24.0, -66.5],
            },
            str(filename)
        )
def download_var(month,year):
    new_folder = os.path.join(RAW_DIR, f"{year}")
    os.makedirs(new_folder, exist_ok=True)
    for mv in mean_variables:
        download_era(mv,month,year,'mean')
    for sv in sum_variables:
        download_era(sv,month,year,'sum')
