from process import process_month, merge_months

years = [i for i in range (1980,2011)]

for yr in years:
    for month in range(1,13):
        print(f"processing {month}/{yr}")
        process_month(month,yr)
    print(f"merging yr")
    merge_months(yr)

