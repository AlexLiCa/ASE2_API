from flask import Flask, request, jsonify
import os
import openai
import json
from flask_cors import CORS
#from dotenv import load_dotenv
import re

# Carga las variables de entorno desde el archivo .env
# load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") # Colocacion de la nueva llave
# a = os.getenv("OPENAI_API_KEY") 

app = Flask(__name__)
CORS(app)

# print(f"Llave: {a}")

def busca_prompt(language, text):
    with open("pr.json", 'r') as archivo:
        idiomas = json.load(archivo)

    if language in idiomas:
        pr = idiomas[language]
        prompt = pr.format(text=text)
    else:
        prompt = None
    return prompt

def create_json(text):
    lineas = text.split('\n')
    informacion = {}
    informacion = {"grade": "", "pointers": [], "ct": ""}
    for i,linea in enumerate(lineas):
        palabras = linea.split()
        #print(linea)
        if len(palabras) >= 2:
            patron = r'\b(?!-)\d+\b'
            match = re.findall(patron, linea)
            texto = re.search(r'"(.*?)"', linea)
            if match:
                informacion['grade'] = palabras[-1]
            elif palabras[0] == "-": 
                consejo = " ".join(palabras)
                informacion['pointers'].append(consejo)
            elif texto:
                texto_corregido = texto.group(1)
                informacion["ct"] = texto_corregido
            else:
                text = " ".join(palabras)
                parts = text.split(":")
                informacion["ct"] = parts[-1]

    return informacion

def correcciones(text, lan):
    pr = busca_prompt(lan, text)
    if pr is not None:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": pr},
            ],
            max_tokens = 100,
            temperature = 0.9
            )
        res = create_json(completion.choices[0].message.content)
        print(completion.choices[0].message.content)
    else:
        res = {"Invalid": "Non supported Language"}

    return res

@app.route('/api/v1/', methods=['POST'])
def process():
    data = request.get_json()
    text = data['text']
    lan = data["lan"]
    #print("entro algo")
    return jsonify(correcciones(text, lan))

if __name__ == '__main__':
    app.run(debug=True)
    print("Adios")