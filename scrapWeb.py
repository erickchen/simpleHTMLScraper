from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from pathlib import Path

#url-test = 'https://cards-loan.cimbniaga.co.id/CreditCard/NewsInfoDetail/NWS-061118-00001'

#initiate method
def scrapWebsite():
    try:
        url =  input("Input Your URL Request Here: ")
        page = requests.get(url)  
        findTag = input("What tag you want to look for ?\nTry tbody\n")  
    except Exception as e:
        print("type error:" + str(e))

    #initiate parsing html from requested url and find HTML Tag.
    def initFindHTMLTag (page,url,findTag):
        soup = BeautifulSoup(page.text, 'html.parser')
        tableData = []

        #find HTML Element. In this case i'm looking for tbody tag
        findTable = soup.find(findTag)

        #looping all ROW inside findTable. As we know that tbody inside has more than one tr and td
        if findTag == 'tbody':
            for row in findTable.find_all('tr'):
                #find_all is for looking all html which has defined html tag. In this case we're looking for all td inside tr
                cols = row.find_all('td')
                if len(cols) == 4:
                    tableData.append((cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip()))
                df = pd.DataFrame(tableData)

                df.columns = ['','','']

        printDF = df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["","-"], regex=True)
        return printDF

    #export file to CSV
    def exportFile(printDF):
        my_file = Path("promo.csv")
        if my_file.exists():
            os.remove("promo.csv")
            printDF.to_csv('promo.csv')
        else: 
            printDF.to_csv('promo.csv')   
        print("Your CSV File has been exported")

    #check website existence
    if page.status_code == 200:
        printDF = initFindHTMLTag(page,url,findTag)
        exportFile(printDF)
    else:
        print("Your Requested URL does not exist")

scrapWebsite()
