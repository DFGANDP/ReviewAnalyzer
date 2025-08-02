from logging import Logger
from typing import List
import json

class JsonlSaver: # many keys
    def __init__(self, output_path: str, logger: Logger):
        self.output_path = output_path
        self.logger = logger

    def save(self, data: List[dict]):
        with open(self.output_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        self.logger.info('Wyniki zapisano do pliku: %s', self.output_path)

class JsonSaver: # only one 
    def __init__(self, filepath: str, logger=None):
        self.filepath = filepath
        self.logger = logger

    def save(self, data: dict):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        if self.logger:
            self.logger.info("Wyniki zapisano do pliku: %s", self.filepath)
