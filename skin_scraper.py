import time,os
import json,requests,re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def setup_driver():
    profile = webdriver.FirefoxProfile()
    # 1 - Allow all images
    # 2 - Block all images
    # 3 - Block 3rd party images 
    profile.set_preference("permissions.default.image", 2)
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    driver.get("https://csgoempire.com/withdraw#730")
    driver.set_window_size(942, 695)
    return driver

def get_csgoempire(driver):
    driver=driver

    # js to remove chat element to save resources
    js_string = """const elements = document.getElementsByClassName("chat h-full z-30 chat--open");
    while (elements.length > 0) elements[0].remove();
    """
    driver.execute_script(js_string)
    
    element = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".mr-4 > .toggle")))
    element.click()
    try:
        WebDriverWait(driver, 50).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.item:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)")))
    except:
        print("Nothing listed right now")
    get_csgoempire_withdraw_items(driver)
    return driver

def get_csgoempire_withdraw_items(driver):
    wear = driver.find_elements(By.XPATH, "//div[@class='item__head flex items-end']")
    name = driver.find_elements(By.XPATH, "//div[@class='px-2']")
    price = driver.find_elements(By.XPATH, "//span[@class='text-xxs font-bold text-light-grey-1']")
    print(len(name))
    for i in range(0,len(name)):
        try:
            wear1=wear[i].text.title()
        except StaleElementReferenceException:
            continue
        try:
            steam_price=float(get_steam(name[i].text,wear1)['lowest_price'].strip('$'))
        except (KeyError,TypeError,IndexError):
            continue        
        em_coins=float(price[i].text)
        if(profit(em_coins,steam_price)):
            print("Buy now!!!!!",name[i].text.replace("\n"," "))
        try:
            fv=float(re.findall('~0\.\d+',wear1)[0].strip('~'))
        except IndexError:
            fv=0
        if (fv!=0 and gud_float(fv)):
            print(name[i].text.replace("\n"," "),"This float is good: ", fv)


def get_steam_weapon(weapon,name,wear):
    #print(weapon,name,wear)
    json_link="https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+weapon+"%20%7C%20"+name+"%20%28"+wear+"%29&currency=1"
    json_link=json_link.replace(" ","%20")
    #print(json_link)
    data=requests.get(json_link).json()
    return data

def get_steam_knife(weapon,name,wear):
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+weapon+"%20%7C%20"+name+"%20%28"+wear+"%29&currency=1"
    json_link=json_link.replace(" ","%20")
    data=requests.get(json_link).json()
    return data

def get_steam_pin(name):
    #print(name)
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+name+"&currency=1"
    json_link=json_link.replace(" ","%20")
    data=requests.get(json_link).json()
    return data

def get_steam_sticker(name,tour,qual):
    if qual!="":
        qual="%20%28"+qual+"%29%20"
    if tour!="":
        tour="%7C"+tour
    #print(name,qual,tour)
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=Sticker%20%7C%20"+name+qual+tour+"&currency=1"
    json_link=json_link.replace(" ","%20")
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
    
    # elif "Knife" in name:
    #     return get_steam_knife(name)
    
    else:
        arr=name.split("\n")
        if "|" in wear:
            arr2=wear.split(" | ")
            wear_float=arr2[1]
            return get_steam_weapon(arr[0],arr[1],arr2[0])
        else:
            return get_steam_weapon(arr[0],arr[1],wear)
    time.sleep(0.5)

def gud_float(fv):
    if 0.20>fv>0.15 or 0.07<fv<0.11 or fv<0.05:
        return True

def profit(em,steam):
    if ((em-steam)/em)<=0.04:
        os.system("powershell -c echo `a")
        return True


#print(get_steam('Sticker\nHowling Dawn',''))


def main():
    driver=setup_driver()
    run_time="1"
    run_time_cond=input("If you want to run the script continuously type 'yes'and press enter: ")
    if(run_time_cond=="yes"):
        run_time="0"
    try:
        while(True):
            os.system("cls")
            driver=get_csgoempire(driver)
            print("refreshing...")
            time.sleep(3)
            print("run_time: ",run_time)
            if(run_time=="1"):
                break
            driver.refresh()
    except KeyboardInterrupt:
        print("Closing the script\nMight take some time so..\nDON'T PRESS IT AGAIN")
        driver.quit()
        print("closing remaining firefox process")
        os.system("pause")
        os.system("""taskkill /f /im "firefox.exe" /t""")
        exit(0)

    driver.quit()
    os.system("""taskkill /f /im "firefox.exe" /t""")

    

main()
