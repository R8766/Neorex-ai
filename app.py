from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# -------------------------------
# SAFE AI CALL
# -------------------------------
def get_ai(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
        )

        data = response.json()

        if "choices" not in data:
            return ""

        return data["choices"][0]["message"]["content"]

    except Exception:
        return ""


# -------------------------------
# CLEAN OUTPUT
# -------------------------------
def clean_output(text):
    if not text:
        return ""

    text = text.replace("1.", "\n1.")
    text = text.replace("2.", "\n2.")
    text = text.replace("3.", "\n3.")
    text = text.replace(". ", ".\n")

    return text.strip()


# -------------------------------
# MAIN ROUTE
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/agent", methods=["POST"])
def agent():
    data = request.json
    task = data.get("task", "")
    task_lower = task.lower().strip()

    if not task:
        return jsonify({"error": "No task provided"}), 400

    # =====================================================
    # 🤖 SMART IDENTITY MATCHING (FIXED)
    # =====================================================

    if any(q in task_lower for q in ["who are you", "what are you", "what is your name", "what's your name", "your name", "tell me your name"]):
        return jsonify({
          "planner": "I am Neorex AI 🤖",
          "tutor": "A smart multi-agent assistant designed to help you learn, plan, and grow.",
          "motivation": "Built to support your learning journey 🚀"
        })
    
    if any(q in task_lower for q in ["who is renu", "who is she", "who is renu wakode"]):
        return jsonify({
            "planner": "Renu Wakode is the developer of Neorex AI.",
            "tutor": "She is a student passionate about AI, software development, and building real-world projects.",
            "motivation": "She believes in learning by building 🚀"
        })

    if any(q in task_lower for q in [
    "who made you",
    "who created you",
    "your creator",
    "who built you",
    "creator",
    "developer"
    ]):
      return jsonify({
          "planner": "Neorex AI was created by Renu Wakode.",
          "tutor": "It is a student-built AI assistant focused on learning and productivity.",
          "motivation": "Built with consistency, curiosity, and passion 🚀"
        })

    if "neorex" in task_lower:
        return jsonify({
            "planner": "Neorex AI is your personal AI assistant.",
            "tutor": "It helps with learning, coding, planning, and productivity.",
            "motivation": "Built to make learning smarter 🚀"
        })

    # =====================================================
    # 🤖 NORMAL AI FLOW
    # =====================================================

    planner = get_ai(f"""
    You are a strict AI Planner.
    Give ONLY 3 points.
    Each point must be on a new line.

    Task: {task}
    """)

    tutor = get_ai(f"""
    You are a Tutor AI.
    Explain simply in short points.
    Each idea on new line.

    Task: {task}
    """)

    motivation = get_ai(f"""
    You are a Motivation AI.
    Give 2 short powerful lines.

    Task: {task}
    """)

    return jsonify({
        "planner": clean_output(planner),
        "tutor": clean_output(tutor),
        "motivation": clean_output(motivation)
    })


if __name__ == "__main__":
    app.run(debug=True)