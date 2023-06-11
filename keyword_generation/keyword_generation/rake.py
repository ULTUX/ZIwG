from rake_nltk import Rake
import nltk

nltk.download("stopwords")
nltk.download("punkt")

r = Rake(language="polish")

text = """
Uczenie maszynowe jest konsekwencją rozwoju idei sztucznej inteligencji i metod jej wdrażania praktycznego. Dotyczy rozwoju oprogramowania stosowanego zwłaszcza w innowacyjnych technologiach i przemyśle. Odpowiednie algorytmy mają pozwolić oprogramowaniu na zautomatyzowanie procesu pozyskiwania i analizy danych do ulepszania i rozwoju własnego systemu.
Uczenie się może być rozpatrywane jako konkretyzacja algorytmu, czyli dobór parametrów, nazywanych wiedzą lub umiejętnością. Służy do tego wiele typów metod pozyskiwania wiedzy oraz sposobów reprezentowania wiedzy
"""
content = "Dzień dobry,Dzisiaj otrzymałem wyniki ze szpitala. Oddział laryngologiczny - pobierany był wycinek z nosogardła. Niestety wynik jest dla mnie niezrozumiały a mój lekarz prowadzący jest na urlopie i wizytę mam dopiero za 3 tygodnie. Bardzo proszę o interpretację wyników:Rozpoznanie patomorfologiczne: Fragmenty tkanki limfatycznej. (M-09450 T-23000)Opis makroskopowy: Nieregularny fragment tkankowy o wymiarach 0,9x0,7x0,3 cm.Bardzo proszę o informacjeSerdecznie pozdrawiam"
r.extract_keywords_from_text(content)

print(r.get_ranked_phrases_with_scores())

