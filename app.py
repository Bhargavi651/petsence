from flask import Flask, request, render_template, jsonify
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_msg}]
    )
    return jsonify({"reply": response.choices[0].message["content"]})

@app.route('/nearby', methods=['POST'])
def nearby():
    data = request.json
    lat, lng, place_type = data["lat"], data["lng"], data["type"]
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,
        "type": place_type,
        "key": GOOGLE_API_KEY
    }
    res = requests.get(url, params=params)
    return jsonify(res.json()["results"])

if __name__ == "__main__":
    app.run(debug=True)
