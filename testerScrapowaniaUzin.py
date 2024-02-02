# Created by DNw XI2023

# ANCHOR plik do testowania productDataDownloader'a dla poszczególnych produktów

from src.SiteProductLinkFinder import SiteProductLinkFinder
from src.ProductDataDownloader import ProductDataDownloader
from src.ScraperUzin import ScraperUzin
from src.Browser import Browser

#linkFinder = SiteProductLinkFinder("https://pl.uzin.com/sitemap.xml")
#linkFinder.getLinksBase()

browser = Browser()
browser.openPage("https://pl.uzin.com/szczegoly/produkt/1528/uzin-sc-912-ergo")

productDataDownloader = ProductDataDownloader()

productDataDownloader.loadSiteData(browser.browser.page_source)

productDataDownloader.getCharacteristics()
productDataDownloader.getGoodsDepartments('https://pl.uzin.com/produkty/przeglad-produktow/ukladanie-jastrychow/uzin-turbolightr-system-jatrychy')
productDataDownloader.getIds()
productDataDownloader.addProductToQueue()
productDataDownloader.product.printDetails()
#productDataDownloader.exportToXlsx()

browser.closeBrowser()


