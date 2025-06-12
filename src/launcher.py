import logging
from time import sleep
from typing import Literal
from .data.data import Data
from .model.message import Message
from .config.messages import LoggingMessages
from .actions import Actions

class Launcher(Data):
    _group: Literal["Sentinela", "Sentinela - Homologação"]
    
    def __init__(self, debug_app: bool = True) -> None:
        super().__init__()
        self._setGroup(debug=debug_app)
        self.logger = logging.getLogger(self.__class__.__name__)

    def _setGroup(self, debug: bool) -> None:
        if debug:
            self._group = "Sentinela - Homologação"
        else:
            self._group = "Sentinela"

    def wppProcess(self, base_path: str) -> None:
        self.read_file(base_path)
        if self.getData.empty:
            self.logger.info(LoggingMessages.EMPTY_DATAFRAME)
            return
        message = Message.getMessage(self.getData[:10])
        self.actions = Actions()
        self.actions.start_WhatsApp()
        self.actions.safe_search(self._group)
        self.actions.send_message(message, split_lines=True)
        sleep(10)