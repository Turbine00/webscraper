from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re


def scraper(link):
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    isins = []
    for isin in soup.findAll('td', attrs={'class': 'views-field views-field-field-code-isin'}):
        isins.append(isin.text.replace('\n', ''))

    additional = []
    for description in soup.findAll('td', attrs={'class': 'views-field views-field-title'}):
        additional.append(description.text.replace('\n', ''))
    data = []
    for i in additional:
        i = re.split("\s", i)
        data.append(list(filter(None, i)))

    df = pd.DataFrame(isins, columns=["ISIN"])

    for i in range(len(additional_info)):
        df.at[i, "type"] = data[i][0]
        df.at[i, "coupon"] = data[i][1]
        df.at[i, "mat_day"] = data[i][2]
        df.at[i, "mat_month"] = data[i][3]
        df.at[i, "mat_year"] = data[i][4]

    return df


link = "https://www.aft.gouv.fr/en/encours-detaille-oatei"  #insert website link to retrieve data from

driver = webdriver.Chrome()
bonds = scraper(link)
driver.quit()

print(bonds)
