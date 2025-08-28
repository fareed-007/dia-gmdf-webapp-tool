from flask import Flask, request, jsonify
import pandas as pd
import openai
import requests
from io import BytesIO
import os

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"
EXCEL_URL = "https://raw.githubusercontent.com/fareed-007/dia-gmdf-webapp-tool/main/Data_for_AI-Model.xlsx"

def load_excel_data():
    response = requests.get(EXCEL_URL)
    excel_data = pd.read_excel(BytesIO(response.content))
    return excel_data

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    df = load_excel_data()
    context = df.to_string()

    prompt = f"""
    You are an assistant that answers questions based on the following Excel data:
    {context}

    Question: {user_question}
    Answer:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response['choices'][0]['message']['content']
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Fix for Railway
    app.run(host="0.0.0.0", port=port)
