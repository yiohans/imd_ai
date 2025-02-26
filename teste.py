from dotenv import load_dotenv

from MultiAgent import MultiAgents


load_dotenv()

models = {
    "supervisor": {
        "provider": "groq",
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.0
        },
    "agent": {
        "provider": "groq",
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.0
        },
}

agents = MultiAgents(models)
inputs = {
    "messages": [
        {
            "role": "user",
            "content": "Olá, gostaria de saber se o processo 203/2025 existe. Liste os 5 primeiros documentos."
        }
    ],
}

response = agents.run(inputs)
for msgs in response['messages']:
    print(msgs.name, msgs.content)

