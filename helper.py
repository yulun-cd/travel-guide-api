import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# function to convert city name to three-letter code
def city_code_helper(city_name):
    api_key = "e950cfac-1f5d-448f-b9bd-501d16315e10"
    url = f"https://airlabs.co/api/v9/suggest?q={city_name}&api_key={api_key}"
    response = requests.get(url)
    result = response.json()
    if result['response']['cities']:
        return result['response']['cities'][0]['city_code']
    
        
# function to convert country name to iso-3166 country code   
with open('iso3166.csv', mode='r') as f:
    reader = csv.reader(f)
    iso_map = {rows[0]:rows[1] for rows in reader}
        
def country_code_helper(country_name):
    if country_name in iso_map.values():
        return country_name
    else:
        return iso_map.get(country_name, None)
    
    
# function to web scrape flight price from expedia for the given depature, destination and date.
def flight_price_helper(depature, destination, d, m, y):
    depature_code = city_code_helper(depature)
    depature = depature.replace(" ", "+")
    destination_code = city_code_helper(destination)
    destination = destination.replace(" ", "+")
    
    url = f"https://www.expedia.co.uk/Flights-Search?leg1=from%3A{depature}%20%28{depature_code}-All%20Airports%29%2Cto%3A{destination}%20%28{destination_code}-All%20Airports%29%2Cdeparture%3A{d}%2F{m}%2F{y}TANYT&mode=search&options=carrier%3A%2A%2Ccabinclass%3A%2Cmaxhops%3A1%2Cnopenalty%3AN&pageId=0&passengers=adults%3A1%2Cchildren%3A0%2Cinfantinlap%3AN&trip=oneway"
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("detach", True)
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(chrome_options=options, executable_path=r"D:\Program\chromedriver.exe")
        driver.get(url)
        time.sleep(10)
        page = driver.page_source
        
        driver.quit()
        
        soup = BeautifulSoup(page, 'html.parser')
        tag = soup.find("li", {"data-test-id": "offer-listing"})
        target = tag.find(text=re.compile("£\d*")).text
        price = int(re.findall("£\d*", target)[0][1:])
        return price
        
    except WebDriverException:
        print("Please update the chrome driver!")