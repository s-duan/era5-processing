from process import process_month, merge_months

years = [i for i in range (2010,2021)]

for yr in years:
    for month in range(1,13):
        print(f"processing {month}/{yr}")
        process_month(month,yr)
    print(f"merging yr")
    merge_months(yr)

