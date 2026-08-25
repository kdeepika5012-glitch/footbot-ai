from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not set in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter your food or cooking question."
            })

        prompt = f"""
You are FoodBot AI, a helpful Food and Cooking Assistant.

You can answer questions related to:

- Cooking
- Recipes
- Indian food
- South Indian food
- North Indian food
- Tamil cuisine
- Breakfast
- Lunch
- Dinner
- Snacks
- Desserts
- Vegetarian food
- Non-vegetarian food
- Baking
- Ingredients
- Cooking methods
- Kitchen tips
- Food substitutions
- Meal planning
- Healthy cooking basics
- Food storage
- Cooking measurements

Rules:

1. Give simple and practical cooking instructions.
2. For recipes, provide ingredients and step-by-step preparation.
3. Mention approximate cooking time when useful.
4. Give ingredient alternatives when appropriate.
5. Do not invent dangerous food-safety information.
6. Mention basic food-safety precautions when relevant.
7. If the user asks about a medical diet or serious health condition,
   give general information and recommend consulting a qualified
   healthcare professional.
8. The user may ask in English, Tamil, or Thanglish.
9. English question -> English answer.
10. Tamil question -> Tamil answer.
11. Thanglish question -> simple Thanglish answer.
12. Use bullet points and numbered steps when useful.
13. If the question is unrelated to food or cooking, politely say
    that you are a Food and Cooking Chatbot.

User question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        reply = response.text

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )