#!/usr/bin/env python3

# ====================================== #
#           MOVIE WATCHLIST APP          #
# ====================================== #

import datetime
import database


menu = """
Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Search movies.
7) Add new user.
8) Exit.

Your selection: """

welcome = "Welcome to the watchlist app!"


def prompt_new_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd.mm.yyyy): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d.%m.%Y")
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)


def print_movies(heading, movies):
    print(f"--- {heading} ---")
    for _id, title, release_date in movies:
        date_time = datetime.datetime.fromtimestamp(release_date)
        h_date = date_time.strftime("%d %b %Y")
        print(f"{_id}: {title} (in {h_date})")
    print("-----------------------")


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Enter movie id you've watched: ")
    database.watch_movie(username, movie_id)


def prompt_new_user():
    username = input("New user name: ")
    database.add_user(username)


def prompt_search_movies():
    search_text = input("Search for: ")
    movies = database.search_movies(search_text)
    print()
    if movies:
        print_movies("Search results", movies)
    else:
        print("No movies found.")


# ===================== MAIN =====================

def main():
    database.establish_connection()
    database.create_tables()
    print(welcome)
    while (user_input := input(menu)) != "8":
        print()
        if user_input == "1":           # Add new movie
            prompt_new_movie()
        elif user_input == "2":         # View upcoming movies
            movies = database.get_movies(upcoming=True)
            print_movies("Upcoming movies", movies)
        elif user_input == "3":         # View all movies
            movies = database.get_movies()
            print_movies("All movies", movies)
        elif user_input == "4":         # Watch a movie
            prompt_watch_movie()
        elif user_input == "5":         # View watched movies
            username = input("Username: ")
            print()
            movies = database.get_watched_movies(username)
            print_movies(f"{username}'s watched movies", movies)
        elif user_input == "6":         # Search movies
            prompt_search_movies()
        elif user_input == "7":         # Add new user
            prompt_new_user()
        else:
            print("Invalid input, please try again!")
    database.close_connection()

# ================================================


if __name__ == "__main__":
    main()
