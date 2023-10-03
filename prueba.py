from flask import Flask, request, jsonify
import os
import openai
from flask_cors import CORS
from pprint import pprint
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") # Colocacion de la nueva llave
a = os.getenv("OPENAI_API_KEY") 

print(f"Llave: {a}")

def correcciones(text):
    pr = f"Revisa el texto {text}. Dame una calificación del 0.0-10. Dame en forma de lista de puntos ideas que tengas para mejorar mi redacción después de cada texto incluyendo faltas en signos de puntuación .Dame solo la calificación, los puntos para mejorar la redacción y el texto corregido"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=pr,
        temperature=0.4,
        max_tokens=1500,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    tips_text = response.choices[0].text.strip()
    pprint(response)

    return tips_text

correcciones("ola me yamo alex")