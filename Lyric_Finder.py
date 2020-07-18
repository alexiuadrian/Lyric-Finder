import bs4
import requests
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getLyrics(url):
    print(url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    try:
        lyrics = soup.find_all('div', class_='lyrics')
    except Exception:
        browser.close()

    if len(lyrics) == 0:
        print('Not found in .lyrics div')
        lyrics = soup.find_all('div', class_='Lyrics__Container')
    
    return lyrics

song = input()

browser = webdriver.Firefox()

browser.get('https://genius.com/')

search = browser.find_element_by_css_selector('.PageHeaderSearchdesktop__Input-eom9vk-2')

search.send_keys(song)
search.submit()

delay = 8

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.column_layout-column_span:nth-child(1) > div:nth-child(1) > search-result-section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > search-result-items:nth-child(1) > div:nth-child(1) > search-result-item:nth-child(1) > div:nth-child(1) > mini-song-card:nth-child(1) > a:nth-child(1) > div:nth-child(2)')))
    #print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

try:
    best_match = browser.find_element_by_css_selector('div.column_layout-column_span:nth-child(1) > div:nth-child(1) > search-result-section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > search-result-items:nth-child(1) > div:nth-child(1) > search-result-item:nth-child(1) > div:nth-child(1) > mini-song-card:nth-child(1) > a:nth-child(1) > div:nth-child(2)')
    best_match.click()
except Exception:
    browser.close()

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'lyrics')))
    #print("Page is ready!")
except TimeoutException:
    try:
        myElem = WebDriverWait(browser, 0).until(EC.presence_of_element_located((By.CLASS_NAME, 'Lyrics__Container')))
    except TimeoutException:
        print("Loading took too much time!")

lyrics = getLyrics(browser.current_url)

print(lyrics[0].text)

# for i in range(0, len(lyrics)):
#     if len(lyrics[i].text) > 50:
#         print(lyrics[i].text)
    
browser.close()