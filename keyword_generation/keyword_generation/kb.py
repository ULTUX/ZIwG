import os
from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
from sentence_transformers import SentenceTransformer

# print(torch.cuda.is_available())
# flair.device = torch.device('cuda:0')

stopwords = []
with open("polish.stopwords.txt") as file:
    stopwords = file.read().splitlines()

# doc = input()

# stopwords.append("jakiegoś")
# stopwords.append("najprawdopodobniej")
# stopwords.append("chociaz")
# stopwords.append("tj")

pl_model = TransformerDocumentEmbeddings("Voicelab/sbert-large-cased-pl")
pl_model2 = SentenceTransformer("distiluse-base-multilingual-cased-v1")
pl_model_roberta = TransformerDocumentEmbeddings("radlab/polish-roberta-large-v2-sts")
pl_model3 = "paraphrase-multilingual-MiniLM-L12-v2"

kw_model = KeyBERT(model=pl_model3)
# keywords = kw_model.extract_keywords(doc, highlight=True, stop_words=stopwords, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=25, top_n=3)

content = "Dzień dobry,Dzisiaj otrzymałem wyniki ze szpitala. Oddział laryngologiczny - pobierany był wycinek z nosogardła. Niestety wynik jest dla mnie niezrozumiały a mój lekarz prowadzący jest na urlopie i wizytę mam dopiero za 3 tygodnie. Bardzo proszę o interpretację wyników:Rozpoznanie patomorfologiczne: Fragmenty tkanki limfatycznej. (M-09450 T-23000)Opis makroskopowy: Nieregularny fragment tkankowy o wymiarach 0,9x0,7x0,3 cm.Bardzo proszę o informacjeSerdecznie pozdrawiam"
weights = kw_model.extract_keywords(content, keyphrase_ngram_range=(1,3), use_maxsum=True, nr_candidates=25, top_n=3)
print(weights)
# for root, dir, files in os.walk("content/"):
#     for filename in files:
#         with open(f"content/{filename}") as file:
#             content = file.read()
#             keywordsWithWeights = kw_model.extract_keywords(content, stop_words=stopwords, keyphrase_ngram_range=(1,3), use_maxsum=True, nr_candidates=25, top_n=3)
#             keywords = [i[0] for i in keywordsWithWeights]
#             filekeywords = "\n".join(keywords)
#             with open(f"keywords/{filename}", "w") as outfile:
#                 outfile.write(filekeywords)
#             print(f"{content}\nKeywords: {', '.join(keywords)}")
#         print("Processed file")


# print(keywords)
