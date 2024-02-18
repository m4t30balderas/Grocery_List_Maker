import gspread
import httpx
import pandas as pd
from dataclasses import dataclass, asdict
from selectolax.parser import HTMLParser
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="root",
    database="recipes"
    )
    
mycursor = db.cursor()


#mycursor.execute("CREATE TABLE Ingredient (item VARCHAR(50), ammount smallint UNSIGNED, unit VARCHAR(50))")


#python -m venv venv
# In cmd.exe
#venv\Scripts\activate.bat
# In PowerShell
#venv\Scripts\Activate.ps1

@dataclass
class ingredient_details:
    ammount: str
    unit: str
    item: str
    note: str


def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
            return None

def get_html(baseurl):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    resp = httpx.get(baseurl, headers=headers)
    html = HTMLParser(resp.text)
    return html

def parse_page(html):
    ingredients = html.css("li.wprm-recipe-ingredient, li.leading-snug")
    Recipe = []
    for ingredient in ingredients:
        item = ingredient_details( 
            ammount=extract_text(ingredient,".wprm-recipe-ingredient-amount, .quantity"), 
            unit=extract_text(ingredient,".wprm-recipe-ingredient-unit, .unit"), 
            item=extract_text(ingredient,".wprm-recipe-ingredient-name, .label"),
            note=extract_text(ingredient,".wprm-recipe-ingredient-notes, .modifier")
            )
        ingredient_data = Recipe.append(asdict(item))

        #mycursor.execute("INSERT INTO Ingredient (item, ammount, unit) VALUES (%s, %s, %s)", (item.item, item.ammount, item.unit))
        #db.commit()

        #mycursor.execute("SELECT * FROM Ingredient")

        #for x in mycursor:
            #print(x)
          
    return Recipe

def main():
    grocery_list = []
    
    
    #DEC_recipe_url = [
        #"https://www.julieseatsandtreats.com/instant-pot-pressure-cooker-french-dip-sandwich/",
        #"https://www.thetravelpalate.com/instant-pot-mexican-beans/",
        #"https://tastesbetterfromscratch.com/instant-pot-mexican-rice/?utm_term=mexican+food+recipes&utm_campaign=2036652051",
        #"https://www.mommysfabulousfinds.com/crockpot-hawaiian-chicken/",
        #"https://happymoneysaver.com/boneless-country-style-bbq-ribs-slow-cooker-freezer-meal/",
        #"https://diethood.com/instant-pot-chicken-tinga/",
        #"https://bytesandyum.com/chicken-adobo-instant-pot/",
        #"https://www.themagicalslowcooker.com/slow-cooker-cheesy-chicken-penne/",
        #"https://kristineskitchenblog.com/instant-pot-carnitas/",
        #"https://thenovicechefblog.com/caldo-de-res-mexican-beef-soup/",
        #"https://www.acozykitchen.com/horchata-coffee",
    #]

    #FEB_recipe_url = [
        #"https://twosleevers.com/caldo-de-res",
        #"https://twosleevers.com/instant-pot-caldo-de-pollo/",
        #"https://bitesofwellness.com/instant-pot-shredded-mexican-chicken/",
        #"https://www.berlyskitchen.com/instant-pot-sausage-chicken-jambalaya/",
        #"https://www.shugarysweets.com/bourbon-chicken/",
        #"https://thefoodieeats.com/pressure-cooker-pho-ga/",
        #"https://www.simplyhappyfoodie.com/instant-pot-korean-ground-beef-bulgogi/",
        #"https://www.ihearteating.com/instant-pot-korean-beef/",
        #"https://www.savorysweetspoon.com/instant-pot-mississippi-pot-roast/",
        #"https://iamhomesteader.com/roasted-potato-breakfast-casserole/",
        #"https://sweetandsavorymeals.com/croissant-french-toast-casserole/",
        #"https://www.scratchpantry.com/recipes/christmas-breakfast-casserole",
        #"https://www.scratchpantry.com/recipes/peach-chili-chicken",
        #"https://www.scratchpantry.com/recipes/honey-ginger-chicken-marinade",
        #"https://www.scratchpantry.com/recipes/balsamic-chicken-marinade",
    #]

    TEST_recipe_url = [
    "https://twosleevers.com/caldo-de-res",
    "https://thefoodieeats.com/pressure-cooker-pho-ga/"
    ]


    for url in TEST_recipe_url:  
      baseurl = url
      html = get_html(baseurl)
      parse_page(html)
      (parse_page(html))
      grocery_list.append((parse_page(html)))

    #print(grocery_list)
    # Your nested dictionary inside a list
    data = []
    for sublist in grocery_list:
        data.extend(sublist)
    print(data)

    # Convert the nested dictionary list to a DataFrame
    df = pd.json_normalize(data)
    print(df)
    
    sa = gspread.service_account(r"C:\Users\Ki11e\OneDrive\Desktop\Meals\service_account.json")
    sh = sa.open("GROCERY LIST")
    wks = sh.worksheet("EXPORT")

    wks.update(range_name='A1', values=([df.columns.values.tolist()] + df.values.tolist()))

if __name__ == "__main__":
    main()    


db = mysql.connector.connect()


