import os
import requests
from bs4 import BeautifulSoup
from count_vehicle import *

google_image = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

image_folder_path = "dataset_scrape/imgs"

def main():
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)
    download_images()

def download_images():
    data = 'traffic_images_hd'
    n_images = int(input('How many images do you want? '))

    newdir = image_folder_path + '/' + data + 's' 
    if not os.path.exists(newdir):
        os.makedirs(newdir)

    start_index = 0
    image_id = 0

    while n_images > 0:
        search_url = google_image + 'q=' + data + '&start=' + str(start_index)
        response = requests.get(search_url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

        count = 1
        links = []

        for result in results:
            try:
                link = result['data-src']
                links.append(link)
                count += 1
                if count > n_images:
                    break
            except KeyError:
                continue

        print(f"Downloading {len(links)} images...")

        for i, link in enumerate(links):
            response = requests.get(link)
            image_id += 1
            image_name = newdir + '/' + data + str(image_id) + '.jpg'

            with open(image_name, 'wb') as fh:
                fh.write(response.content)

        n_images -= len(links)
        start_index += 100


if __name__ == "__main__":
    main()
