from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import math
import psutil
# https://www.reddit.com/r/webscraping/comments/15emy4p/web_scrape/?onetap_auto=true

def get_ram_usage():
    # Get system's virtual memory information
    virtual_memory = psutil.virtual_memory()

    # Calculate RAM usage in percentage
    ram_usage_percent = virtual_memory.percent

    # Calculate RAM usage in MB
    ram_usage_mb = virtual_memory.used / (1024 * 1024)

    return ram_usage_percent, ram_usage_mb


def open_browser(url):
    edge_options = Options()
    #edge_options.use_chromium = True 
    edge_options.add_argument("start-maximized")
    edge_options.add_argument("inprivate")
    edge_options.add_argument('--mute-audio')
    #edge_options.add_argument("--disable-notifications")
    #edge_options.add_argument('--log-level=3')
    edge_options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=edge_options)
    
    driver.get(url)
    return driver 
    
def get_tool_url(driver):
    tools_list = driver.find_elements(By.XPATH, '//div[@class="col-xl-4 col-lg-4 col-md-6 tool_box"]' ) 
    print('tools_list', len(tools_list))
    tools_urls = []
    for tool in tools_list:
        element = tool.find_element(By.XPATH, './/div[@class="mt-3 mb-2 d-flex"]/h5/a[1]' )
        tool_url = element.get_attribute("href") 
        
        try:
            element = tool.find_element(By.XPATH, './/div[@class="mt-3 mb-2 d-flex"]/h5/a[1]')
            tool_url = element.get_attribute("href")
        except StaleElementReferenceException:
            # Element became stale, try finding it again
            try:
                element = tool.find_element(By.XPATH, './/div[@class="mt-3 mb-2 d-flex"]/h5/a[1]')
                tool_url = element.get_attribute("href")
            except NoSuchElementException:
            # Element not found, set tool_name to None
                tool_url = None
        
        #print('tool_url', tool_url)
        tools_urls.append(tool_url)
    
    #print('#### TOOLS URLS ####')
    #print(tools_urls)
    return tools_urls 

def get_data(driver , urls):
    tools_names = []
    tools_urls = []
    what_is_s = []
    pricings = []
    tags = []
    use_cases_s = []
    n = len(urls)
    for i in range(n):
        url = urls[i]
        print("#############")
        print(f'Visiting {url} page...')
        print(f'Url number {i+1}/{n} .')
        print("#############")

        driver.get(url)
        try:
            tool_name = driver.find_element(By.XPATH, '//h1[@class="text-capitalize"]' ).text
        except NoSuchElementException:
            tool_name = None
        try:
            tool_url =  driver.find_element(By.XPATH, '//span[@class="bg-black btn btn-sm"]/a' ).get_attribute("href")
        except NoSuchElementException:
            tool_url = None
        try:
            what_is = driver.find_element(By.XPATH ,'//div[@class="my-5"]/p[@class="p-1 py-2 rounded"]').text
        except NoSuchElementException:
            what_is = None
        try:
            pricing = driver.find_element(By.XPATH ,'//p[@class="mt-3 mb-2"]/span').text
        except NoSuchElementException:
            pricing = None
        try:
            tag = driver.find_element(By.XPATH ,'//p[@class="my-2 "]/span[@class="badge bg-black"]/a').text
        except NoSuchElementException:
            tag=None
        
        try:
            use_cases = driver.find_element(By.XPATH ,'//div[@class="my-4"]/ol').text
        except NoSuchElementException:
            use_cases = None

        tools_names.append(tool_name)
        tools_urls.append(tool_url)
        what_is_s.append(what_is)
        pricings.append(pricing)
        tags.append(tag)
        use_cases_s.append(use_cases)
        time.sleep(5)

    return  tools_names, urls, what_is_s, pricings, tags, use_cases_s
    


def save_data(tools_names, urls, what_is_s, pricings, tags, use_cases_s, output_file_name='output.csv'):
    df = pd.DataFrame( {'tools_names':tools_names,
                         'urls':urls,
                         'what_is': what_is_s,
                         'pricing': pricings,
                         'tags': tags,
                         'use_cases': use_cases_s})
    print('############')
    print(f'we have {len(df.index)} elements.')
    print('############')
    print('Here is the first 5 elements please check if that\'s correct.')
    print('############')

    print(df.head())

    print('############')
    print('Here is the last 5 elements please check if that\'s correct.')
    print('############')

    print(df.tail())

    
    print('############')
    print('Saving...')
    print('############')
    
    df.to_csv(f'{output_file_name}', index=False)


def main(url, output_file_name, elements_number=50):
    driver = open_browser(url)
    time.sleep(5)
    for _ in range( math.ceil(elements_number/18) ):    
        urls = get_tool_url(driver)
        # scroll down
        driver.find_element(By.XPATH,'//body').send_keys(Keys.END)
        time.sleep(10)
    
    print('###############')
    print("urls",urls)
    print("length of urls",len(urls))
    # parse data from every element (aka every url)
    tools_names, urls, what_is_s, pricings, tags, use_cases_s = get_data(driver, urls)
    save_data(tools_names, urls, what_is_s, pricings, tags, use_cases_s, output_file_name)

    driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    url = "https://topai.tools/browse"
    output_file_name = 'ai_tools.csv'
    elements_number = 500
    print('###############')
    print(f'Scraping {elements_number} elements...')
    print('###############')
    main(url, output_file_name, elements_number)    
    print('###############')
    ram_usage_percent, ram_usage_mb = get_ram_usage()
    print(f"RAM usage: {ram_usage_percent:.2f}%")
    print(f"RAM usage: {ram_usage_mb:.2f} MB")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")
    print('###############')
    