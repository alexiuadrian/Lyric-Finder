import bs4
import requests
import sys
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getLyrics(url):
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    try:
        lyrics = soup.find(class_='lyrics')
    except Exception:
        try:
            lyrics = soup.find(class_='Lyrics__Container')
        except Exception:
            return "Try again"

    if lyrics is None:
        return "Try again"
    else:
        return lyrics.text

def browserInstance(artist, song):
    delay = 5

    os.environ['MOZ_HEADLESS'] = '1'

    browser = webdriver.Firefox()

    browser.get('https://genius.com/')

    try:
        best_match = browser.find_element_by_css_selector('div.column_layout-column_span:nth-child(1) > div:nth-child(1) > search-result-section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > search-result-items:nth-child(1) > div:nth-child(1) > search-result-item:nth-child(1) > div:nth-child(1) > mini-song-card:nth-child(1) > a:nth-child(1) > div:nth-child(2)')
        best_match.click()
        print(browser.current_url)

        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'fb-root')))

            url = browser.current_url

            lyrics = getLyrics(url)

            browser.close()

            return lyrics

        except Exception:
            browser.close()

    except Exception:
        browser.close()

def browserInstance_faster(artist, song):
    #Faster scrapping by going straight to links than clicking on buttons
    delay = 5

    os.environ['MOZ_HEADLESS'] = '1'

    browser = webdriver.Firefox()

    browser.get('https://genius.com/search?q=' + artist + '%20' + song)

    try:

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.column_layout-column_span:nth-child(1) > div:nth-child(1) > search-result-section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > search-result-items:nth-child(1) > div:nth-child(1) > search-result-item:nth-child(1) > div:nth-child(1) > mini-song-card:nth-child(1) > a:nth-child(1)')))

        best_match = browser.find_element_by_css_selector('div.column_layout-column_span:nth-child(1) > div:nth-child(1) > search-result-section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > search-result-items:nth-child(1) > div:nth-child(1) > search-result-item:nth-child(1) > div:nth-child(1) > mini-song-card:nth-child(1) > a:nth-child(1)').get_attribute('href')

        try:

            lyrics = getLyrics(best_match)

            while lyrics == "Try again" or lyrics is None:
                lyrics = getLyrics(best_match)

            print(lyrics)

            browser.close()

            return lyrics

        except Exception:
            browser.close()

    except Exception:
        print("sada")
        browser.close()