
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

# Load env vars
load_dotenv()

def get_llm(temperature: float = 0.7) -> BaseChatModel:
    """
    Returns an initialized LLM based on environment variables.
    Prioritizes Azure, then Standard OpenAI.
    """
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_CHAT", "gpt-4o") 
    
    openai_key = os.getenv("OPENAI_API_KEY")

    if azure_endpoint and azure_key:
        print(f"DEBUG: Using Azure OpenAI (Deployment: {azure_deployment})")
        return AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_key,
            azure_deployment=azure_deployment,
            api_version=azure_version,
            # temperature=temperature # Removed to support o1/preview models that don't support temp
        )
    elif openai_key:
        print("DEBUG: Using Standard OpenAI")
        return ChatOpenAI(
            api_key=openai_key,
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
            temperature=temperature
        )
    else:
        raise ValueError("No valid OpenAI or Azure Configuration found in .env")
