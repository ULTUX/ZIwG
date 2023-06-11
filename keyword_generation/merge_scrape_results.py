import pandas as pd
from datetime import datetime
import re


def prepareContent(x: str):
    x = x.strip()
    x = x.replace("\n", " ")
    x = re.sub("\s\s+", " ", x)
    words = x.split()[:350]
    return " ".join(words)


medyczka = pd.read_csv("dataset/filtered_medyczka.csv")
forumed = pd.read_csv("dataset/forummed.csv")
ilekarze = pd.read_csv("dataset/test.csv")
ilekarze["Source"] = "ilekarze.pl"


output = pd.DataFrame()
output.insert(0, "Source", pd.concat([medyczka["source"], forumed["Source"], ilekarze["Source"]]))
output.insert(1, "Timestamp", pd.concat([medyczka["date"], forumed["Timestamp"], ilekarze["Date"]]))
output.insert(2, "Title", pd.concat([medyczka["title"], forumed["Title"], ilekarze["Topic"]]))
output.insert(3, "Content", pd.concat([medyczka["content"], forumed["Content"], ilekarze["Content"]]))

output["Content"] = output["Content"].apply(lambda x: prepareContent(str(x)))

output["ID"] = output.reset_index().index
output: pd.DataFrame = output.reindex(columns=['ID', 'Source', 'Title', 'Content', 'Timestamp'])
output = output.sample(frac=1)

output.to_csv("merged.csv", index=False)
