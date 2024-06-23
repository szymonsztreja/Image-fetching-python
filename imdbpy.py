import csv
from imdb import Cinemagoer
import json

def get_imdb_id(movie_list):
    ia = Cinemagoer()
    movie_title = movie_list['title']
    movie_date = movie_list['date']
    search_results = ia.search_movie(movie_title)
    
    for movie in search_results:
        if 'year' in movie.keys() and movie['year'] == movie_date:
            return movie
    return None


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        movies = json.load(file)
    return movies


def save_json_dataset(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)


def new_json(movies_json, output_json):
    movies = read_json(movies_json)
    movies_with_ids = []
    for movie in movies:
        title = movie['title']
        date = movie['date']
        imdb_id = get_imdb_id(movie)
        if imdb_id:
            movies_with_ids.append({'title': title, 'imdb_id': imdb_id.movieID})
            try:
                print(f"Processed: {title} -> {imdb_id}")
            except UnicodeEncodeError:
                print(f"Processed: {title.encode('utf-8')} -> {imdb_id}")
        else:
            print(f"No match for movie: {title} year: {date}")
    save_json_dataset(movies_with_ids, output_json)


if __name__ == "__main__":
    movies_json = 'movies_title_date.json'
    output_json = 'title_imdb_id.json'
    new_json(movies_json, output_json)
