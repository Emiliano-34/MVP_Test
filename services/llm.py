import os
from groq import Groq, GroqError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class LLMClient:
    def __init__(self):
        # Inicializa el cliente solo si existe la API Key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY no encontrada en variables de entorno. Revisa tu archivo .env")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    # RÚBRICA: Reintentos (hasta 3) con espera exponencial
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((GroqError, TimeoutError)),
        reraise=True
    )
    def get_response(self, messages, temperature=0.7, max_tokens=500):
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stop=None,
                stream=False
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error en LLM: {str(e)}")
            raise e
