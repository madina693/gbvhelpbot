from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

initial_questions = [
    "Do you feel unsafe in your current relationship?",
    "Have you ever been physically hurt by someone close to you?",
    "Has anyone tried to control where you go or who you talk to?",
    "Have you experienced unwanted touching or harassment?",
    "Do you feel emotionally manipulated or constantly blamed?"
]

@app.route("/")
def home():
    return render_template("index.html", questions=initial_questions)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    lang = request.json.get("lang", "en")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and supportive GBV assistant who answers in " + ("Swahili" if lang == "sw" else "English")},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Sorry, something went wrong. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
