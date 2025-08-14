from typing import Dict, Any
import json
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


class BaseAgent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions
        self.llm = ChatOllama(model="llama3.2:1b-instruct-q5_0", temperature=0.7)
        self.json_parser = JsonOutputParser()
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.instructions),
            ("user", "{input}"),
        ])

    async def run(self, messages: list) -> Dict[str, Any]:
        """Default run method to be overridden by child classes"""
        raise NotImplementedError("Subclasses must implement run()")

    def _invoke_llm(self, prompt: str) -> Dict[str, Any]:
        """Invoke Langchain LLM with the given prompt and parse JSON output"""
        try:
            chain = self.prompt_template | self.llm | self.json_parser
            response = chain.invoke({"input": prompt})
            return response
        except Exception as e:
            print(f"Error invoking LLM or parsing JSON: {str(e)}")
            raise

    def _parse_json_safely(self, text: str) -> Dict[str, Any]:
        """Safely parse JSON from text, handling potential errors"""
        try:
            return self.json_parser.parse(text)
        except Exception as e:
            print(f"Error parsing JSON: {str(e)}")
            return {"error": f"Invalid JSON content: {e}"}


