# review_analyzer/infrastructure/aspect_labeler_llm.py
from logging import Logger
import json
from ollama import Client
from typing import List
from review_analyzer.domain.aspect_labeler import AspectLabeler
import re



class MistralAspectLabeler(AspectLabeler):
    def __init__(self, client: Client, model_name: str, prompt_template: str, logger: Logger):
        self.client = client
        self.model = model_name
        self.prompt_template = prompt_template
        self.logger = logger

    def _extract_json(self, text: str) -> dict:
        match = re.search(r'\{\s*"labels"\s*:\s*\[.*?\]\s*\}', text, re.DOTALL)
        if not match:
            raise json.JSONDecodeError("Brak poprawnego JSON-a w odpowiedzi", text, 0)
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            self.logger.warning("Błąd dekodowania JSON: %s", e)
            raise

    def label_aspect(self, aspect: str) -> List[str]:
        prompt = self.prompt_template.replace("{INSERT_ASPECT_HERE}", aspect)

        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.15}
            )
            self.logger.debug("RESPONSE: %s", response)
            raw = response["message"]["content"]

            parsed = self._extract_json(raw)
            return parsed.get("labels", [])
        except Exception as e:
            self.logger.warning("Błąd podczas etykietowania aspektu (%s): %s", aspect, e)
            return []