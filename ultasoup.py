import requests
from bs4 import BeautifulSoup
import math

#tested on Face Serums section of Ulta.com
#when translating to database use entire Face Treatments Section
#make sure to change URL for database writing


URL = "https://www.ulta.com/skin-care-treatment-serums-face-serums?N=27he&No=0&Nrpp=96"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

#get number of pages to loop through multiple pages with for loop
number = soup.find("span", class_ = "search-res-number")
pages = math.ceil(int(number.text) / 96)
items= 0


for i in range(0,pages):
    results = soup.find(id = "foo16")

    serums = soup.find_all("div", class_ = "productQvContainer")


    for serum in serums:
        link = serum.find("a")['href']
        itemURL = "https://www.ulta.com" + link
        try:
            itemPage = requests.get(itemURL)
        except:
            print("ERROR AT " + itemURL)
            continue
        itemSoup = BeautifulSoup(itemPage.content, 'lxml')
        brand = itemSoup.find("p", class_ = "Text Text--body-1 Text--left Text--bold Text--small Text--$magenta-50")
        name = itemSoup.find("span", class_ = "Text Text--subtitle-1 Text--left Text--small Text--text-20")

        #some items do not have ingredients listed
        ingredients = itemSoup.find("div", class_ = "ProductDetail__ingredients")
        try:
            ingredients= ingredients.find("div", "ProductDetail__productContent")   
        except:
            print(brand.text)
            print(name.text)
            print("No ingredients at " + itemURL)
            continue
        ingredients = ingredients.text.split(", ")
        #print(brand.text)
        #print(name.text+ "\n" *2)
        #print(ingredients)
        #print("\n")
    items += 96
    URL = f'https://www.ulta.com/skin-care-treatment-serums-face-serums?N=27he&No={items}&Nrpp=96'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')

#have the links and can extract the names from either the link page or scraping page
#can just scrape link and go to link and scrape stuff from there to save