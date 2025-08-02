from ollama import Client
import json
import re
from typing import List, Dict
from logging import Logger

from review_analyzer.domain.interfaces import ReviewAspectExtractor

class MistralSentimentAspectExtractor(ReviewAspectExtractor):
    def __init__(self, client: Client, model_name: str, prompt: str, logger: Logger):
        self.client = client
        self.prompt_template = prompt
        self.model = model_name
        self.logger = logger


    def _build_result(self, review, liked: List[str], disliked: List[str], error: str = None) -> Dict:
        result = {
            "appid": review.appid,
            "recommendationid": review.recommendationid,
            "liked": liked,
            "disliked": disliked,
            "original_review": review.review,
        }
        if error:
            result["error"] = error
        return result

    def _extract_json(self, text: str) -> Dict:
        text = text.replace("\xa0", " ")
        text = re.sub(r",\s*]", "]", text)
        match = re.search(r"\{[\s\S]+?\}", text)
        if not match:
            raise json.JSONDecodeError("No valid JSON found", text, 0)
        return json.loads(match.group(0))

    def extract_sentence_sentiment(self, review) -> Dict: 
        prompt = self.prompt_template.replace("{INSERT_REVIEW_HERE}", review.review)
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.15} # from https://ollama.com/MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L
            )
            self.logger.debug('RESPONSE: %s', response)

            #parsed = json.loads(response["message"]["content"])
            raw = response["message"]["content"]
            parsed = self._extract_json(raw)

            return self._build_result(
                review,
                liked=parsed.get("liked", []),
                disliked=parsed.get("disliked", [])
            )

        except json.JSONDecodeError as e:
            self.logger.warning(
                "Błąd dekodowania JSON z modelu (recommendationid=%s): %s",
                review.recommendationid, str(e)
            )
            return self._build_result(review, [], [], error="json_decode")

        except Exception as e:
            self.logger.error(
                "Błąd podczas przetwarzania review (recommendationid=%s): %s",
                review.recommendationid, str(e),
                exc_info=True
            )
            return self._build_result(review, [], [], error=str(e))