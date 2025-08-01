from ..model.element import Element
from selenium.webdriver.common.by import By

class Selectors:
    NEW_CHAT = Element(By.CSS_SELECTOR, "[data-icon='new-chat-outline']")
    SEARCH = Element(By.CSS_SELECTOR, 'div[aria-label="Pesquisar nome ou número"]')
    ATTACHMENTS = Element(By.CSS_SELECTOR, "button[title='Anexar']")
    FILE_INPUT_ALL = Element(By.CSS_SELECTOR, "input[type='file'][accept='*']")
    FILE_INPUT_IMAGE = Element(By.CSS_SELECTOR, "input[type='file'][accept='image/*']")
    SEND_BUTTON = Element(By.CSS_SELECTOR, "[data-icon='send']")
    MESSAGE_BOX = Element(By.CSS_SELECTOR, "div[aria-label='Digite uma mensagem']")
    MESSAGES_AREA = Element(By.CSS_SELECTOR, 'div[class*="_amkz message-out focusable-list-item _amjy _amjz _amjw"]')
    # MESSAGES_AREA2 = Element(By.CSS_SELECTOR, 'div[class="message-out focusable-list-item _amjy _amjz _amjw"]')
    CHECK = Element(By.CSS_SELECTOR, 'span[aria-label=" Entregue "]')
    BACK = Element(By.CSS_SELECTOR, "span[data-icon='back']")
    MAIN_AREA = Element(By.CSS_SELECTOR, "div[id='main']")
    SAFE_SEARCH = Element(By.CSS_SELECTOR, "div[aria-label='Caixa de texto de pesquisa']")
    CANCEL_SAFE_SEARCH = Element(By.CSS_SELECTOR, 'button[aria-label="Cancelar pesquisa"]')