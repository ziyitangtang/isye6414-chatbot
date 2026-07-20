import os

from flask import Flask, render_template, request, jsonify
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

app = Flask(__name__)

# ==========================================
# AZURE AI FOUNDRY CONFIG
# ==========================================

# ENDPOINT = os.getenv("FOUNDRY_ENDPOINT")
ENDPOINT = "https://course-chatbot-demo-01-resource.services.ai.azure.com/api/projects/course-chatbot-demo-01"

project_client = AIProjectClient(
    endpoint=ENDPOINT,
    credential=DefaultAzureCredential(),
)

AGENT_NAME = "GT-course-assistant"
AGENT_VERSION = "22"

openai_client = project_client.get_openai_client()

# MODEL_NAME = "gpt-4.1"

# token_provider = get_bearer_token_provider(
#     DefaultAzureCredential(),
#     "https://ai.azure.com/.default"
# )

# client = OpenAI(
#     base_url=ENDPOINT,
#     api_key=token_provider
# )

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

        response = openai_client.responses.create(
            input=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            extra_body={
                "agent_reference": {
                    "name": AGENT_NAME,
                    "version": AGENT_VERSION,
                    "type": "agent_reference"
                }
            }
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
