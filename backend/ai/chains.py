
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field
from .core import get_llm

class VocabularyItem(BaseModel):
    word: str = Field(description="The source word or phrase being defined")
    definition: str = Field(description="Clear, concise definition in the target language")
    pronunciation: str = Field(description="IPA pronunciation")
    translation: str = Field(description="Direct translation of the word into the target language")
    example_sentence: str = Field(description="An example sentence using the word (monolingual or bilingual as appropriate)")
    
def get_dictionary_chain() -> Runnable:
    llm = get_llm(temperature=0.3)
    
    parser = PydanticOutputParser(pydantic_object=VocabularyItem)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful language tutor. You provide clear definitions and examples for language learners. Output strict JSON."),
        ("user", "Define the term (word or phrase) '{word}' from the context sentence: '{context_sentence}'.\nTarget Language: {target_language}.\n\n{format_instructions}")
    ])
    
    return prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

class ContextExplanation(BaseModel):
    summary: str = Field(description="Brief summary of the meaning in target language")
    grammar_notes: str = Field(description="Key grammar points observed, explained in target language")
    cultural_notes: str = Field(description="Any cultural context or slang, explained in target language")

def get_context_chain() -> Runnable:
    llm = get_llm(temperature=0.7)
    parser = PydanticOutputParser(pydantic_object=ContextExplanation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert language teacher. Analyze the given subtitle text for grammar and cultural nuance."),
        ("user", "Analyze this text: '{subtitle_text}'.\nExplain in: {target_language}.\n\n{format_instructions}")
    ])
    
    return prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
