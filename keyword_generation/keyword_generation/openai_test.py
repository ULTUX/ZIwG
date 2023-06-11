import openai
from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Wyciągnij słowa kluczowe: \nMagnez kurcze mięśni łydek i ud.\nWynik:",
  temperature=0,
  max_tokens=60,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)
