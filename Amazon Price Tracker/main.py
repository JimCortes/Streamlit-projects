import streamlit as st
import streamlit.components.v1 as stc 
from requests_html import HTMLSession
import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
import sqlite3
import datetime


conn = sqlite3.connect('history.db')
c = conn.cursor()



title = """
<div style="font-size:60px;font-weight:bolder;background-color:#fff;padding:10px;
border-radius:30px;border:5px solid #464e5f;text-align:center;">
		<span style='color:blue'>Price Tracker</span>
		
</div>
"""

def table():
    c.execute('CREATE TABLE IF NOT EXISTS historytable(title TEXT,price TEXT,image TEXT, postdate,DATE)')

table()

def add(title,price, image, postdate):
    c.execute('INSERT INTO historytable(title,price, image, postdate) VALUES (?,?,?,?)',(title,price,image,postdate))
    conn.commit()

def history():
    c.execute('SELECT * FROM historytable')
    data = c.fetchall()
    return data



#url = "https://www.amazon.co.uk/Apple-Airpods-Wireless-Charging-latest/dp/B07PYM8FB8/ref=sr_1_6?keywords=airpods&qid=1581244893&sr=8-6"

@st.cache
def getInfo(url):
    s = HTMLSession()
    r = s.get(url)

    try:
        image = r.html.xpath('//*[@id="landingImage"]', first=True).attrs
        image = image['data-old-hires']
    
        product = {
            'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
            'price': r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text,
            'image':image            
        }

    except:

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            title = soup.select_one(selector="#productTitle").getText()

            product = {
            'title': title.strip(),
            'price': soup.select_one(selector="#priceblock_ourprice").getText(),
            
                    }



        except:

            product = {
            'title': "No iteam",
            'price': "not value",
            
                    }

    
    return product


stc.html(title)
menu = ["Home","History"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    url = st.text_input('Enter URLss to track')
    if url != "":        
        try:
            item = getInfo(url)
            title = item["title"]
            price = item["price"]
            image = item['image']
            st.write(title)
            picture = st.image(image,width=400)
            st.write("price:",price)
        except:
            item = getInfo(url)
            title = item["title"]
            price = item["price"]
            st.write(title)
            image = st.image("image.png")
            st.write("price:",price)
            if st.button("json"):
                st.button("close")
                st.write(item)
            if st.button("add"):
                add(title,price,str(image),str(datetime.datetime.now()))
        else:
            pass                    
else:
    a = pd.DataFrame(history())
    st.write(a)