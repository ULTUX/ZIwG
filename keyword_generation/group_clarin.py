import pandas as pd
csv = pd.read_csv("assets/keytool_with_data.csv")

output = {}
output_voicelab = {}
output_clarin = {}
output_textclass = {}
output_ner = {}

#blacklist = ["dni", "only", "med", "godzinach porannych"]


def extract_keywords(keywords, out):
    for keyword in keywords:
        if keyword == "nan" or keyword == "":
            continue
        if keyword not in out:
            out[keyword] = 0
        out[keyword] += 1


for i, row in csv.iterrows():
    timestamp = row["Timestamp"].split("-")
    year = timestamp[2]
    month = timestamp[1]
    if year not in output:
        output[year] = {}
    if month not in output[year]:
        output[year][month] = {}
    if "topicrank" not in output[year][month]:
        output[year][month]["topicrank"] = {}
    if "voicelab" not in output[year][month]:
        output[year][month]["voicelab"] = {}
    if "clarin" not in output[year][month]:
        output[year][month]["clarin"] = {}
    if "textclass" not in output[year][month]:
        output[year][month]["textclass"] = {}
    if "ner" not in output[year][month]:
        output[year][month]["ner"] = {}

    voicelab = output[year][month]["voicelab"]
    clarin = output[year][month]["clarin"]
    textclass = output[year][month]["textclass"]
    ner = output[year][month]["ner"]

    # TopicRank
        # if keyword in blacklist:
        #     continue
    extract_keywords(str(row["Ours"]).split("\n"),output[year][month]["topicrank"])
    # voicelab
    extract_keywords(str(row["Voicelab"]).split("\n"), voicelab)
    extract_keywords(str(row["Clarin"]).split("\n"), clarin)
    extract_keywords(str(row["Textclass"]).split("\n"), textclass)
    extract_keywords(str(row["Ner"]).split("\n"), ner)
    # clarin
print(output)
csv_out = pd.DataFrame()

for year in output.keys():
    for month in output[year].keys():
        keywords = {}
        for alg in output[year][month].keys():
            best_kw = ''
            best_kw_occurencies = 0
            for keyword in output[year][month][alg]:
                if keyword == "nan" or keyword == "":
                    continue
                occurencies = output[year][month][alg][keyword]
                if occurencies > best_kw_occurencies:
                    best_kw = keyword
                    best_kw_occurencies = occurencies
            print(f"Best keyword for period {month}-{year} is \"{best_kw}\" with {best_kw_occurencies} occurs")
            keywords[alg] = best_kw
        out_frame = {"Year": year, "Month": month}
        for k in keywords.keys():
            out_frame[k] = keywords[k]
        dataframe_dict = pd.DataFrame(out_frame, index=[0])
        csv_out = pd.concat([csv_out, dataframe_dict], ignore_index=True)
csv_out.index.name = "ID"
csv_out.to_csv("final_grouped_v3.csv", index=None)
