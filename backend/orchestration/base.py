from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from google import genai
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class WorkerAgent(Generic[T], ABC):
    """
    Abstract Base Class for specialized advocacy workers.
    Each worker must define its own extraction schema and prompt logic.
    """

    client: Optional[genai.Client]

    def __init__(self, api_key: Optional[str] = None):
        import os

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Optional[T]:
        """
        Main execution point for the agent.
        Takes a context dictionary (e.g., building data, reports) and
        returns a structured Pydantic model.
        """
        pass

    def _call_gemini(
        self, prompt: str, schema: Type[T], model: str = "gemini-2.5-flash"
    ) -> Optional[T]:
        """
        Standardized Gemini call for structured extraction.
        """
        if not self.client:
            return None

        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                },
            )
            # The SDK's parsed field can be T if schema is passed correctly
            return response.parsed  # type: ignore
        except Exception as e:
            print(f"Gemini Error in {self.__class__.__name__}: {e}")
            return None
