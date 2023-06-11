from llama_cpp import Llama
import json


print("loading model...")
llm = Llama(model_path="models/gml-old-vic13b-q5_1.bin")
print("Model loaded")

output = llm("Extract keywords: Na pokładzie zainstalowano dwa kompasy: jeden mokry na rufie, umieszczony w naktuzie i drugi w dziobowej części sterówki, zamknięty w otwartej od dołu skrzyni, którego wskazania można było obserwować także z wnętrza kiosku i z wnętrza kadłuba[33]. W dziobowej części kiosku były umieszczone elektryczne i wodoszczelne światła nawigacyjne w kolorach zielonym i czerwonym. Słowa kluczowe:", max_tokens=100, stop=["\n","Question", "Q:"], echo=True)
print(json.dumps(output, indent=2))

