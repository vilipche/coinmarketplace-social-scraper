import requests

import pandas as pd

from time import sleep

from bs4 import BeautifulSoup

import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


import chromedriver_autoinstaller

chromedriver_autoinstaller.install()



def get_n_crypto_currency_by_market_cap(n, begin_from = 1):
    headers = {
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://coinmarketcap.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }

    params = (
        ('start', str(begin_from)),
        ('limit', str(n)),
        ('sortBy', 'market_cap')
    )

    response = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing', headers=headers, params=params)
    return response


def get_crypto_currency_social(slug):
    
    url = "https://coinmarketcap.com/currencies/"+slug+"/social/"

    #Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")

    #Run chrome
    browser = webdriver.Chrome(options=chrome_options)
    
    # options = Options()
    # options.headless = True
    
    # browser = webdriver.Chrome('./chromedriver',options=options)
    browser.get(url) 

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    
#     # This should be executed when the browser is on
#     # It doesn't work when we close the browser
#     # No, coin's coinmaketcap url, coin name, twitter id

    market_cap = soup.find('div', {'class': 'statsValue___2iaoZ'}).text.split('$')[-1]
    coin_name  = soup.find('small', {'class': 'nameSymbol___1arQV'}).text
    coin_rank  = soup.find('div', {'class': 'namePillPrimary___2-GWA'}).text.split('#')[-1]
    
    twitter_username = ""
    
    try:
        browser.execute_script("window.scrollTo(0, 500);")
        sleep(1)
        element = WebDriverWait(browser, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "twitter-widget-0"))
        )
        
        twitter_username = browser.find_element_by_class_name("customisable-highlight").text
        sleep(1)
    except:
        pass
    finally:
        browser.quit()


    
    if(args.quiet):
        print(coin_rank, coin_name, slug, market_cap, twitter_username)


    return {
        "coin_rank": coin_rank,
        "market_cap": market_cap,
        "coin_name": coin_name,
        "twitter_username": twitter_username
    }



def scrape(n, begin):
    response = get_n_crypto_currency_by_market_cap(n, begin)
    master_list = []
    for coin in response.json()['data']['cryptoCurrencyList']:
        slug = coin['slug']
        data = get_crypto_currency_social(slug)
        data['slug'] = slug
        master_list.append(data)

    return master_list

def save_csv(master_list):
    df = pd.DataFrame(master_list)
    df.to_csv("crypto-social.csv", index=False)
    if(args.quiet):
        print("Saved to", args.filename)

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is a negative integer, please provide values >= 1" % value)
    return ivalue



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Scrape and store data")

    parser.add_argument("n",   
                        help="display a square of a given number",
                        type=check_positive
    )

    parser.add_argument("begin_from", 
                        nargs='?', 
                        default=1,
                        type=check_positive, 
                        help="Select from which position to begin"
    )
    
    parser.add_argument(
        "-f", "--filename",
        type=str,
        help="Name the file of the .csv",
        default="crypto-social.csv"
    )

    parser.add_argument(
        "-q", "--quiet", 
        action="store_false"
    )

    args = parser.parse_args()

    master_list = scrape(args.n, args.begin_from)
    save_csv(master_list)
























