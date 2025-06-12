import base64
import logging
import random
from os.path import join
from time import sleep
from typing import Optional

from .config.messages import LoggingMessages
from .config.config import Config
from .config.seletores import Selectors
from .utils.driver.driver import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class Actions:
    def __init__(self) -> None:
        self.webdriver = Driver()
        self._safe_search = False
        self.logger = logging.getLogger(self.__str__())

    def __str__(self) -> str:
        return "Action Automate"

    def entregue(self) -> bool:
        """Verifica se a última mensagem foi entregue."""
        messages = self.webdriver.find_element(element=Selectors.MESSAGES_AREA, multiples=True)
        if isinstance(messages, list):
            final_message = messages[-1]
            return self.webdriver.await_element(element=Selectors.CHECK, area=final_message, wait=False) is not None
        return False
    
    def start_WhatsApp(self) -> None:
        """Inicia o WhatsApp Web."""
        self.webdriver.getDriver().get("https://web.whatsapp.com/")
        self.logger.info(LoggingMessages.START_PLATFORM)

    def safe_search(self, target: str) -> None:
        """Realiza uma busca segura pelo número."""
        self.logger.info(LoggingMessages.SEARCH_CONTACT_BEFORE.format(target))
        search_area = self.webdriver.await_element(Selectors.SAFE_SEARCH)
        if isinstance(search_area, WebElement):
            search_area.send_keys(target)
            search_area.send_keys(Keys.ENTER)
            self._safe_search = True
            sleep(random.randint(1, 3))
        else:
            raise Exception("Área não encontrada")

    def cancel_safe_search(self) -> None:
        """Cancela a busca segura."""
        if self._safe_search:
            try:
                cancel_button = self.webdriver.await_element(Selectors.CANCEL_SAFE_SEARCH, wait=True)
                cancel_button.click() # type: ignore
                sleep(random.randint(1, 3))
                self._safe_search = False
            except Exception:
                self.cancel_safe_search()
            
    def stop(self) -> None:
        """Finaliza o webdriver."""
        self.webdriver.kill()

    def search(self, number: int) -> Optional[bool]:
        """Busca um contato pelo número."""
        self.logger.info(LoggingMessages.SEARCH_CONTACT_AFTER.format(number))
        new_chat = self.webdriver.await_element(Selectors.NEW_CHAT)
        if not isinstance(new_chat, WebElement):
            return None
        new_chat.click()
        search = self.webdriver.await_element(Selectors.SEARCH)
        if not isinstance(search, WebElement):
            return None
        search.send_keys(str(number))
        sleep(random.randint(4, 10))
        search.send_keys(Keys.ENTER)
        message_box = self.webdriver.await_element(element=Selectors.MESSAGE_BOX, wait=False)
        if message_box is None:
            self.logger.error(LoggingMessages.NUMBER_NOT_FIND.format(number=number))
            self.back()
            return False
        sleep(random.randint(1, 3))
        return True

    def _send_message(self, message: str, message_box: WebElement) -> None:
        message_box.send_keys(str(message))
        message_box.send_keys(Keys.ENTER)

    def _send_messages(self, message: str, message_box: WebElement):
        messages = message.splitlines()
        for message in messages:
            message_box.send_keys(str(message))
            message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        message_box.send_keys(Keys.ENTER)

    def send_message(self, message: str, split_lines: bool = False) -> None:
        self.logger.info(LoggingMessages.MESSAGE_SENDED)
        """Envia uma mensagem."""
        message_box = self.webdriver.await_element(element=Selectors.MESSAGE_BOX)
        if not isinstance(message_box, WebElement):
            return
        if split_lines:
            self._send_messages(message, message_box)
        else:
            self._send_message(message, message_box)
        sleep(random.randint(1, 3))

    def _input_buttons(self) -> None:
        """Clica no botão de anexos."""
        anexos = self.webdriver.await_element(element=Selectors.ATTACHMENTS)
        if not isinstance(anexos, WebElement):
            return
        anexos.click()
        sleep(random.randint(1, 3))

    def send_file(self, file_path: str, is_image: bool = False) -> None:
        """Envia um arquivo."""
        self._input_buttons()
        file_input = self.webdriver.await_element(element=Selectors.FILE_INPUT_IMAGE if is_image else Selectors.FILE_INPUT_ALL)
        if not isinstance(file_input, WebElement):
            return
        file_input.send_keys(file_path)
        send_button = self.webdriver.await_element(element=Selectors.SEND_BUTTON)
        if not isinstance(send_button, WebElement):
            return
        send_button.click()
        sleep(random.randint(1, 3))

    def screenshot(self, name: str | int) -> None:
        """Tira um screenshot da área principal."""
        main = self.webdriver.await_element(element=Selectors.MAIN_AREA)
        if not isinstance(main, WebElement):
            return
        if main.screenshot(join(Config.REPOSITORY_JGP, f'{name}.png')):
            self.logger.info(f"Registro guardado com sucesso em: '{name}'")
        else:
            logging.error("Falha ao guardar registro da tela.")      

    def print_page(self, name: str | int) -> None:
        """Imprime a página em PDF."""
        pdf = self.webdriver.getDriver().print_page(self.webdriver.getPrintOptions())
        pdf_decode = base64.b64decode(pdf)
        with open(Config.REPOSITORY_PDF.format(name), "wb") as file:
            file.write(pdf_decode)

    def back(self) -> None:
        """Volta para a tela anterior."""
        back_button = self.webdriver.await_element(element=Selectors.BACK)
        if not isinstance(back_button, WebElement):
            return
        back_button.click()
        sleep(random.randint(1, 3))
