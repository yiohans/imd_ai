import subprocess

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from tools import *

class MultiAgents:
    def __init__(self, models):
        self.supervisor_model, self.agent_model = self.initialize_models(models)
        # self.chat_agent = self.initialize_agent(
        #     name="chat_agent",
        #     tools=[],
        #     prompt="You can only chat with the user."
        # )
        self.research_agent = self.initialize_agent(
            name="sei_research_agent",
            tools=[search_process, get_document_list_from_process, get_document_by_type],
            prompt=(
                "Você é especialista em obter informações sobre processos do SEI. "
                "Você é capaz de: "
                "pesquisar processos usando a função search_process, "
                "listar documentos de um processo usando a função get_document_list_from_process, "
                "e obter tipos específicos de documentos de um processo usando a função get_document_by_type. "
            )
        )
        self.graph = self.initialize_graph((
            "Você é um chatbot com um time de especialistas para atender o usuário. "
            "Use sei_research_agent para responder perguntas sobre processos no "
            "Sistema Eletrônico de Informações (SEI) do TRE do Rio Grande do Norte (TRE-RN)."
        ))

    def initialize_models(self, models):
        match models['supervisor']["provider"]:
            case "groq":
                print("Using Groq model for supervisor")
                llm_supervisor = ChatGroq(
                    model=models['supervisor']['model'],
                    temperature=models['supervisor']['temperature']
                )
            case "ollama":
                print("Using Ollama model for supervisor")
                llm_supervisor = ChatOllama(
                    model=models['supervisor']['model'],
                    temperature=models['supervisor']['temperature']
                    )
                model_name = models['supervisor']['model']
                subprocess.run(["ollama", "pull", model_name])
                
        match models['agent']['provider']:
            case "groq":
                print("Using Groq model for agent")
                llm_agent = ChatGroq(
                    model=models['agent']['model'],
                    temperature=models['agent']['temperature']
                )
            case "ollama":
                print("Using Ollama model for agent")
                llm_agent = ChatOllama(
                    model=models['agent']['model'],
                    temperature=models['agent']['temperature']
                    )
                model_name = models['agent']['model']
                subprocess.run(["ollama", "pull", model_name])
        return llm_supervisor, llm_agent
    
    def initialize_agent(self, name, prompt, tools):
        agent =  create_react_agent(
            self.agent_model,
            name=name,
            tools=tools,
            prompt=prompt,
        )
        return agent
    
    def initialize_graph(self, prompt):
        workflow = create_supervisor(
            [self.research_agent],
            model=self.supervisor_model,
            prompt=prompt,
            output_mode="full_history"
        )
        return workflow.compile()
    
    def run(self, messages, recursion_limit=10):
        return self.graph.invoke(
            messages,
            {"recursion_limit": recursion_limit}
        )
    
    def stream(self, messages, recursion_limit=10):
        return self.graph.stream(
            messages,
            {"recursion_limit": recursion_limit},
            stream_mode="values"
        )