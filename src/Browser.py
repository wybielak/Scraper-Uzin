# Created by DNw XI2023
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Browser: # SECTION robot logujący się na stronę i otwierający linki
               # w obecnej konfiguracji przystosowany do łączenia się z www.remmers.pl
    browser = None

    def __init__(self): # ANCHOR ustawienie sterownika przeglądarki na Chrome
        self.browser = webdriver.Chrome()

    def openPage(self, url: str): # ANCHOR otwieranie strony z url
        self.browser.get(url)

    def closeBrowser(self): # ANCHOR zamykanie strony
        self.browser.close()

    def addInput(self, by: By, value: str, text: str, parent_by = '', parent_val = ''): # ANCHOR wprowadzanie danych do inputa,
        if parent_by != '' and parent_val != '':                                         # można podać pojemnik nadrzędny parent inputa w razie problemów
            parent_elem = self.browser.find_element(by=parent_by, value=parent_val)
            field = WebDriverWait(parent_elem, 10).until(EC.element_to_be_clickable((by, value)))
        else:
            field = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((by, value)))
        field.send_keys(text)

    def clickButton(self, by: By, value: str, parent_by = '', parent_val = ''): # ANCHOR klikanie w przycisk
        if parent_by != '' and parent_val != '':                                 # można podać pojemnik nadrzędny parent buttona w razie problemów
            parent_elem = self.browser.find_element(by=parent_by, value=parent_val)
            button = WebDriverWait(parent_elem, 10).until(EC.element_to_be_clickable((by, value)))
        else:
            button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((by, value)))
        button.click()