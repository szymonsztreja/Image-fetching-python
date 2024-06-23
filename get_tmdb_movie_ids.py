import requests
import csv
import json
import time


headers = {
    "accept": "application/json",
    "Authorization": "Bearer "
}


def search_movies_by_title(headers, title):
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page=1"
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     return response.json()['results']
    # else:
    #     return None
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'results' in data and data['results']:
            # Assuming the first result is the most relevant
            movie_id = data['results'][0]['id']
            return movie_id
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


def read_csv_file(file_name):
    move_list = []
    with open(file_name, newline='') as csvfile:
        # spamreader = csv.reader(csvfile, delimiter='')
        for movie in csvfile:
            move_list.append(movie.strip())

    return move_list



def save_dataset(dataset, filename):
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)


if __name__ == "__main__":
    movies = read_csv_file("stopmotion.csv")

    # movies_id = []
    dataset = []

    for title in movies:
        movie_id = search_movies_by_title(headers, title)
        if movie_id:
            dataset.append({'title': title, 'tmdb_id': movie_id})
        else:
            print(f"Movie '{title}' not found.")
        time.sleep(0.2)

    
    save_dataset(dataset, 'movie_dataset.json')
    


    # print(movies_id)
    