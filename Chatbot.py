import streamlit as st

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

st.title("💬 Chatbot")
st.caption("Um chatbot para responder perguntas sobre processos no Sistema Eletrônico de Informações (SEI) do Tribunal Regional Eleitoral do Rio Grande do Norte (TRE-RN).")
if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {
            "role": "assistant",
            "content": "Olá! Como posso ajudar você?"
        }
    ]

for msg in st.session_state['messages']:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    st.chat_message("user").write(prompt)
    response = agents.run({"messages": st.session_state['messages']})
    for msgs in response['messages']:
        name = "assistant"
        print(name)
        content = msgs.content
        print(content)
        st.session_state['messages'].append(
           {
                "role": name,
                "content": content
           }
        )
        st.chat_message(name).write(content)
    # stream = agents.stream({"messages": st.session_state['messages']})
    # for s in stream:
    #     name = list(s.keys())[0]
    #     content = s[name]
    #     for c in content:
    #         if isinstance(c, dict):
    #             for msg in c['messages']:
    #                 print(f"{name} : {msg}")
    #         elif isinstance(c, str):
    #             print(f"{name} : {c}")
            