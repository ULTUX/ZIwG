import pandas as pd
import os

dataset = pd.read_csv("final_dataset.csv")

for root, dirs, files in os.walk("keywords"):
    for filename in files:
        id = filename.replace(".txt", "")
        with open(f"keywords/{filename}") as file:
            keywords = file.read()
            dataset.loc[dataset["ID"] == int(id), "Keywords"] = keywords

dataset.to_csv("final_with_keywords.csv")
print(dataset)
