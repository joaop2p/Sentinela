import logging
from os.path import isfile, basename
from time import sleep
from pandas import DataFrame, read_csv
from typing import Iterable
from ..config.messages import ErrorsMessages, LoggingMessages
from ..utils.exceptions.dataExceptions import DataException

class Data:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._df: DataFrame

    def _validateColumns(self, columns: Iterable["str"]) -> bool:
        essentials = (
            "CONTA", "LOCALIDADE", "NOME", "DEFEITO_FALHA", "DH_INICIAL_INT")
        return not any(essential not in columns for essential in essentials)

    def read_file(self, path:str|None):
        if path is None or not isfile(path):
            raise DataException(ErrorsMessages.INVALID_PATH_ERR.format(path=path))
        try:
            temp_df = read_csv(path, sep=";")
        except PermissionError:
            self.logger.warning(LoggingMessages.FILE_BUSY.format(file = basename(path)))
            sleep(120)
            return self.read_file(path)
        if self._validateColumns(temp_df.columns):
            self.logger.info(LoggingMessages.TOT_OCCURRENCE.format(total=len(temp_df)))
            self._df = temp_df
        else:
            raise DataException(ErrorsMessages.NO_COLUMNS_IN_DATA)

    @property
    def getData(self) -> DataFrame:
        return self._df