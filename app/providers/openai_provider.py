import os

from dotenv import load_dotenv
from openai import OpenAI

from app.providers.base_provider import BaseProvider
from app.exceptions import ProviderException


load_dotenv()


class OpenAIProvider(BaseProvider):
    """
    Real OpenAI Provider.
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:

            raise ProviderException("OPENAI_API_KEY not found in .env")

        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        try:

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.7,
                max_tokens=512,
            )

            return response.choices[0].message.content

        except Exception as e:

            raise ProviderException(f"OpenAI API Error: {e}")
