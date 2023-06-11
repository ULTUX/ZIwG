import yake

kw_ext = yake.KeywordExtractor(lan="pl", n=4, dedupLim=0.01, dedupFunc='seqm')
text = "Witam. Jestem w 8 tyg ciąży i na USG wyszło że mam bardzo grubą pępowine. Dzidziuś mierzy 7mm a pępowina 5mm. Lekarz tylko tyle mi powiedział że jest za gruba i trzeba ją obserwowac. Może któraś mama miała taki przypadek i powie mi coś więcej na ten temat czy jest to niebespieczne i jakie mogą wystąpic komplikacje?"
content = "Dzień dobry,Dzisiaj otrzymałem wyniki ze szpitala. Oddział laryngologiczny - pobierany był wycinek z nosogardła. Niestety wynik jest dla mnie niezrozumiały a mój lekarz prowadzący jest na urlopie i wizytę mam dopiero za 3 tygodnie. Bardzo proszę o interpretację wyników:Rozpoznanie patomorfologiczne: Fragmenty tkanki limfatycznej. (M-09450 T-23000)Opis makroskopowy: Nieregularny fragment tkankowy o wymiarach 0,9x0,7x0,3 cm.Bardzo proszę o informacjeSerdecznie pozdrawiam"
keywords = kw_ext.extract_keywords(content)
print(keywords)
