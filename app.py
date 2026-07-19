import os

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

app = Flask(__name__)

# ==========================================
# AZURE AI FOUNDRY CONFIG
# ==========================================

#ENDPOINT = os.getenv("FOUNDRY_ENDPOINT")
ENDPOINT = "https://course-chatbot-demo-01-resource.services.ai.azure.com/api/projects/course-chatbot-demo-01"

MODEL_NAME = "gpt-4.1"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=ENDPOINT,
    api_key=token_provider
)

# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message", "")

    response = client.responses.create(
        model=MODEL_NAME,
        input=user_message
    )

    answer = response.output_text

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)