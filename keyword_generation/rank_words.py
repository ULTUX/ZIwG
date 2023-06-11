import pandas as pd

input_data = pd.read_csv("final_with_keywords.csv")

occurs = {}
all = 0


for i, d in input_data.iterrows():
    kws = str(d["Keywords"]).split("\n")
    for kw in kws:
        if kw not in occurs:
            occurs[kw] = 0
        occurs[kw] += 1
        all += 1
# for i in occurs.keys():
#     occurs[i] /= all

occurs = list(reversed(sorted(occurs.items(), key=lambda item: item[1])))

keywords = ['dzieci', 'ciąży', 'zawroty głowy', 'ból']

kw_occurs = {}
kw_all = {}

for i, d in input_data.iterrows():
    kws = str(d["Keywords"]).split("\n")
    timestamp = d["Timestamp"].split("-")
    year = timestamp[2]
    month = timestamp[1]
    if year not in kw_all:
        kw_all[year] = {}
    if month not in kw_all[year]:
        kw_all[year][month] = 0
    kw_all[year][month] += 1
    for kw in kws:
        kw_lower = kw.lower()
        if kw_lower in keywords:
            if year not in kw_occurs:
                kw_occurs[year] = {}
            if month not in kw_occurs[year]:
                kw_occurs[year][month] = {}
            if kw_lower not in kw_occurs[year][month]:
                kw_occurs[year][month][kw_lower] = 0
            kw_occurs[year][month][kw_lower] += 1

dataframes = {}
for kw in keywords:
    dataframes[kw] = pd.DataFrame()

for year in kw_occurs.keys():
    in_year = kw_occurs[year]
    for month in in_year.keys():
        in_month = in_year[month]
        for kw in in_month.keys():
            in_month[kw] /= kw_all[year][month]
            dataframes[kw] = pd.concat([dataframes[kw], pd.DataFrame(
                {"Timestamp": "-".join([year, month]), "Occurs": in_month[kw]}, index=[0])], ignore_index=True)

for kw in dataframes.keys():
    df = dataframes[kw]
    df.to_csv(f"{kw}-aggregated.csv")
