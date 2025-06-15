from flask import request, jsonify, current_app
from openai import OpenAI

from . import shambabot_bp


@shambabot_bp.route("/chat", methods=["POST"])
def handle_chat():
    """
    Handles incoming chat messages and returns a JSON response.
    """
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "Please send a valid message."}), 400

    try:
        client = OpenAI(
            api_key=current_app.config.get("OPENAI_API_KEY", ""),
            organization=current_app.config.get("OPENAI_ORGANIZATION", ""),
            project=current_app.config.get("OPENAI_PROJECT", ""),
        )

        system_prompt = "You are Shamba Bot, an expert farming assistant for a platform called Shamba Salama. You will be used by farmers in Western Kenya. Answer the following user question clearly and concisely."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        print("OpenAI Error:", e)
        return (
            jsonify({"response": "Sorry, there was an error processing your request."}),
            500,
        )
