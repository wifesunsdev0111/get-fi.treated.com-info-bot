from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import requests
import quickstart
import re
from translate import Translator
import get_latitude_and_longitude



# Create a Translator object and translate the string
translator = Translator(to_lang="en")
website_links = ["https://fi.treated.com/raskauden-ehkaisy"]


for link in website_links:



    
    driver = webdriver.Chrome()    
    driver.maximize_window()
    driver.get(link)


    try:
        cookey_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]"))).click()
    except:
        pass

    try:
        main_content = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id=\"addmore_row_filter\"]")))
        driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 0);", main_content)
        main_content_lists = WebDriverWait(main_content, 20).until(EC.presence_of_all_elements_located((By.XPATH, "./*")))
        for main_content in main_content_lists:
            try:
                apply_button = WebDriverWait(main_content, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class=\"ljoptimizer cta-1  consultation-startup-btn elementor-button product-consultation product-card elementor-size-sm w-100\"]")))
                WebDriverWait(main_content, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class=\"elementor-button product_access\"]"))).click()
                break
            except:
                continue

    except:
        pass
    
    # sleep(3)
    # window_handles = driver.window_handles
    # driver.switch_to.window(window_handles[1])
    # sleep(3)
    
    try:
        cookey_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]"))).click()
    except:
        pass

    
    body_content = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id=\"compare-price-id\"]")))

    driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 0);", body_content)

    try:
        cookey_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]"))).click()
    except:
        pass

    product_lists_parent = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"compare-prices slick-initialized slick-slider slick-dotted\"]")))
    product_lists_body = WebDriverWait(product_lists_parent, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"slick-track\"]")))
    product_lists = WebDriverWait(product_lists_body, 20).until(EC.presence_of_all_elements_located((By.XPATH, "./*")))

    print(f'All Products Body = ', len(product_lists))

    for index, product_body in enumerate(product_lists):
        select_tabs_body = WebDriverWait(product_body, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"select-mg-tabs\"]")))
        select_tabs = WebDriverWait(select_tabs_body, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
        print(f'Select Tab Count = ', len(select_tabs))
        
        # product_name_body_parent = WebDriverWait(product_body, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"product-details\"]")))
        product_name_body = WebDriverWait(product_body, 20).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        product_name_main = WebDriverWait(product_name_body, 20).until(EC.presence_of_element_located((By.TAG_NAME, "a"))).text
        product_name_detail =  WebDriverWait(product_name_body, 20).until(EC.presence_of_element_located((By.TAG_NAME, "span"))).text
        product_name = product_name_main + "(" + product_name_detail + ")"
        print(f"Product Name = ", product_name)
        
        
        for index, tab in enumerate(select_tabs):
            sleep(2)
            capacity = tab.text
            print(f'capacity = ', capacity)
            
            try:
                tab.click()
            except:
                pass
            
            id = "viagra-dose-" + str(index + 1)
            tabs_content = WebDriverWait(product_body, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"tabs-content\"]")))
            tabs_content_lists = WebDriverWait(tabs_content, 20).until(EC.presence_of_all_elements_located((By.XPATH, "./*")))


            tbody_content = WebDriverWait(tabs_content_lists[index], 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody[class=\"table-body\"]")))
            tr_content_lists = WebDriverWait(tbody_content, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

            for index, tr_content in enumerate(tr_content_lists):

                amount = WebDriverWait(tr_content, 20).until(EC.presence_of_element_located((By.TAG_NAME, "th"))).text
                price_td = WebDriverWait(tr_content, 20).until(EC.presence_of_element_located((By.TAG_NAME, "td")))

                price = WebDriverWait(price_td, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class=\"price\"]"))).text
                
                try:
                    saving_price_1 = WebDriverWait(price_td, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class=\"save\"]"))).text
                    saving_price = saving_price_1.replace("Säästö", "")
                except:
                    saving_price = ""
                    pass
                
                print(f'price = ', price)
                print(f'saving price = ', saving_price)
            
                sleep(1)    
                quickstart.main()
                columnCount = quickstart.getColumnCount()
            
                
                print(f'columnCount = ',columnCount)


                results = []
                results.append(str(columnCount + 1))
                results.append(product_name)
                results.append(capacity)
                results.append(amount)
                results.append(price)
                results.append(translator.translate(saving_price))

                quickstart.main()
                RANGE_DATA = f'viagra_info!A{columnCount + 2}:F'
                quickstart.insert_data(RANGE_DATA, results)
        
        try:
            WebDriverWait(body_content, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"right-nav slick-arrow\"]"))).click()
        except:
            pass
                                
            
        
    driver.quit()

        
        
    
