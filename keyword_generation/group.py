import pandas as pd

csv = pd.read_csv("final_with_keywords.csv")

output = {}

blacklist = ["dni", "only", "med", "godzinach porannych"]

for i, row in csv.iterrows():
    timestamp = row["Timestamp"].split("-")
    year = timestamp[2]
    month = timestamp[1]
    if year not in output:
        output[year] = {}
    if month not in output[year]:
        output[year][month] = {}
    for keyword in str(row["Keywords"]).split("\n"):
        if keyword in blacklist:
            continue
        if keyword not in output[year][month]:
            output[year][month][keyword] = 0
        output[year][month][keyword] += 1

csv_out = pd.DataFrame()

for year in output.keys():
    for month in output[year].keys():
        best_kw = ''
        best_kw_occurencies = 0
        for keyword in output[year][month]:
            occurencies = output[year][month][keyword]
            if occurencies > best_kw_occurencies:
                best_kw = keyword
                best_kw_occurencies = occurencies
        print(
            f"Best keyword for period {month}-{year} is \"{best_kw}\" with {best_kw_occurencies} occurs")
        dataframe_dict = pd.DataFrame(
            {"Year": year, "Month": month, "Keyword": best_kw, "Occurs": best_kw_occurencies}, index=[0])
        csv_out = pd.concat([csv_out, dataframe_dict], ignore_index=True)
csv_out.to_csv("final_grouped.csv")
