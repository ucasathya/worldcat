import csv
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)
items = ["The 5 AM club","Eat That Frog","Anna Karenina","The Great Gatsby","A Passage to India","Invisible Man","Things Fall Apart"]

rows=[]
for item in items:
    worldcat_url =f"https://www.worldcat.org/search?qt=worldcat_org_bks&q={item}"
    driver = webdriver.Firefox(executable_path="C:\\Users\\Asus\\Desktop\\geckodriver.exe")
    driver.maximize_window()
    print(f"Searching for {item}.")
    driver1 = driver.get(worldcat_url)
    heading=driver.find_element_by_id('result-1').text
    print(heading)
    try:
        search_button = driver.find_element_by_link_text(item)
        time.sleep(5)
        search_button.click()
        print("try")
    except:
        search_button = driver.find_element_by_link_text(heading)
        time.sleep(5)
        search_button.click()
        print("Except")            
    chwd = driver.window_handles            
    for w in chwd:
        driver.switch_to.window(w)
    time.sleep(5)
    url=driver.current_url
    headers= ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})
    page=requests.get(url=url,headers=headers)
    soup = BeautifulSoup(page.content,'lxml')
    row=[]
    try:
        c = soup.find("div",id="bibdata").text
        l=(c.split("\n"))
        k=[]
        for i in l:
            if i != "":
                k.append(i)
        row.append(k[0])
        #k.pop(0)
        print(k)
        heading=["Author:","Publisher:","Edition/Format:","Rating:"]
        field=[]
        h=0
        m=len(k)-1
        n="NA"
        for i in heading:
            c=0
            for j in k:
                if k[c]==heading[h]:
                    field.append(j)
                    row.append(strip_non_ascii(k[c+1]))
                    break
                elif m==c:
                    row.append(n)                       
                c+=1
            h+=1

        rows.append(row)
    except:
        print("Attribute Error")
    driver.quit()
heading.insert(0,'Book Name')
print(heading)
print(rows)
with open('GFG.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(heading) 
    write.writerows(rows)
print("success")
    

    
