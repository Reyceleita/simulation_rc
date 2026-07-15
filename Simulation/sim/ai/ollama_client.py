"""
ollama_client.py

Cliente encargado de comunicarse con Ollama.
"""

import requests

from sim.ai.prompts import (
    SYSTEM_PROMPT,
    build_prompt,
)


class OllamaNewsGenerator:

    def __init__(
        self,
        host="http://192.168.0.103:11434", #Verificar antes de iniciar
        model="llama3.1:8b"
    ):

        self.url = f"{host}/api/chat"
        self.model = model

    # ---------------------------------------------------------

    def generate(
        self,
        topic: str,
        history: list[str],
    ) -> str:
        """
        Genera un titular utilizando Ollama.
        """

        prompt = build_prompt(
            topic,
            history,
        )

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },

            {
                "role": "user",
                "content": prompt,
            },

        ]

        data = {

            "model": self.model,
            "messages": messages,
            "stream": False,

        }

        try:

            response = requests.post(
                self.url,
                json=data,
                timeout=60,
            )

            response.raise_for_status()

            text = response.json()["message"]["content"].strip()

            return self._clean_response(text)

        except Exception as e:

            print(f"[News] Error generando noticia: {e}")

            return "Noticiero: No ocurrió nada interesante hoy."

    # ---------------------------------------------------------

    @staticmethod
    def _clean_response(text: str) -> str:
        """
        Limpia respuestas inesperadas del modelo.
        """

        text = text.strip()

        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]

        if not text.startswith("Noticiero:"):
            text = f"Noticiero: {text}"

        return text