from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_data(link):
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    isins = []
    for isin in soup.findAll('td', attrs={'class': 'views-field views-field-field-code-isin'}):
        isins.append(isin.text.replace('\n', ''))

    addings = []
    for info in soup.findAll('td', attrs={'class': 'views-field views-field-title'}):
        addings.append(info.text.replace('\n', ''))
    additional_info = []
    for i in addings:
        i = re.split("\s", i)
        additional_info.append(list(filter(None, i)))

    df = pd.DataFrame(isins, columns=["ISIN"])

    for i in range(len(additional_info)):
        df.at[i, "type"] = additional_info[i][0]
        df.at[i, "coupon"] = additional_info[i][1]
        df.at[i, "mat_day"] = additional_info[i][2]
        df.at[i, "mat_month"] = additional_info[i][3]
        df.at[i, "mat_year"] = additional_info[i][4]

    return df


driver = webdriver.Chrome()
bonds = get_data('https://www.aft.gouv.fr/en/encours-detaille-oatei')
driver.quit()

print(bonds)
