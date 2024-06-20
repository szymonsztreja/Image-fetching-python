import csv
from imdb import Cinemagoer
import json

def get_imdb_id(movie_title):
    ia = Cinemagoer()
    search_results = ia.search_movie(movie_title)
    if search_results:
        return search_results[0].movieID
    return None

def read_csv_file(file_name):
    move_list = []
    with open(file_name, newline='') as csvfile:
        # spamreader = csv.reader(csvfile, delimiter='')
        for movie in csvfile:
            move_list.append(movie.strip())

    return move_list

# def write_csv(file_path, data):
#     with open(file_path, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Title", "IMDb ID"])
#         for row in data:
#             writer.writerow(row)


def save_dataset(dataset, filename):
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)


def new_csv(input_csv, output_csv):
    movie_titles = read_csv_file(input_csv)
    movies_with_ids = []
    for title in movie_titles:
        imdb_id = get_imdb_id(title)
        if imdb_id:
            movies_with_ids.append({'title': title, 'imdb_id': imdb_id})
        print(f"Processed: {title} -> {imdb_id}")
    # write_csv(output_csv, movies_with_ids)
    save_dataset(movies_with_ids, 'movies_with_imdb_ids.json')


if __name__ == "__main__":
    input_csv = 'stopmotion.csv'
    output_csv = 'movies_with_imdb_ids.csv'
    new_csv(input_csv, output_csv)