from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Edge()
driver.get('https://amazon.in')
time.sleep(2)
driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('iphone')
time.sleep(2)
driver.find_element(By.ID, 'nav-search-submit-button').click()
time.sleep(3)

all_titles = []
all_prices = []

for page in range(4):  # Scrape 4 pages
    titles = driver.find_elements(By.CSS_SELECTOR, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
    prices = driver.find_elements(By.CLASS_NAME, "a-price-whole")
    # Extract and clean text
    all_titles.extend([title.text.split(':')[0] + ':' if title in titles else '' for title in titles])
    all_prices.extend([price.text if price in prices else '' for price in prices])
    print(f"Scraped page {page+1}")

    if page < 3:
        try:
            next_btn = driver.find_element(By.LINK_TEXT,"Next").click()
            time.sleep(3)
        except Exception as e:
            print("Could not find Next button or error occurred:", e)
            break

driver.quit()

# Save to CSV
df = pd.DataFrame({'Title': all_titles, 'Price': all_prices})
df.to_csv('amazon_iphone.csv', index=False)
print("Saved to amazon_iphone.csv")
