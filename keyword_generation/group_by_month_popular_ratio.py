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
        if year not in kw_occurs:
            kw_occurs[year] = {}
        if month not in kw_occurs[year]:
            kw_occurs[year][month] = {}
        if kw_lower not in kw_occurs[year][month]:
            kw_occurs[year][month][kw_lower] = 0
        kw_occurs[year][month][kw_lower] += 1

return_kws = {}
csv_out = ""
for year in kw_occurs.keys():
    by_year = kw_occurs[year]
    for month in by_year.keys():
        by_month = by_year[month]
        max_occurs_kw = ''
        max_occurs = 0
        for kw in by_month.keys():
            occurs = by_month[kw]
            if occurs > max_occurs:
                max_occurs = occurs
                max_occurs_kw = kw
        if year not in return_kws:
            return_kws[year] = {}
        if month not in return_kws[year]:
            return_kws[year][month] = {}
        return_kws[year][month][max_occurs_kw] = max_occurs / kw_all[year][month]
        csv_out += f"{month}-{year},{max_occurs_kw},{return_kws[year][month][max_occurs_kw]},{max_occurs},{kw_all[year][month]}\n"
with open("most_popular_keywords_per_month.csv", "w", encoding='utf-8') as file:
    file.write("Timestamp,Keyword,Occurs/All,Occurs,All\n")
    file.write(csv_out)
