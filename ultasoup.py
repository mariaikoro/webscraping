import requests
from bs4 import BeautifulSoup

URL = "https://www.ulta.com/skin-care-treatment-serums-face-serums?N=27he"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

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
    ingredients = itemSoup.find("div", class_ = "ProductDetail__ingredients")
    ingredients= ingredients.find("div", "ProductDetail__productContent")
    ingredients = ingredients.text.split(", ")
    #print(brand.text)
    #print(name.text+ "\n" *2)
    #print(ingredients)
#have the links and can extract the names from either the link page or scraping page
#can just scrape link and go to link and scrape stuff from there to save