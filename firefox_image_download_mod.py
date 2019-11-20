
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import os
import json
from urllib.request import *
import sys
import time


def main(folder,num_request, url):
    
    driver = webdriver.Firefox(executable_path=r"C:/Users/syahr/OneDrive/Documents/coding/Data_collecting/from_google/geckodriver.exe")
    driver.get(url)

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    extensions = {"jpg", "jpeg", "png"}
    img_count = 0
    downloaded_img_count = 0
    
    for _ in range(100):
        for __ in range(100):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(0.2)
        # to load next 400 images
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//input[@value='visa fler resultat']").click()
        except Exception as e:
            print ("Less images found: {}".format(e))
            break

    # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
    imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    print(imges)
    print ("Total images: {}\n".format(len(imges)))
    for img in imges:
        img_count += 1
        img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
        img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
        print ("Downloading image {}:{}".format(img_count,img_url))
        try:
            if img_type not in extensions:
                img_type = "jpg"
            req = Request(img_url, headers=headers)
            raw_img = urlopen(req).read()
            f = open(folder+"/"+str(downloaded_img_count)+"."+img_type, "wb")
            f.write(raw_img)
            f.close
            downloaded_img_count += 1
        except Exception as e:
            print ("failed: {}".format(e))
        finally:
            print
        if downloaded_img_count >= num_requested:
            break

    print ("Total downloaded: {}/{}".format(downloaded_img_count,img_count))
    driver.quit()

if __name__ == "__main__":
    folder = "C:/Users/syahr/OneDrive/Documents/coding/Data_collecting/from_google/downloads/blog/"
    url = "https://www.google.co.id/search?q=najwa+shihab&sxsrf=ACYBGNSifErPUinWYKVCj9GR_IY5niXamQ:1573948665807&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic0frY9-_lAhWixIsKHSRGCwQQ_AUIEigB&biw=1280&bih=567"

    num_requested = 20 
    main(folder,num_requested,url)