# Created by DNw XI2023

from bs4 import BeautifulSoup
import requests

class SiteProductLinkFinder: # SECTION klasa pobierająca określone linki z mapy strony
                             # w obecnej konfiguracji pobiera linki do produktów z pl.uzin.com
    def __init__(self, sitemap_url):
        self.links_base = {}
        self.sitemap_url = sitemap_url

    def getLinksBase(self): # ANCHOR tworzenie listy linków do produktów
        response = requests.get(self.sitemap_url) # NOTE pobieranie mapy strony z linku
        
        if response.status_code == 200:
            sitemap_content = response.text
            sitemap_soup = BeautifulSoup(sitemap_content, "xml") # NOTE przetwarzanie pobranej zawartości na bs

            for loc in sitemap_soup.find_all("loc"): # NOTE wyciąganie linków do podmap
                if loc:
                    sub_sitemap = requests.get(loc.text) # NOTE pobieranie podmap

                    if sub_sitemap.status_code == 200:
                        sub_sitemap_content = sub_sitemap.text

                        sub_sitemap_soup = BeautifulSoup(sub_sitemap_content, "xml") # NOTE przetwarzanie pobranej zawartości podmap

                        for category_url in sub_sitemap_soup.find_all('loc'): # NOTE pobieranie linków do kategorii
                            if 'przeglad-produktow/' in category_url.text and 'przeglad-produktow/przeglad-produktow' not in category_url.text:
                                if category_url not in self.links_base:
                                    self.links_base[category_url.text] = [] # NOTE tworzenie słownika z kategoriami

                                    category_response = requests.get(category_url.text)
                                    category_soup = BeautifulSoup(category_response.text, "html.parser")

                                    for link in category_soup.find_all('a'): # NOTE pobieranie linków do produktów z kategorii
                                        if type(link.get("href")) == type("str"):
                                            if 'produkt/' in link.get("href"):
                                                url_product = link.get("href")
                                                if url_product not in self.links_base[category_url.text]:
                                                    self.links_base[category_url.text].append(url_product) # dodawanie produktów do słownika danej kategorii
                    else:
                            print("Nie udało się pobrać podmapy strony")
        else:
            print("Nie udało się pobrać mapy strony.")

    def getCategoryBaseSize(self): # ANCHOR rozmiar pobranej listy kategorii
        return len(self.links_base)
    
    def getProductBaseSize(self): # ANCHOR rozmiar pobranej listy produktów
        sum = 0
        for cat in self.links_base:
            sum += len(self.links_base[cat])
        return sum
