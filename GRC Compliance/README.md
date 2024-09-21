# Cybersecurity GRC Compliance Tool

This tool allows users to upload cybersecurity policy documents and standards, compare them for compliance, and identify missing elements.

## Setup

1. Ensure you have Python 3.7+ installed.

2. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Set up Qdrant:
   - Ensure Docker is installed on your system. If not, download and install it from https://www.docker.com/get-started
   - Pull the Qdrant Docker image:
     ```
     docker pull qdrant/qdrant
     ```
   - Run Qdrant container:
     ```
     docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
     ```
   - Install Qdrant client:
     ```
     pip install qdrant-client
     ```

7. Set up Ollama:
   - Install Ollama following the instructions at https://ollama.ai/
   - Pull the Llama models: `ollama pull llama3.1:latest`
   - Pull the nomic-embed-text model: `ollama pull nomic-embed-text:latest`

8. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

9. Open a web browser and navigate to `http://localhost:8000` to use the application.

## Usage

1. Upload a cybersecurity policy document and a standard document through the web interface.
2. The system will process the documents, split them into sections, and compare them for compliance.
3. View the detailed compliance results on the results page, including:
   - Compliance status for each section
   - Missing elements in the policy
   - Summaries of non-compliant sections

## Dependencies

- FastAPI
- Uvicorn
- Jinja2
- LangChain
- Ollama
- Qdrant

For a complete list of dependencies, see `requirements.txt`.

## Troubleshooting

If you encounter a "command not found: qdrant" error, ensure that:
1. Docker is running
2. The Qdrant container is active
3. The Qdrant client is installed in your virtual environment

## Note

This tool uses AI-powered analysis to assess compliance. While it provides valuable insights, it should be used as an aid to human expertise, not as a replacement for professional judgment in cybersecurity compliance matters.

## Updating Dependencies

If you encounter deprecation warnings related to LangChain, you may need to update your imports and install additional packages:

1. Update import statements in your code:
   Change `from langchain.llms import Ollama` to `from langchain_community.llms import Ollama`

2. Install the langchain-community package:
   ```
   pip install -U langchain-community
   ```

These steps will ensure compatibility with future versions of LangChain.