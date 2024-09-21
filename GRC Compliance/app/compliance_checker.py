from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .react_agent import create_react_agent
from .database import get_text_from_embedding, init_qdrant
from typing import List, Dict
from qdrant_client import QdrantClient  

def init_qdrant():
    return QdrantClient("localhost", port=6333)

def split_document(text: str, max_length: int = 1000) -> List[str]:
    """Split a document into smaller chunks."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) < max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def check_compliance(policy_embedding, standard_embedding) -> List[Dict]:
    llm = Ollama(model="llama3.1:latest")
    agent = create_react_agent()
    client = init_qdrant()  # Initialize the Qdrant client

    # Retrieve original text from embeddings
    policy_text = get_text_from_embedding(client, policy_embedding)
    standard_text = get_text_from_embedding(client, standard_embedding)

    policy_sections = split_document(policy_text)
    standard_sections = split_document(standard_text)

    compliance_results = []

    for i, policy_section in enumerate(policy_sections):
        standard_section = standard_sections[i] if i < len(standard_sections) else ""
        
        prompt = f"""
        Analyze the following policy section and compare it to the standard section:

        Policy Section:
        {policy_section}

        Standard Section:
        {standard_section}

        Determine if the policy section is compliant with the standard section. 
        If it's not compliant, identify the missing or incorrect elements.
        """

        response = agent.run(prompt)

        # Parse the agent's response
        is_compliant = "compliant" in response.lower()
        issues = []
        if not is_compliant:
            issues = [issue.strip() for issue in response.split('\n') if issue.strip().startswith('-')]

        result = {
            "section": f"Section {i+1}",
            "compliant": is_compliant,
            "issues": issues if issues else ["No specific issues identified, but marked as non-compliant."]
        }

        compliance_results.append(result)

    return compliance_results