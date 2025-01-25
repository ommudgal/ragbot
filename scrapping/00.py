import os
import requests
from bs4 import BeautifulSoup

os.makedirs("data", exist_ok=True)
os.makedirs("data/pdf", exist_ok=True)

with open("links.txt", "r") as file:
    urls = file.readlines()


def scrape_and_save(url, index):
    try:
        response = requests.get(url.strip())
        response.raise_for_status()

        if "application/pdf" in response.headers.get("Content-Type", ""):
            pdf_path = f"data/pdf/page_{index}.pdf"
            with open(pdf_path, "wb") as file:
                file.write(response.content)
            print(f"Successfully saved PDF from {url.strip()}")
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()

            with open(f"data/page_{index}.txt", "w", encoding="utf-8") as file:
                file.write(url.strip() + "\n" + text)
            print(f"Successfully saved content from {url.strip()}")
    except requests.RequestException as e:
        print(f"Failed to retrieve {url.strip()}: {e}")
        with open("failed.txt", "a", encoding="utf-8") as failed_file:
            failed_file.write(url.strip() + "\n")


for index, url in enumerate(urls):
    scrape_and_save(url, index)
