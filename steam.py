import requests,json,time

def get_steam_weapon(weapon,name,wear):
    #print(weapon,name,wear)
    json_link="http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name="+weapon+"%20%7C%20"+name+"%20%28"+wear+"%29&currency=1"
    json_link=json_link.replace(" ","%20")
    #proxies={'http':'http://117.239.240.202:53281' , 'http':'http://165.22.213.55:3128'}
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
    json_link="https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=Sticker%20%7C%20"+name+qual+tour+"&currency=1"
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
