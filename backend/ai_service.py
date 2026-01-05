
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI

# LangChain Imports
try:
    from ai.chains import get_dictionary_chain, get_context_chain
    from ai.graph import create_tutor_graph
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("WARN: LangChain dependencies not found. AI features may be limited.")
    LANGCHAIN_AVAILABLE = False

# Load env vars from .env file
env_path = Path(__file__).parent / '.env'
print(f"DEBUG: Loading .env from {env_path.absolute()}")
load_dotenv(dotenv_path=env_path, override=True)  # Force override

class AIService:
    def __init__(self):
        # --- Whisper Setup (Keep as is) ---
        # Check for Azure config first
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        self.whisper_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_WHISPER", "whisper") # User provided name
        
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if self.azure_endpoint and self.azure_key:
            print(f"DEBUG: Using Azure OpenAI Service for Whisper (Endpoint: {self.azure_endpoint})")
            self.client = AzureOpenAI(
                api_key=self.azure_key,
                api_version=self.azure_version,
                azure_endpoint=self.azure_endpoint
            )
            self.is_azure = True
        elif self.openai_key and "placeholder" not in self.openai_key:
            print("DEBUG: Using Standard OpenAI Service for Whisper")
            self.client = OpenAI(api_key=self.openai_key)
            self.is_azure = False
        else:
            print("WARNING: No valid API Key found (OpenAI or Azure). Whisper will fail.")
            self.client = None

        # --- LangChain Setup ---
        self.dictionary_chain = None
        self.context_chain = None
        self.tutor_graph = None

        if LANGCHAIN_AVAILABLE:
            try:
                self.dictionary_chain = get_dictionary_chain()
                self.context_chain = get_context_chain()
                self.tutor_graph = create_tutor_graph()
                print("DEBUG: LangChain Agents Initialized Successfully.")
            except Exception as e:
                 print(f"ERROR: Failed to initialize LangChain Agents: {e}")

    def transcribe_audio(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Transcribes the given audio file using OpenAI Whisper API.
        Returns a list of segment dictionaries compatible with SubtitleSegment.
        """
        if not self.client:
            raise ValueError("API Key is missing. Please check backend/.env")

        audio_file_path = Path(audio_path)
        if not audio_file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"DEBUG: sending {audio_path} to Whisper API...")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                if self.is_azure:
                    # Azure uses the deployment name as model
                    model_name = self.whisper_deployment
                else:
                    model_name = "whisper-1"

                # Use response_format="verbose_json" to get segments with timestamps
                transcript = self.client.audio.transcriptions.create(
                    model=model_name, 
                    file=audio_file, 
                    response_format="verbose_json",
                    timestamp_granularities=["segment"] 
                )
            
            # The structure of transcript with verbose_json includes 'segments'
            # Each segment has: id, seek, start, end, text, tokens, temperature, ...
            
            # We map this to our SubtitleSegment structure
            segments = []
            if hasattr(transcript, 'segments'):
                for i, seg in enumerate(transcript.segments):
                    segments.append({
                        "index": i,
                        "start_time": seg.start,
                        "end_time": seg.end,
                        "text": seg.text.strip()
                    })
            else:
                 # Fallback if no segments (short audio?)
                 segments.append({
                     "index": 0,
                     "start_time": 0.0,
                     "end_time": transcript.duration,
                     "text": transcript.text
                 })

            return segments

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise e

    # --- New AI Features ---

    def lookup_word(self, word: str, context_sentence: str, target_language: str = "English") -> Dict[str, Any]:
        """
        Analyzes a word in context using LangChain DictionaryAgent.
        """
        if not self.dictionary_chain:
            return {"error": "AI Service not initialized"}

        try:
            # invoke returns a VocabularyItem (Pydantic object) because of the parser
            result = self.dictionary_chain.invoke({
                "word": word, 
                "context_sentence": context_sentence,
                "target_language": target_language
            })
            return result.model_dump() # Pydantic v2
        except Exception as e:
            print(f"Error in lookup_word: {e}")
            return {"error": str(e)}

    def explain_context(self, subtitle_text: str, target_language: str = "English") -> Dict[str, Any]:
        """
        Explains grammar/culture using LangChain ContextExplainer.
        """
        if not self.context_chain:
            return {"error": "AI Service not initialized"}

        try:
            result = self.context_chain.invoke({
                "subtitle_text": subtitle_text,
                "target_language": target_language
            })
            return result.model_dump()
        except Exception as e:
            print(f"Error in explain_context: {e}")
            return {"error": str(e)}

    def chat_with_tutor(self, messages: List[Dict[str, str]], context_text: Optional[str] = None, target_language: str = "Chinese") -> Dict[str, Any]:
        """
        Runs the LangGraph tutor workflow.
        Input messages: [{"role": "user", "content": "..."}]
        """
        if not self.tutor_graph:
            return {"error": "AI Service not initialized"}

        try:
            # We need to convert simple dict messages to LangChain BaseMessage objects
            # Typically LangGraph state expects BaseMessage
            from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
            
            lc_messages = []
            for m in messages:
                if m['role'] == 'user':
                    lc_messages.append(HumanMessage(content=m['content']))
                elif m['role'] == 'assistant':
                    lc_messages.append(AIMessage(content=m['content']))
                elif m['role'] == 'system':
                    lc_messages.append(SystemMessage(content=m['content']))
            
            input_state = {
                "messages": lc_messages, 
                "context_text": context_text or "",
                "target_language": target_language
            }
            
            # Invoke graph
            result = self.tutor_graph.invoke(input_state)
            
            # Result state['messages'] contains the full history. We want the last one.
            last_message = result["messages"][-1]
            
            return {"content": last_message.content, "role": "assistant"}
        except Exception as e:
             print(f"Error in chat_with_tutor: {e}")
             return {"error": str(e)}

ai_service = AIService()
