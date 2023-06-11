import pandas as pd
import os

dataset = pd.read_csv("final_dataset.csv")
for index, row in dataset.iterrows():
    if index <= 2000:
        continue
    id = row["ID"]
    content = row["Content"]
    with open(os.path.join("content", f"{id}.txt"), "w") as file:
        if type(content) is str:
            file.write(content)
        else:
            print(f"Found content that is not string, id: {id}, content: {content}, skipping...")
