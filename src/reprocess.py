from process import process_month, merge_months

years = [i for i in range (2010,2011)]

for yr in years:
    for month in range(1,13):
        process_month(month,yr)
    merge_months(yr)

