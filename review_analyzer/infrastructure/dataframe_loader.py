from logging import Logger
import pandas as pd 

from review_analyzer.domain.interfaces import DataFrameLoader

class DataFrameLoaderCsv(DataFrameLoader):
    def __init__(self, logger: Logger):
        self.logger = logger

    def load(self, csv_path):
        try:
            df = pd.read_csv(csv_path, sep=';')
            self.logger.info("Wczytano plik: %s posiada %d lini", csv_path, len(df))
            return df
        except Exception as e:
            self.logger.warning("Blad podczas wczytywania %s, %s", csv_path, e)
        return None