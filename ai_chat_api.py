from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import openai
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Allow frontend to access this API

# 🔧 Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Excel file from your GitHub repo
EXCEL_URL = "https://raw.githubusercontent.com/fareed-007/dia-gmdf-webapp-tool/main/Export_File/Data_for_AI-Model.xlsx"

def load_excel_data():
    """Load Excel file from GitHub and return as DataFrame."""
    response = requests.get(EXCEL_URL)
    df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
    return df

@app.route("/ask", methods=["POST"])
def ask():
    """Receive question and return AI-generated answer based on Excel data."""
    question = request.json.get("question")
    df = load_excel_data()
    context = df.to_string()

    prompt = f"""
    You are an assistant that answers questions based on the following Excel data:
    {context}

    Question: {question}
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
    app.run(debug=True)
