import subprocess

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from tools import search_process, get_documents_from_process

class MultiAgents:
    def __init__(self, models):
        self.supervisor_model, self.agent_model = self.initialize_models(models)
        self.chat_agent = self.initialize_agent(
            name="chat_agent",
            tools=[],
            prompt="You can only chat with the user."
        )
        self.research_agent = self.initialize_agent(
            name="research_agent",
            tools=[search_process, get_documents_from_process],
            prompt="You can only search for SEI processes and get documents from them."
        )
        self.graph = self.initialize_graph((
            "You are a team supervisor managing a team of experts. "
            "For conversation, use chat_agent. "
            "For processes information, use research_agent."
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
            [self.chat_agent, self.research_agent],
            model=self.supervisor_model,
            prompt=prompt,
            output_mode="last_message"
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
            {"recursion_limit": recursion_limit}
        )