from download import download_var
from process import process_month, merge_months

start = 2019
end = 2020

years = [1980,1981,1982,2015]

for j in years:
    for i in range(1,13):
        month = i
        if j == 1982 and i <= 7:
            download_var(i,j)
        process_month(i,j)
    merge_months(j)

