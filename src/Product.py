# Created by DNw XI2023

class Product:
    def __init__(self):
        self.soup = None
        self.name_soup = None
        self.response = None

        self.name = ''
        self.additional_name = ''
        self.description = ''
        self.long_description = ''
        self.photo = ''
        self.technical_card = ''
        self.dzialtow3 = ''
        self.dzialtow4 = ''

        self.qualities = {}

        self.size_code_list = []

    def printDetails(self):
        print(f"\033[37m\t\t Kod producenta: {self.size_code_list}")
        print(f"\033[37m\t\t Nazwa towaru: {self.name}")
        print(f"\033[37m\t\t Nazwa dodatkowa: {self.additional_name}")
        print(f"\033[37m\t\t CECHA_DOD_Opis: {self.description}")
        print(f"\033[37m\t\t CECHA_DOD_Dlugi_Opis: {len(self.long_description)}")
        print(f"\033[37m\t\t Dzial towarowy 3: {self.dzialtow3}")
        print(f"\033[37m\t\t Dzial towarowy 4: {self.dzialtow4}")

        for key, val in self.qualities.items():
            print(f'\033[37m\t\t {key}: {val}')

        print(f"\033[37m\t\t Zdjecie: {self.photo}")