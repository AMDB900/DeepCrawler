from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse
from collections import deque
import csv

def is_same_domain(url, domain):
    return urlparse(url).netloc == domain

def bfs_crawl(start_url, max_urls=2000, output_csv="list.csv"):
    print(output_csv)
    visited = set()
    queue = deque([start_url])
    domain = urlparse(start_url).netloc

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--headless')  # Run in headless mode (optional)
    driver = webdriver.Chrome(options=chrome_options)

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['URL'])

        while queue and len(visited) < max_urls:
            current_url = queue.popleft()
            if current_url not in visited:
                visited.add(current_url)
                print(f"Visiting: {current_url} , {len(visited)}")
                csvwriter.writerow([current_url])

                try:
                    driver.get(current_url)
                    links = driver.find_elements(By.TAG_NAME, 'a')
                    print(f"Number of links found: {len(links)}")
                    for link in links:
                        try:
                            href = link.get_attribute('href')
                            if href and is_same_domain(href, domain) and href not in visited:
                                queue.append(href)
                        except NoSuchElementException:
                            continue
                except Exception as e:
                    print(f"Failed to access {current_url}: {e}")

    driver.quit()
    return visited

if __name__ == "__main__":
    #3
    start_url = "https://www.massgeneral.org/"
    crawled_urls = bfs_crawl(start_url, output_csv="massgen.csv")
    print(f"Total URLs visited: {len(crawled_urls)}")