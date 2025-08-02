from logging import Logger
import pandas as pd 

from review_analyzer.domain.interfaces import DataFrameSaver

class DataFrameSaverCsv(DataFrameSaver):
    def __init__(self, logger: Logger):
        self.logger = logger

    def save(self, dataframe, csv_path):
        try:
            dataframe.to_csv(csv_path, index=False, sep=';')
            self.logger.info("Zapisano plik: %s", csv_path)
        except Exception as e:
            self.logger.warning("Blad podczas zapisu %s, %s", csv_path, e)