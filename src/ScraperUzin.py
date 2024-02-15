# Created by DNw XI2023

from src.SiteProductLinkFinder import SiteProductLinkFinder
from src.ProductDataDownloader import ProductDataDownloader
from src.Browser import Browser

class ScraperUzin:
    def __init__(self):
        try:
            self.linkFinder = SiteProductLinkFinder('https://pl.uzin.com/sitemap.xml')
            self.productDataDownloader = ProductDataDownloader()
            self.browserConnector = Browser()

            self.done_count = 0
        except Exception as e:
            print("Wystąpił problem podczas logowania")
            print(e)


    def getProductLinks(self): # ANCHOR generowanie linków
        try:
            print("Pobieranie linków do produktów ...")
            self.linkFinder.getLinksBase()
        except Exception as e:
            print("Wystąpił problem podczas pobierania bazy linków")
            print(e)

    def scrapProducts(self): # ANCHOR główna funkcjonalność, przechodzenie przez wszystkie produkty we wszystkich kategoriach
        with open('errorlogs.txt', 'w', encoding='utf-8') as errfile:
            errfile.write('')
        try:
            for category_link in self.linkFinder.links_base:
                for product_link in self.linkFinder.links_base[category_link]:
                    try:
                        self.browserConnector.openPage(product_link)
                        self.productDataDownloader.loadSiteData(self.browserConnector.browser.page_source)
                        self.productDataDownloader.getCharacteristics()
                        self.productDataDownloader.getGoodsDepartments(category_link)
                        self.productDataDownloader.getIds()
                        self.productDataDownloader.addProductToQueue()
                        self.exportToXlsx()
                        self.done_count += 1
                    except Exception as e:
                        print("Wystąpił problem podczas pobierania produktów! Sprawdź produkt testerem scrapowania!")
                        with open('errorlogs.txt', 'a', encoding='utf-8') as errfile:
                            errfile.write(f'{product_link} [] {category_link}\n')
                        print(category_link)
                        print(product_link)
                        print(e)

                    print(f"Pobrano {self.done_count}/{self.linkFinder.getProductBaseSize()}")

            self.browserConnector.closeBrowser()

        except Exception as e:
            print("Wystąpił problem podczas pobierania produktów")
            print(e)

    def exportToXlsx(self): # ANCHOR export
        try:
            print("Exportowanie do xlsx")
            self.productDataDownloader.exportToXlsx()
            print("Wyeksportowano")
        except Exception as e:
            print("Wystąpił problem z exportem do xlsx")
            print(e)