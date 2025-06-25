from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import urllib.request
# This script uses Selenium to scrape image URLs from a specific webpage.
# to run Chrome in headless mode
options = Options()
options.add_argument("--headless")

# initialize a Chrome WerbDriver instance
# with the specified options
driver = webdriver.Chrome(
    service=ChromeService(),
    options=options
)

# to avoid issues with responsive content
driver.maximize_window()

# the URL of the target page
url = "https://mabrouk.tn/categorie-produit/nouvelle-collection/page/4/"
# visit the target page in the controlled browser
driver.get(url)
driver.implicitly_wait(10)  # wait for elements to load
# find all image elements on the page
images = driver.find_elements("css selector", "img")
# extract the URLs of the images
image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]
# print the extracted image URLs
for i, img_url in enumerate(image_urls, start=1):
    print(f"Image {i+197}: {img_url}")
    #download the image or process it as needed
    file_name = f"image_{i+197}.jpg"
    urllib.request.urlretrieve(img_url, file_name)
    
# close the browser and free up its resources
driver.quit()