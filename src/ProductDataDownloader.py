# Created by DNw XI2023

import os
import shutil
import openpyxl
import requests
from bs4 import BeautifulSoup
import datetime

from src.Product import Product

class ProductDataDownloader: # SECTION klasa do scrapowania stron
                             # w obecnej konfiguracji scrapuje www.remmers.pl
    def __init__(self):
        self.product = Product()
        self.labels = [
            'Kod producenta',
            'Nazwa towaru',
            'Nazwa dodatkowa',
            'Jm.',
            'Opis towaru',
            'CECHA_DOD_Dlugi_Opis',
            'Dzial towarowy_1',
            'Dzial towarowy_2',
            'Dzial towarowy_3',
            'Dzial towarowy_4',
            'CECHA_DOD_Karta_techniczna',
            'Zdjecie 1'
            ]
        
        self.queue = []
        self.exportQueue = []
        self.quality_labels = {}

        self.resetFolder()

    def resetFolder(self): # ANCHOR reset folderu na zdjęcia
        if os.path.exists('photos/'):
            shutil.rmtree('photos/')

        if not os.path.exists('photos/'):
            os.makedirs('photos/')

    def loadSiteData(self, product_src): # ANCHOR pobieranie kodu strony
        #self.product.response = requests.get(product_url)
        self.product.soup = BeautifulSoup(product_src, 'html.parser')

        self.product.name_soup = self.product.soup.find('div', class_="productsDetailInner")

    def getCharacteristics(self): # ANCHOR ustawianie podstawowych cech produktu
        # NOTE nazwa
        self.product.name = self.product.name_soup.find('h2').text

        if self.product.name_soup.find('h2').find('span'):
            self.product.additional_name = self.product.name_soup.find('h2').find('span').text

            self.product.name = self.product.name[:len(self.product.name)-len(self.product.additional_name)]

        else:
            self.product.additional_name = ""

        # NOTE opis
        if self.product.name_soup.find('p'):
            self.product.description = self.product.name_soup.find('p').text
        if self.product.name_soup.find('ul') and self.product.name_soup.find('ul').get('class') != ['list-icons', 'list-icons-large']:
            self.product.description += f"{self.product.name_soup.find('ul')}"
        else:
            self.product.description = ""

        # NOTE opis dlugi
        if self.product.soup.find('section', id = 'product-application'):
            self.product.long_description += self.product.soup.find('section', id = 'product-application').prettify()

        # NOTE zdjecie
        self.product.photo = self.product.soup.find('div', class_='productImage').get("style")
        prefix = "background-image: url('"
        self.product.photo = f"https://pl.uzin.com{self.product.photo[len(prefix):len(self.product.photo)-2]}"

        try:
            img_response = requests.get(self.product.photo)
            img_response.raise_for_status()

            photo_n = self.product.name

            if " " in self.product.name:
                photo_n = self.product.name.replace(' ','_')

            if "/" in self.product.name:
                photo_n = self.product.name.replace('/','')

            if "\\" in self.product.name:
                photo_n = self.product.name.replace('\\','')

            with open(f'photos/{photo_n}-photo.png', 'wb') as img_file:
                img_file.write(img_response.content)
                
            self.product.photo = f'{photo_n}-photo.png'
        except requests.exceptions.RequestException as e:
            print(e)
            self.product.photo = ''

        # NOTE karta techniczna
        self.product.technical_card = self.product.soup.find('ul', class_='list-icons list-icons-large').find('a')

        if self.product.technical_card and self.product.technical_card.get("href") != '#':
            self.product.technical_card = self.product.technical_card.get("href")
            self.product.technical_card = f"https://pl.uzin.com{self.product.technical_card}"
        else:
            self.product.technical_card = ''

        # NOTE cechy
        technical_data_list = self.product.soup.find('div', id='tabContentTechnicalData').findAll('tr')
        
        self.product.qualities = {}

        for quality in technical_data_list:
            key = quality.find('th').text.strip().replace(' ','_').replace('.','').replace(':','')
            value = quality.find('td').text.strip()

            self.product.qualities["CECHA_DOD_"+key] = value.replace('²','2').replace('°', 'st').replace('Ø','fi')
            self.quality_labels["CECHA_DOD_"+key] = ''

    def getGoodsDepartments(self, category_url): # ANCHOR ustawianie działów towarowych, wspólne dla kategorii
        category_response = requests.get(category_url)
        soup_ct = BeautifulSoup(category_response.text, "html.parser")

        self.product.dzialtow3 = soup_ct.find_all('li', class_="breadcrumb-item")[-2].text
        self.product.dzialtow4 = soup_ct.find('li', class_="breadcrumb-item active").text #category_url.text

    def getIds(self): # ANCHOR tworzenie listy z kodami produktów i odpowiadającymi im wagami
        code_list = self.product.soup.find('div', id='tabContentArticles').findAll('th')
        code_index = 0
        art_index = 0
        size_index = 0
        self.product.size_code_list = []

        for i, elem in enumerate(code_list):
            if 'Artykuł' in elem.text:
                art_index = i
            if 'Numer artykułu' in elem.text:
                code_index = i
            if 'Wielkość opakowania' in elem.text:
                size_index = i

        code_list = self.product.soup.find('div', id= 'tabContentArticles').find('tbody')

        if code_list:

            for elem in code_list.findAll('tr'):
                self.product.size_code_list.append([art_index, code_index, size_index, elem.findAll('td')[art_index].text, elem.findAll('td')[code_index].text, elem.findAll('td')[size_index].text])

    def addProductToQueue(self): # ANCHOR funkcja przygotowuje produkt i dodaje go do kolejki dodawania do excela 
        if len(self.product.size_code_list) > 0: # NOTE Zapis produktu jeśli znaleziono kilka wariantów wagowych
            for lst in self.product.size_code_list:

                if lst[3] != lst[4]:
                    name_pt_tmp = lst[3]
                else:
                    name_pt_tmp = self.product.name

                self.queue.append({
                'Kod producenta': lst[4], # Kod producenta
                'Nazwa towaru': name_pt_tmp.replace('Ø', 'fi').replace('\xf8', 'fi'), # Nazwa towaru
                'Nazwa dodatkowa': self.product.additional_name, # Nazwa dodatkowa
                'Jm.': 'szt', # Jm.
                'CECHA_DOD_Opis': self.product.description, # Opis
                'CECHA_DOD_Dlugi_Opis': self.product.long_description, # Dlugi opis
                'Dzial towarowy_1': 'Chemia budowlana', # tow1
                'Dzial towarowy_2': 'Uzin', # tow2
                'Dzial towarowy_3': self.product.dzialtow3, # tow3
                'Dzial towarowy_4': self.product.dzialtow4, # tow4
                'CECHA_DOD_Karta_Techniczna': self.product.technical_card, # Karta techniczna
                'Zdjecie 1': self.product.photo, # Zdjecie
                })

                for key, val in self.product.qualities.items():
                    self.queue[-1][key] = val
        
        elif len(self.product.size_code_list) == 0: # NOTE Zapis produktu jeśli znaleziono tylko jeden wariant wagowy
            self.queue.append({
                'Kod producenta': '', # Kod producenta
                'Nazwa towaru': self.product.name, # Nazwa towaru
                'Nazwa dodatkowa': self.product.additional_name, # Nazwa dodatkowa
                'Jm.': 'szt', # Jm.
                'CECHA_DOD_Opis': self.product.description, # Opis
                'CECHA_DOD_Dlugi_Opis': self.product.long_description, # Dlugi opis
                'Dzial towarowy_1': 'Chemia budowlana', # tow1
                'Dzial towarowy_2': 'Uzin', # tow2
                'Dzial towarowy_3': self.product.dzialtow3, # tow3
                'Dzial towarowy_4': self.product.dzialtow4, # tow4
                'CECHA_DOD_Karta_Techniczna': self.product.technical_card, # Karta techniczna
                'Zdjecie 1': self.product.photo, # Zdjecie
            })
            
            for key, val in self.product.qualities.items():
                    self.queue[-1][key] = val

    def generateLabels(self): # ANCHOR generowanie brakujących pustych cech dla produktów, aby każdy produkt miał taką samą ilość cech

        self.labels = [
            'Kod producenta',
            'Nazwa towaru',
            'Nazwa dodatkowa',
            'Jm.',
            'Opis towaru',
            'CECHA_DOD_Dlugi_Opis',
            'Dzial towarowy_1',
            'Dzial towarowy_2',
            'Dzial towarowy_3',
            'Dzial towarowy_4',
            ]

        for key, val in self.quality_labels.items():
            self.labels.append(key)

        self.labels.append('CECHA_DOD_Karta_techniczna')
        self.labels.append('Zdjecie 1')
            
        self.export_queue = [self.labels]

        for i, row in enumerate(self.queue):
            for label in self.labels:
                if label not in row.keys():
                    self.queue[i][label] = ''

        for i, row in enumerate(self.queue):
            tmp_row = []
            for label in self.labels:
                tmp_row.append(row[label])

            self.export_queue.append(tmp_row)

    def numberToExcelColId(self, numer): # ANCHOR konwersja indexu pętli na numer kolumny w excelu
        identyfikator = ""
        while numer > 0:
            modulo = (numer - 1) % 26
            litera = chr(65 + modulo)
            identyfikator = litera + identyfikator
            numer = (numer - modulo) // 26
        return identyfikator

    def exportToXlsx(self): # ANCHOR funkcja importuje utworzoną kolejkę do excela
        self.generateLabels()
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for i, row in enumerate(self.export_queue):
            for j, col in enumerate(row):
                sheet[f'{self.numberToExcelColId(j+1)}{i+1}'] = str(self.export_queue[i][j])

        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year

        name = f"uzin_from_website_{day}_{month}_{year}.xlsx"

        workbook.save(name)
        workbook.close()
