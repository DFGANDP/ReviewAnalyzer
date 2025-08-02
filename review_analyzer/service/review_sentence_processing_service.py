from typing import List
#from multiprocessing import Pool
from multiprocessing.dummy import Pool  # Thread-based pool

from tqdm import tqdm

class ReviewProcessingService:
    def __init__(self, extractor, loader, saver, logger, workers=4, limit=None):
        self.extractor = extractor
        self.loader = loader
        self.saver = saver
        self.logger = logger
        self.workers = workers
        self.limit = limit

    def run(self, language=None):
        self.logger.info("Start przetwarzania recenzji")
        self.logger.debug("Parametry: language=%s, workers=%d, limit=%s", language, self.workers, self.limit)

        reviews = self.loader.load_reviews(language)
        if self.limit:
            reviews = reviews[:self.limit]


        self.logger.debug("Przetwarzanie %d recenzji", len(reviews))
        try:
            with Pool(processes=self.workers) as pool:
                results = list(
                    tqdm(
                        pool.imap_unordered(self.extractor.extract_sentence_sentiment, reviews),
                        total=len(reviews),
                        desc="Przetwarzanie recenzji"
                    )
                )
        except Exception as e:
            self.logger.error("Błąd podczas przetwarzania recenzji: %s", str(e), exc_info=True)
            return

        self.logger.info("Zakończono przetwarzanie — %d wyników", len(results))

        try:
            self.saver.save(results)
            self.logger.info("Zapisano %d wyników", len(results))
        except Exception as e:
            self.logger.error("Błąd podczas zapisu wyników: %s", str(e), exc_info=True)