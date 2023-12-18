from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def bypass_yandex_images_captcha():
    try:
        captcha_button = browser.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button")
        captcha_button.click()
        browser.implicitly_wait(10000)
    except:
        print("Unknown error occurred\n")
        return


base_url = "https://yandex.ru/images/"
url1 = "https://yandex.ru/images/search?text=*tiger"
url2 = "https://yandex.ru/images/search?text=*leopard"
fo = webdriver.FirefoxOptions()
fp = webdriver.FirefoxProfile()

browser = webdriver.Firefox()
browser.maximize_window()

for url in url1, url2:
    print(f"Вывод изображений по ссылке: {url}\n")
    browser.get(url)
    browser.implicitly_wait(20000)
    if browser.title == "Ой!":
        bypass_yandex_images_captcha()
    image_divs = browser.find_elements(By.CLASS_NAME, "SimpleImage")
    for image_div in image_divs:
        image_link = image_div.find_element(By.TAG_NAME, "img").get_property("src")
        print(image_link, end="\n")

# image = cv2.imread(path_to_file)   прочтение изображения из файла, path_to_file - путь до файла-изображения
# cv2.imwrite(path_to_save_image, image)   сохранение изображения по заданному пути, например, path_to_folder/image_name.jpg

# print(image.shape)  # распечатать размер прочитанного изображения

# инструкции для просмотра изображения
# cv2.imshow(window_name, image)
# cv2.waitKey(0)
