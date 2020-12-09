
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from flask import Markup

#define function scrape
def scrape():
    #Scarping News
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    n_title=soup.find("div", class_="content_title").a.text.strip('\n')
    n_pgraph=soup.find("div", class_="rollover_description_inner").text.strip('\n')

    #Adding variables to a Dictionary
    mars={
        "Title":n_title,
        "Description":n_pgraph
    }

    #Scraping Images
    #executable_path={"executable_path":ChromeDriverManager().install()}
    #browser=Browser("chrome", **executable_path, headless=False)

    #My computer has a internet service controlled by my company, I can´t use the "Robot" tool for scrappe, but here would be the code needed to create browser
    #browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    #html=browser.html
    #soup=BeautifulSoup(html,"html.parser")

    #Using regular scrapping with Get method
    url_i="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response_i=requests.get(url_i)
    soup=BeautifulSoup(response_i.text,"html.parser")
    image_url = soup.find("div", class_="carousel_items").a["data-fancybox-href"]
    featured_image_url=f"https://www.jpl.nasa.gov{image_url}"
    mars["imageURL"]=featured_image_url

    #Scrapping Facts
    facts_url="https://space-facts.com/mars/"
    facts=pd.read_html(facts_url)
    facts_table=facts[0].copy()
    facts_table=facts_table.rename(columns={0:"Title",1:"Value"})
    facts_table_html=Markup(facts_table.to_html())
    mars["facts_table"]=facts_table_html

    #Scrapping Hemispheres
    hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response=requests.get(hemispheres_url)
    soup=BeautifulSoup(response.text,"html.parser")
    hemispheres=soup.find_all("div",class_="item")
    mars_hemispheres=[]
    for h in hemispheres:
        img_url_aux=h.a.img["src"]
        h_description=h.div.h3.text.rstrip(" Enhanced")
        mars_hemispheres.append(
        {
            "Hemisphere":h_description,
            "URL":f"https://astrogeology.usgs.gov/{img_url_aux}"
        }
        )
    mars["hemispheres"]=mars_hemispheres

    return(mars)


