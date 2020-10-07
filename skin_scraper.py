import time
import json,requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_csgoempire():
    driver = webdriver.Firefox()
    driver.get("https://csgoempire.com/withdraw#730")
    driver.set_window_size(942, 695)
    
    # js to remove chat element to save resources
    js_string = """const elements = document.getElementsByClassName("chat h-full z-30 chat--open");
    while (elements.length > 0) elements[0].remove();
    """
    driver.execute_script(js_string)
    
    element = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".mr-4 > .toggle")))
    element.click()
    try:
        WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.item:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)")))
    except:
        print("Nothing listed right now")
    get_csgoempire_withdraw_items(driver)

def get_csgoempire_withdraw_items(driver):
    wear = driver.find_elements(By.XPATH, "//div[@class='item__head flex items-end']")
    name = driver.find_elements(By.XPATH, "//div[@class='px-2']")
    price = driver.find_elements(By.XPATH, "//span[@class='text-xxs font-bold text-light-grey-1']")
    #get_steam(weapon,name,wear)
    for i in range(0,len(name)):
        print(wear[i].text,end=" ")
        print(name[i].text,end=" ")
        print(price[i].text)

def get_steam_weapon(weapon,name,wear):
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+weapon+"%20%7C%20"+name+"%20%28"+wear+"%29&currency=1"
    data=requests.get(json_link).json()
    return (data)

def get_steam_knife(weapon,name,wear):
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+weapon+"%20%7C%20"+name+"%20%28"+wear+"%29&currency=1"
    data=requests.get(json_link).json()
    return (data)

def get_steam_pin(name):
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+name+"&currency=1"
    data=requests.get(json_link).json()
    return (data)

def get_steam_sticker(name,tour,qual):
    if qual!="":
        qual="%20%28"+qual+"%29%20"
    if tour!="":
        tour="%7C"+tour
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=Sticker%20%7C%20"+name+qual+tour+"&currency=1"
    json_link=json_link.replace(" ","%20")
    print(json_link)
    data=requests.get(json_link).json()
    return data

def get_steam(name,wear):
    if "Pin" in name:
        return get_steam_pin()
    
    elif "Sticker" in name:
        name=name.lstrip("'Sticker\n'")
        if "-" in name:
            arr=name.split("-")
            return get_steam_sticker(arr[0],arr[1],wear)
        else:
            return get_steam_sticker(name,'',wear)
    
    #elif 

print(get_steam('Sticker\nHowling Dawn',''))

#get_csgoempire()