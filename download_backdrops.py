import os
import json
import time
import requests
import re

def sanitize_filename(filename):
    # Replace characters not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def download_backdrops(movies_data, output_root):
    # Create root directory if it doesn't exist
    if not os.path.exists(output_root):
        os.makedirs(output_root)
    
    for movie in movies_data:
        title = movie['title']
        tmdb_id = movie['tmdb_id']
        
        # Fetch backdrops from TMDB API
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/images"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMDZiMGJkMzBmNjdkMTlkYTA3MDQzY2MyYjdlN2ZmMCIsInN1YiI6IjYzOTc1MzZjOGE4OGIyMDA3ZDkzYTVmYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.weVhOAz4IBYejajHEa9VNlweNr0lGRlXa9VM4trYBeo"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            backdrops = data.get('backdrops', [])

            # Skip the iteration if backdrops is empty
            if not backdrops:
                continue

            sanitized_title = sanitize_filename(title)
            
            # Create directory for each movie
            movie_dir = os.path.join(output_root, f"{sanitized_title}")
            if not os.path.exists(movie_dir):
                os.makedirs(movie_dir)
            
            # Download each backdrop image
            for idx, backdrop in enumerate(backdrops):
                file_path = backdrop['file_path']
                full_url = f"https://image.tmdb.org/t/p/w300{file_path}"
                
                # Download image
                response = requests.get(full_url)
                if response.status_code == 200:
                    # Save image to the movie directory
                    filename = os.path.basename(file_path)
                    with open(os.path.join(movie_dir, filename), 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download image for {title}, URL: {full_url}")

                time.sleep(0.2)
        else:
            print(f"Failed to fetch images for {title}, TMDB ID: {tmdb_id}")


if __name__ == "__main__":
    # Load JSON data from file
    json_file = 'movie_dataset.json'
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # Directory to save all movie directories
    output_root_directory = './movie_backdrops'
    
    # Download backdrops
    download_backdrops(json_data, output_root_directory)
