from logging import Logger
from multiprocessing.dummy import Pool  # Thread-based
from typing import List
from tqdm import tqdm
import pandas as pd

from review_analyzer.infrastructure.aspect_labeler import MistralAspectLabeler

class AspectLabelingService:
    def __init__(self, labeler: MistralAspectLabeler, aspect_df: pd.DataFrame, logger: Logger, workers: int = 4, limit: int = None):
        self.labeler = labeler
        self.aspect_df = aspect_df
        self.logger = logger
        self.workers = workers
        self.limit = limit

    def run(self):
        self.logger.debug("Parametry: workers=%d, limit=%s", self.workers, self.limit)

        df = self.aspect_df.head(self.limit).copy() if self.limit else self.aspect_df.copy()

        self.logger.info("Przetwarzanie %d aspektów", len(df))

        with Pool(processes=self.workers) as pool:
            labels = list(
                tqdm(pool.imap_unordered(self.labeler.label_aspect, df["aspect"]), total=len(df))
            )

        df["labels"] = labels
        result_df = df.explode("labels").reset_index(drop=True)
        return result_df