from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Options for selenium
options = Options()
options.page_load_strategy = 'eager'  # Faster load so it does not wait for video ads to render
options.add_argument("--headless")  # Run Chrome in headless mode


def get_webpage_html(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html
