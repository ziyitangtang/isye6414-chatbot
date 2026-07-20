import os

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://course-chatbot-demo-01-resource.openai.azure.com/openai/v1"
)

# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.json.get("message", "")

        print("STEP 1: got message")

        response = client.responses.create(
            model="gpt-4.1",
            input=user_message
        )

        print("STEP 2: got response")

        answer = response.output_text

        print("STEP 3: extracted text")

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ERROR TYPE:", type(e))
        print("ERROR REPR:", repr(e))

        return jsonify({
            "answer": f"ERROR: {repr(e)}"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
