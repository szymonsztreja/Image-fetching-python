import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
import sys

def sanitize_filename(filename):
    # Replace characters not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def fetch_imdb_images(movie_data):
    base_url = 'https://www.imdb.com/title/tt{}/mediaindex/?contentTypes=still_frame'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for movie in movie_data:
        imdb_id = movie['imdb_id']
        title = movie['title']

        # Construct URL for fetching images
        imdb_url = base_url.format(imdb_id)

        # Fetch page content
        response = requests.get(imdb_url, headers=headers)
        if response.status_code != 200:
            print(f'Error fetching page for movie "{title}": {response.status_code}')
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <img> tags in the media index section
        image_tags = soup.find_all('img', class_='ipc-image')

        if not image_tags:
            print(f'No images found for movie "{title}".')
            continue

        sanitized_title = sanitize_filename(title)
        output_folder = os.path.join('imdb_images', sanitized_title)

        # Ensure the folder for saving images exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Fetch and save each image
        for idx, img_tag in enumerate(image_tags):
            img_url = img_tag.get('src')
            if img_url:
                # Ensure the URL is absolute
                img_url = urljoin(imdb_url, img_url)
                try:
                    img_data = requests.get(img_url, headers=headers).content
                    img_filename = os.path.join(output_folder, f'{sanitized_title}_{idx+1}.jpg')
                    with open(img_filename, 'wb') as handler:
                        handler.write(img_data)
                    # Encode filename before printing to handle non-ASCII characters
                    print(f'Pobrano {img_filename.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding)}')
                except Exception as e:
                    # Encode error message before printing to handle non-ASCII characters
                    print(f'Error fetching image {img_url} for movie "{sanitized_title}": {e}'.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
            else:
                print(f'No URL for image #{idx+1} for movie "{sanitized_title}"')

if __name__ == "__main__":
    json_file = 'title_imdb_id.json'
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    fetch_imdb_images(json_data)



