import json
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import lru_cache
from selenium.common.exceptions import NoSuchElementException

# Decorando a função scrape_site com lru_cache para armazenamento em cache
@lru_cache(maxsize=None)
def scrape_site(url, name):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")

    service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    
    produtos = []

    try:
        if 'gsuplementos.com.br' in url:
            wait = WebDriverWait(driver, 8)
            div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.row.small-up-1.medium-up-2.large-up-3.categoria-vitrine')))
            product_elements = div_element.find_elements(By.CSS_SELECTOR, '.flex-container.flex-dir-column.vitrine-prod.flex-child-auto.produto-categoria-link')
            for product_element in product_elements:
                product_name = product_element.find_element(By.CSS_SELECTOR, 'h3').text
                if name.lower() in product_name.lower():
                    product_price = product_element.find_element(By.CSS_SELECTOR, 'span.vitrine-valor').text
                    product_avaliacoes = product_element.find_element(By.CSS_SELECTOR, 'span.ts-shelf-right.ts-shelf-rate-count.ts-shelf-rate-enabled').text
                    product_link = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    product_details = {
                        'Produto': product_name,
                        'Preço': product_price,
                        'Avaliações': product_avaliacoes,
                        'Link': product_link
                    }
                    produtos.append(product_details)
            
        elif 'integralmedica.com.br' in url:
            wait = WebDriverWait(driver, 8)
            div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#gallery-layout-container')))

            divs_pai = div_element.find_elements(By.XPATH, "./div")
            for product_element in divs_pai:
                product_name = product_element.find_element(By.CSS_SELECTOR, 'span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body').text
                if name.lower() in product_name.lower():
                    product_price = product_element.find_element(By.CSS_SELECTOR, 'span.vtex-product-price-1-x-sellingPriceValue.vtex-product-price-1-x-sellingPriceValue--shelfDefault').text
                    product_avaliacoes = product_element.find_element(By.CSS_SELECTOR, 'span.ts-shelf-right.ts-shelf-rate-count.ts-shelf-rate-enabled').text
                    product_link = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    product_details = {
                        'Produto': 'Integral Medica ' + product_name,
                        'Preço': product_price,
                        'Avaliações': product_avaliacoes,
                        'Link': product_link
                    }
                    produtos.append(product_details)
      
        elif 'www.maxtitanium.com.br' in url:
            wait = WebDriverWait(driver, 8)
            element_impulse_search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'impulse-search')))
        
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', element_impulse_search)

            elemento_products = shadow_root.find_elements(By.CSS_SELECTOR, '#products div.impulse-product-card')

            count = 0
            for product_element in elemento_products:
                if count == 5:
                    break
                    
                product_name = product_element.find_element(By.CSS_SELECTOR, 'h1.impulse-title').text
                product_price = product_element.find_element(By.CSS_SELECTOR, '.price-container').text
                product_link = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    
                product_details = {
                    'Produto': 'Max Titanium ' + product_name,
                    'Preço': product_price,
                    'Avaliações': 'não existem avaliações.',
                    'Link': product_link
                }
                produtos.append(product_details)
                count += 1
        elif 'www.darkness.com.br' in url:
            wait = WebDriverWait(driver, 8)
            element_search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.prateleira.vitrine.n4colunas')))
        
            elemento_products = element_search.find_elements(By.CSS_SELECTOR, '.prateleira.vitrine.n4colunas > ul.slick-initialized.slick-that-disabled > li')

            for product_element in elemento_products:

                # Encontre o nome do produto dentro do produto atual
                product_name = product_element.find_element(By.CSS_SELECTOR, 'h3.product-name').text
                
                # Encontre o preço do produto dentro do produto atual
                product_price = product_element.find_element(By.CSS_SELECTOR, 'span.best-price').text
                
                # Encontre o preço do produto dentro do produto atual
                # product_reviews = product_element.find_element(By.CSS_SELECTOR, 'span.ts-shelf-right.ts-shelf-rate-count.ts-shelf-rate-enabled').text

                
                # Encontre o link do produto dentro do produto atual
                product_link = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                # Adicione os detalhes do produto à lista de produtos
                product_details = {
                    'Produto': 'Darkness ' + product_name,
                    'Preço': product_price,
                    'Avaliações': 'sem avaliacao',
                    'Link': product_link
                }
                produtos.append(product_details)
                count += 1

    except Exception as e:
        print(f"Erro ao raspar {url}: {e}")

    finally:
        driver.quit()

    return produtos

def scraper(name):
    urls = [
        f'https://www.gsuplementos.com.br/busca/?busca={name}',
        f'https://www.integralmedica.com.br/creatina?_q={name}&map=ft',
        f'https://www.maxtitanium.com.br/busca?q={name}',
        f'https://www.darkness.com.br/#&search-term={name}',
    ]

    produtos = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_site, url, name) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            produtos.extend(future.result())

    return produtos
