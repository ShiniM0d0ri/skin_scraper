import time,os,re
import steam
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
        time.sleep(1)
    return driver

def get_csgoempire_withdraw_items(driver):
    wear = driver.find_elements(By.XPATH, "//div[@class='item__head flex items-end']")
    name = driver.find_elements(By.XPATH, "//div[@class='px-2']")
    price = driver.find_elements(By.XPATH, "//span[@class='text-xxs font-bold text-light-grey-1']")
    print("Currently listed ",len(wear)," items")
    for i in range(0,len(name)):
        try:
            wear1=wear[i].text.title()
        except StaleElementReferenceException:
            print("stale element")
            continue
        em_coins=float(price[i].text.strip(','))
        try:
            fv=float(re.findall('~0\.\d+',wear1)[0].strip('~'))
        except IndexError:
            fv=0
        if (fv!=0 and gud_float(fv)):
            print(name[i].text.replace("\n"," ")," | good float: ", fv," for ",em_coins)
        try:
            steam_json=steam.get_steam(name[i].text,wear1)
            if(steam_json['success']=='false'):
                print("rate blocked by steam")
                r=time.sleep(2)
                continue
            steam_price=float(steam_json['lowest_price'].strip('$'))
        except (TypeError,KeyError):
            print("json error")
            continue        
        if(profit(em_coins,steam_price)):
            print("Buy now!!!!!",name[i].text.replace("\n"," "),"at",steam_price-em_coins)
    return driver



def gud_float(fv):
    if 0.20>fv>0.15 or 0.07<fv<0.11 or fv<0.05:
        return True

def profit(em,steam):
    if ((em-steam)/em)<=0.04:
        #os.system("powershell -c echo `a")
        return True


#print(get_steam('Sticker\nHowling Dawn',''))


def main():
    driver=setup_driver()
    try:
        driver=get_csgoempire(driver)
        while(True):
            os.system("cls")
            driver=get_csgoempire_withdraw_items(driver)
            print("refreshing...")
            time.sleep(5)
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
