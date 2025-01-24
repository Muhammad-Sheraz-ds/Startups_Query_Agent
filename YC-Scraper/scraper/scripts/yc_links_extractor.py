import json
import re
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


def make_driver():
    """Creates headless Chrome WebDriver instance using webdriver-manager."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resources in containers
    service = Service(ChromeDriverManager().install())  # Use Service to handle ChromeDriver path
    return Chrome(service=service, options=chrome_options)


driver = make_driver()
page = "https://www.ycombinator.com/companies"


def get_page_source():
    """Returns the source of the current page."""
    driver.get(page)


def click_see_all_options():
    """Clicks 'See all options' button to load checkboxes for all batches."""
    sleep(3)
    see_all_options = driver.find_element(By.LINK_TEXT, 'See all options')
    see_all_options.click()


def compile_batches():
    """Returns elements of checkboxes from all batches."""
    pattern = re.compile(r'^(W|S|IK)[012]')
    bx = driver.find_elements(By.XPATH, '//label')
    for element in bx:
        if pattern.match(element.text):
            yield element


def scroll_to_bottom():
    """Scrolls to the bottom of the page."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def fetch_url_paths():
    """Returns a generator with url paths for all companies."""
    elements = driver.find_elements(
        By.XPATH, ('//a[contains(@href,"/companies/") and not(contains(@href,"founders"))]'))
    for url in elements:
        yield url.get_attribute('href')


def write_urls_to_file(ul: list):
    """Writes a list of company URLs to a properly formatted text file."""
    txt_file = './YC-Scraper/scraper/data/start_urls.txt'
    with open(txt_file, mode='w', encoding='utf-8') as f:
        f.writelines([url.rstrip('"') + '\n' for url in ul])  # Write each URL on a new line

def yc_links_extractor():
    """Run the main script to write all start urls to a file."""
    print(f"Attempting to scrape links from {page}.")
    get_page_source()
    click_see_all_options()
    batches = compile_batches()
    ulist = []

    for b in tqdm(list(batches)):
        b.click()
        scroll_to_bottom()
        urls = [u for u in fetch_url_paths()]
        ulist.extend(urls)
        b.click()

    write_urls_to_file(ulist)
    driver.quit()


if __name__ == '__main__':
    yc_links_extractor()
