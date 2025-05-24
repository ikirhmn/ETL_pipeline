import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def extract_data():
    all_data = []

    try:
        for page in range(1, 51):  # full 50 pages
            if page == 1:
                url = "https://fashion-studio.dicoding.dev"
            else:
                url = f"https://fashion-studio.dicoding.dev/page{page}"

            print(f"Scraping page {page}...")

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"[X] Error fetching page {page}: {e}")
                continue  # skip page kalau gagal

            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.select(".collection-card")
            timestamp = datetime.now().isoformat()

            for product in products:
                try:
                    title = product.select_one(".product-title").text.strip()
                    price = product.select_one(".price").text.strip()

                    details = product.select("p")
                    rating = None
                    colors = "0"
                    size = "Unknown"
                    gender = "Unknown"

                    if len(details) > 0:
                        rating_text = details[0].text.strip()
                        # parsing rating, contoh "⭐ 4.8 / 5"
                        if "⭐" in rating_text:
                            rating_raw = rating_text.split("⭐")[-1].strip()
                            rating = rating_raw.split("/")[0].strip()
                        else:
                            rating = None

                    if len(details) > 1:
                        colors = details[1].text.strip().replace(" Colors", "")

                    if len(details) > 2:
                        size = details[2].text.strip().replace("Size: ", "")

                    if len(details) > 3:
                        gender = details[3].text.strip().replace("Gender: ", "")

                    all_data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating if rating else "NaN",
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": timestamp
                    })

                except Exception as inner_err:
                    print(f"[!] Error parsing product on page {page}: {inner_err}")

            time.sleep(1)  # sopan sama server

    except Exception as e:
        print(f"[X] Error during extraction: {e}")

    return pd.DataFrame(all_data)
