import csv

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, ui
from time import sleep

page_max = 1


def get_value(driver, string):
    try:
        return driver.find_element_by_css_selector(string).text
    except:
        return ""


driver = webdriver.Firefox()

def is_visible(locator, timeout = 10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        return True
    except TimeoutException:
        return False


for i in range(1, page_max+1):
    url = "https://www.amazon.com/s?i=grocery&bbn=16310101&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114320011&dc&page=" + str(i)
    driver.get(url)
    sleep(2)
    products = driver.find_elements_by_css_selector(".s-include-content-margin")
    # print(len(driver.find_elements_by_css_selector(".s-include-content-margin")))
    for product in products:
        elem = driver.find_elements_by_css_selector("h2 a")
        links = []
        for e in elem:
            links.append(e.get_attribute("href"))
        for link in links[:1]:
            # print(link)
            driver.get(link)
            try:
                wait = is_visible('#productTitle', timeout=10)
            except:
                print("Timeout... #productTitle")

            action = ActionChains(driver)
            elems = driver.find_elements_by_css_selector('#altImages ul li.item')
            # Should not move cursor
            for elem in elems:
                sleep(1)
                action.move_to_element(elem).perform()
            # feel free to move  cursor
            name = get_value(driver, "#productTitle")
            description = get_value(driver, "#feature-bullets")
            images = driver.find_elements_by_css_selector(".a-text-center.a-fixed-left-grid-col.a-col-right #main-image-container ul.a-unordered-list.a-nostyle.a-horizontal.list.maintain-height li.image img")
            print("div container: ", images[0].get_attribute("innerHTML"))
            im = []

            for image in images:
                im.append(image.get_attribute("src"))
                print(im)

            #data = [name, link, description, sku, ingredients, nutrifacts, directions, "-".join(im)]
            #writer.writerow(data)
    driver.close()