from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from typing import Dict, List, Any
from langchain.agents import Tool

class ComplianceCheckTool(BaseTool):
    name: str = "ComplianceCheck"
    description: str = "Check if a policy section complies with a standard section"

    def _run(self, policy_section: str, standard_section: str) -> str:
        llm = Ollama(model="llama3.1:latest")
        prompt = f"Analyze the compliance of the following policy section with the given standard section. Respond with 'Compliant', 'Partially Compliant', or 'Non-compliant', followed by a brief explanation.\n\nPolicy section: {policy_section}\n\nStandard section: {standard_section}"
        return llm(prompt)

    def _arun(self, policy_section: str, standard_section: str):
        raise NotImplementedError("This tool does not support async")

class MissingElementsTool(BaseTool):
    name: str = "MissingElements"
    description: str = "Identify elements missing from the policy that are present in the standard"

    def _run(self, policy_section: str, standard_section: str) -> str:
        llm = Ollama(model="llama3.1:latest")
        prompt = f"Identify key elements present in the standard section but missing from the policy section. List the missing elements.\n\nPolicy section: {policy_section}\n\nStandard section: {standard_section}"
        return llm(prompt)

    def _arun(self, policy_section: str, standard_section: str):
        raise NotImplementedError("This tool does not support async")

def create_react_agent():
    llm = Ollama(model="llama3.1:latest")
    
    tools = [
        ComplianceCheckTool(),
        MissingElementsTool(),
        Tool(
            name="Summarize",
            func=lambda x: llm(f"Summarize the following text:\n{x}"),
            description="Useful for summarizing long sections of text"
        )
    ]
    
    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad"],
        template="You are a cybersecurity compliance expert. Your task is to analyze policy documents and compare them to standards, identifying compliance issues and missing elements. Compare the following policy section to the standard section:\n\nPolicy Section: {policy_section}\n\nStandard Section: {standard_section}\n\n{agent_scratchpad}"
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain