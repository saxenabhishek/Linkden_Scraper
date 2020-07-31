import pickle
import time
import re
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def Firstlogin(driver, user, password):
    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_name("session_key").send_keys(user)
    driver.find_element_by_name("session_password").send_keys(password)
    driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']").click()
    time.sleep(5)

def cookieloader(web, cookiepath):
    if Path(cookiepath + "cookies.pkl").exists() == False:
        Firstlogin(web,"as7122000@gmail.com","XXXXXXX")
        pickle.dump( web.get_cookies() , open(cookiepath + "cookies.pkl","wb")) 
    else:
        web.get("https://www.linkedin.com")
        cookies = pickle.load(open(cookiepath + "cookies.pkl", "rb"))
        for cookie in cookies:
            web.add_cookie(cookie)
    
def collectlinks(web,q,depth):
    links = []
    
    web.get("https://www.linkedin.com/search/results/people/?keywords=" + q)

    time.sleep(1)

    html = web.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    
    time.sleep(1)

    libutspan = [i.text for i in web.find_elements_by_css_selector("li button span")]
    pageno = list(filter(lambda x:re.findall("\d+",x),libutspan))[-1]

    if int(pageno) < depth:
        depth = pageno

    for i in range(depth):
        time.sleep(2)
        html = web.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(5)
        li = web.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
        links += [i.get_attribute("href") for i in li][::2]
        nxt = web.find_elements_by_xpath("//span[@class='artdeco-button__text']")
        nxt[-2].click()

    return links

def collectinfo(web,links):
    info={
        'name':[],
        'pos':[],
        'adr':[],
        'links':[],
        'span':[],
        'head':[]   
    }

    for i in links:
        
        web.get(i)
        A = web.find_elements_by_css_selector("li[class = 'inline t-24 t-black t-normal break-words']")
        B = web.find_elements_by_css_selector("h2[class='mt1 t-18 t-black t-normal break-words']")
        C = web.find_elements_by_css_selector("li[class='t-16 t-black t-normal inline-block']")
        web.find_element_by_css_selector("span[class='t-16 t-bold']").click()
        time.sleep(2)
        D = [i.get_attribute("href") for i in web.find_elements_by_css_selector("div[class='pv-profile-section__section-info section-info'] a:link")]
        E = [i.text for i in web.find_elements_by_css_selector("div[class='pv-profile-section__section-info section-info'] span")]
        F = [i.text for i in web.find_elements_by_css_selector("div[class='pv-profile-section__section-info section-info'] header")]

        def lam(a):
            if len(a) == 0:
                return ""
            else:
                return a[0].text
    
        A, B, C = map(lam,(A,B,C))

        info["name"].append(A)
        info["pos"].append(B)
        info["adr"].append(C)
        info["links"].append(D)
        info["span"].append(E)
        info["head"].append(F)

    return info

def main():
    path = "/home/kaafibored/Projects/Linkden_Scraper/"

    web = webdriver.Chrome(path+"chromedriver")
    web.maximize_window()

    cookieloader(web, path)

    links = collectlinks(web,"CSR",1)
    
    finaldf = pd.DataFrame(final)

    finaldf.to_csv(path + "Links.csv",index=False)

    #final = collectinfo(web,links)

    #finaldf = pd.DataFrame(final)

    #finaldf.to_csv(path + "data.csv",)

    web.close()

if __name__ == "__main__":
    main()
