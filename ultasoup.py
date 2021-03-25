import requests
from bs4 import BeautifulSoup
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#initialize database

cred = credentials.Certificate("./ServiceKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


SCRAPING_ON = False

def query_database(collection, name):
    #this checks if query exists and returns an id
    doc_ref = db.collection(collection)
    query = doc_ref.where(u'name', u'==', name).get()
    if len(query) == 0:
        doc_ref = db.collection(collection).document()
        doc_ref.set({
            u'name': name,
        })
        return doc_ref.id
    return query[0].id


def add_data(item, brand, ingredients):
    #first check if brand exists in db
    brand_id = query_database(u'brands', brand)

    #store ingredients by specific id in an array
    arr = []
    for ingredient in ingredients:
        #slight fix for ingredients
        if "." in ingredient and ingredient == ingredients[-1]:
            ind = ingredient.index(".")
            ingredient = ingredient[:ind]

        arr.append(query_database(u'ingredients', ingredient.lower()))

    doc_ref = db.collection(u'items').document()
    doc_ref.set({
        u'name': item,
        u'brandID': brand_id,
        u'ingredients': arr
    })


#tested on Face Serums section of Ulta.com
#make sure to change URL for database writing for different sections
#can also make driver code later for longer webscraping


#database notes
#check if last item begins with "and"
#some have ingredients separated by active or inactive Or they come in a set
#active inactive are typically one set and need to be split, may have to correct later




if SCRAPING_ON == True:
    URL = "https://www.ulta.com/skin-care-treatment-serums-face-serums?N=27he&No=0&Nrpp=96"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')

    #get number of pages to loop through
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
                try:
                    #try original link without ulta.com root
                    itemPage = requests.get(link)
                except:
                    print("Unresolved Error at" + link)
                    continue
            itemSoup = BeautifulSoup(itemPage.content, 'lxml')
            brand = itemSoup.find("p", class_ = "Text Text--body-1 Text--left Text--bold Text--small Text--$magenta-50")
            name = itemSoup.find("span", class_ = "Text Text--subtitle-1 Text--left Text--small Text--text-20")

            #some items do not have ingredients listed
            ingredients = itemSoup.find("div", class_ = "ProductDetail__ingredients")
            try:
                ingredients= ingredients.find("div", "ProductDetail__productContent")   
            except:
                #no listed ingredients, skip
                #without ingredients, will not help filter
                continue
            ingredients = ingredients.text.split(", ")

            doc_ref = db.collection(u'items')
            query = doc_ref.where(u'name', u'==', name.text).get()
            if len(query) > 0:
                continue
            add_data(name.text, brand.text, ingredients)
            
        items += 96
        URL = f'https://www.ulta.com/skin-care-treatment-serums-face-serums?N=27he&No={items}&Nrpp=96'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')