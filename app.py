import os
import random
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

MOVES = ["rock", "paper", "scissors"]


def decide_winner(user_move, bot_move):
    if user_move == bot_move:
        return "draw"
    wins_against = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if wins_against[user_move] == bot_move:
        return "user"
    return "bot"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Something type pannunga da!"})

    user_move = None
    lowered = user_message.lower()
    for move in MOVES:
        if move in lowered:
            user_move = move
            break

    if user_move:
        bot_move = random.choice(MOVES)
        result = decide_winner(user_move, bot_move)

        if result == "draw":
            outcome_text = f"Draw! Naanum {bot_move} thaan podren."
        elif result == "user":
            outcome_text = f"Nee jeichitinga! Nee {user_move}, naan {bot_move} pottutten."
        else:
            outcome_text = f"Naan jeichitten! Naan {bot_move}, nee {user_move} pottinga."

        return jsonify({"reply": outcome_text})

    response = model.generate_content(user_message)
    return jsonify({"reply": response.text})


if __name__ == "__main__":
    app.run(debug=True)
