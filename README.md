# ISYE 6414 Course Assistant

Student-facing chatbot built using:

- Azure AI Foundry
- Azure App Service
- Azure OpenAI GPT-4.1
- Course Knowledge Base

## Local Run

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:8000
```

## Azure Environment Variable

Set:

```text
FOUNDRY_ENDPOINT
```

Example:

```text
https://your-foundry-endpoint/openai/v1/
```