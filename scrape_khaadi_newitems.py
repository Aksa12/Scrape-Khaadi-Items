from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#opening the file
fname = "clothes.csv"
f = open(fname,'w')
headers = "product_name, price, link, color\n"
f.write(headers)

#grab new items info from khaadi
url = "https://pk.khaadi.com/new-in.html"


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options, executable_path='C:/Users/Aksa/Downloads/chromedriver_win32/chromedriver.exe')
driver.get(url)

timeout = 20
try:
    element_present = EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a.action.next span'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

#function to scrape details of items
def getDetails():
    global driver
    global f
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.swatch-attribute.color div.swatch-attribute-options.clearfix div.swatch'))
        WebDriverWait(driver, 20).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # Give the javascript time to render
    page_soup = BeautifulSoup(driver.page_source,"html.parser")
    items = page_soup.select('li.item.product.product-item-info.product-item')
    for item in items:
        link = item.select('div.product-top a.product.photo.product-item-photo')[0]['href']
        detail = item.select('div.product.details.product-item-details')[0]
        name = detail.select('h5.product.name.product-item-name a.product-item-link')[0].contents[0].strip()
        price = detail.select('div.price-box.price-final_price span.price')[0].contents[0].strip()
        colors = [c['option-label'] for c in detail.select('div.swatch-attribute.color div.swatch-attribute-options.clearfix div.swatch-option.color')]
        price = price.replace('PKR ','')
        price = price.replace(',','')
        print(link, name, price, colors)
        f.write(f"{name}, {price}, {link}")
        for color in colors:
            f.write(f", {color}")
        f.write("\n")

while 1:
    getDetails()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if driver.find_elements_by_css_selector('a.action.next'):
        next = driver.find_elements_by_css_selector('a.action.next')[1]
        next.click()
    else:
        break

#closing files and browser
f.close()
driver.quit()
