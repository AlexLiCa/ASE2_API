from flask import Flask, request, jsonify
import os
import openai
from flask_cors import CORS

openai.api_key = os.getenv("OPENAI_API_KEY") # Colocacion de la nueva llave

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def process():
    data = request.get_json()
    text = data['text']

    corrected_text = correct(text)
    grade_text = grade(text)
    tips_text  = tips(text)

    return jsonify({'corrected_text': corrected_text, 'grade_text': grade_text, 'tips_text': tips_text})

def correct(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Correct this to standard Spanish:\n\n{text}",
        temperature=0.5,
        max_tokens=1500,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    corrected_text = response.choices[0].text.strip()
    return corrected_text

def grade(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Asigna una calificación al texto (Excelente, Muy bien, Regular, Malo):\n\n{text}",
        temperature=0.4,
        max_tokens=1500,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    grade_text = response.choices[0].text.strip()
    return grade_text

def tips(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Actua como profesor de español, dame consejos de los errores que se encontraron en el texto:\n\n{text}",
        temperature=0.4,
        max_tokens=1500,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    tips_text = response.choices[0].text.strip()
    return tips_text

def correcciones(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Actua como profesor de español, dame consejos de los errores que se encontraron en el texto:\n\n{text}",
        temperature=0.4,
        max_tokens=1500,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    tips_text = response.choices[0].text.strip()
    return tips_text


if __name__ == '__main__':
    app.run(debug=True)
    print("Adios")



