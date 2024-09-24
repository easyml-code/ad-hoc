from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# Configure the WebDriver (e.g., using Firefox)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)

def download_pdf(pdf_url, save_path):
    download_folder='/'.join(save_path.split('/')[:-1])
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
#         print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download {pdf_url}. Status code: {response.status_code}")
        
def extract_directory_links(base_url):
    browser.get(base_url)
    
    # Wait for the elements with the specific class to be present
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.w-full.flex.gap-4.transition-all.duration-300.bg-dark-800.hover\\:bg-dark-300.hover\\:duration-0.rounded-xl.p-2.items-center'))
        )
        
        # Locate all elements with the specified class
        links = browser.find_elements(By.CSS_SELECTOR, 'a.w-full.flex.gap-4.transition-all.duration-300.bg-dark-800.hover\\:bg-dark-300.hover\\:duration-0.rounded-xl.p-2.items-center')
        hrefs = []
        
        for link in links:
            href = link.get_attribute('href')
            if href:
                hrefs.append(href)
        return hrefs

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    base_url = 'https://dl.ibdocs.re/IB%20PAST%20PAPERS%20-%20SUBJECT/Group%204%20-%20Sciences/'
    directory_links = extract_directory_links(base_url)

    directory_links2=[]
    for link in directory_links:
        temp_link = extract_directory_links(link)
        directory_links2.append(temp_link)

    for i in directory_links2:
        for link in i:
            temp_pdf_link = extract_directory_links(link)
            for pdf_url in temp_pdf_link:
                print("pdf_url" ,pdf_url)
                save_path = pdf_url.replace("https://dl.ibdocs.re/api/IB%20PAST%20PAPERS%20-%20SUBJECT/Group%204%20-%20Sciences/", '').replace("%20","_")
                save_path = 'downloaded_pdfs/'+ save_path
                download_pdf(pdf_url, save_path)
    
    print("Sucessfully downloaded all files")
    browser.quit()

if __name__ == "__main__":
    main()
