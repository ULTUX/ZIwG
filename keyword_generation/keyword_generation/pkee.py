import pke
import os

stopwords = []
with open("polish.stopwords.txt") as file:
    stopwords = file.read().splitlines()

extractor = pke.unsupervised.TopicRank()

for root, dir, files in os.walk("content/"):
    for filename in files:
        with open(f"content/{filename}") as file:
            content = file.read()

            extractor.load_document(
                stoplist=stopwords, input=content, language='pl', normalization='stemming')
            extractor.candidate_selection()
            extractor.candidate_weighting()
            keywordsWithWeights = extractor.get_n_best(3)

            keywords = [i[0] for i in keywordsWithWeights]
            filekeywords = "\n".join(keywords)
            with open(f"keywords/{filename}", "w") as outfile:
                outfile.write(filekeywords)
            print(f"Content: {content}\nKeywords: {', '.join(keywords)}")
            print("Processed file")
