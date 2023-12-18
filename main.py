import os
import requests
import cv2
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By


def bypass_yandex_images_captcha():
    """this func checks website for special error page and tries to find capcha pass button in html code, after that clicks on it and waits for page to update. if it didnt work pulls 
    out an error message.
    """
    try:
        captcha_button = browser.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button")
        captcha_button.click()
        browser.implicitly_wait(10000)
    except:
        print("Unknown error occurred\n")
        return

def download_image_by_url(image_url):
    """this func dowloads image from url by turnning it onto byte array and after that decoding it

    Args:
        image_url 

    Returns:
        img decoded with cv2  
    """
    req = requests.get(image_url)
    arr = np.asarray(bytearray(req.content), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img

base_url = "https://yandex.ru/images/"
url1 = "https://yandex.ru/images/search?text=*tiger"
url2 = "https://yandex.ru/images/search?text=*leopard"
fo = webdriver.FirefoxOptions()
fp = webdriver.FirefoxProfile()

try:
    os.mkdir("dataset")
    os.mkdir("dataset\\tiger")
    os.mkdir("dataset\\leopard")
except FileExistsError:
    print("Folder already exists")

browser = webdriver.Firefox()
browser.maximize_window()

for url in url1, url2:
    print(f"Image output from url: {url}\n")
    browser.get(url)
    browser.implicitly_wait(20000)

    if browser.title == "Ой!":
        bypass_yandex_images_captcha()

    image_divs = browser.find_elements(By.CLASS_NAME, "SimpleImage") #clicks button show more to scroll the page further
    while len(image_divs) < 1200:
        load_button_div = browser.find_element(By.CLASS_NAME, "SerpList-LoadContent")
        load_button = load_button_div.find_element(By.TAG_NAME, "button")
        load_button.click()
        image_divs = browser.find_elements(By.CLASS_NAME, "SimpleImage")    

    image_num = 0 #downloads images and prints urls of images
    for image_div in image_divs:
        image_link = image_div.find_element(By.TAG_NAME, "img").get_property("src")
        print(image_link, end="\n")
        image = download_image_by_url(image_link)
        image_name = str(image_num)
        while len(image_name) < 4:
            image_name = "0" + image_name
        image_num += 1
        if url == url1:
            cv2.imwrite(f"dataset\\tiger\{image_name}.jpg", image)
        else:
            cv2.imwrite(f"dataset\\leopard\{image_name}.jpg", image)
browser.close()
