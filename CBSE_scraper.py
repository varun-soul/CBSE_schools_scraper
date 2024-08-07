from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd

options = ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

def loadpage():
    driver.get("https://saras.cbse.gov.in/cbse_aff/schdir_Report/userview.aspx")
    state_radio = driver.find_element(By.XPATH,"//input[@id='optlist_2']")
    state_radio.click()
    driver.implicitly_wait(3)

loadpage()

states_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlitem']")
search_button = driver.find_element(By.XPATH, "//input[@id='search']")   
data = []

for i in range (1,39):
    states_dropdown = driver.find_element(By.XPATH, "//select[@id='ddlitem']")
    
    Select(states_dropdown).select_by_index(i)
    driver.implicitly_wait(3)

    search_button = driver.find_element(By.XPATH, "//input[@id='search']")   
    
    search_button.click()
    driver.implicitly_wait(3)

    total_schools = int(driver.find_element(By.XPATH, "//span[@id='lbltotal1']").text)
    total_pages = int(total_schools/25)+1
    school_links = []
    
    for j in range(total_pages):
        
        big_table = driver.find_element(By.XPATH, "//table[@id='T1']")        
        link_element = big_table.find_elements(By.TAG_NAME, "a")
        for link in link_element:
            if link not in school_links:
                school_links.append(link.get_attribute('href'))

        next_page_button = driver.find_element(By.XPATH, "//input[@id='Button1']")
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].click();", next_page_button)
        
    for links in school_links:
            
        driver.get(links)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        link_table = soup.find('table', {'bordercolorlight': '#808080', 'bordercolordark': '#808080'})
        rows = link_table.find_all('tr')

        dict = {}

        for row in rows[2:]:
            cell = row.find_all('td')
            if len(cell)>1:
                label = cell[0].get_text(strip = True)
                value = cell[1].get_text(strip = True)
                dict.update({label:value})
        
        data.append(dict)
    
    loadpage()

df = pd.DataFrame(data).fillna(0)
df.drop_duplicates(inplace = True)

file_name = "cbse_school_data.xlsx"
df.to_excel(file_name)




