# Created by DNw XI2023

from src.ScraperUzin import ScraperUzin

scraper = ScraperUzin()

scraper.getProductLinks()
scraper.scrapProducts()
scraper.exportToXlsx()

print("Można zakończyć działanie programu")

