#!/usr/bin/env python3

#======================================#
#=         MOVIE WATCHLIST APP        =#
#======================================#

import datetime
import database

menu = """
Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

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
    for movie in movies:
        date_time = datetime.datetime.fromtimestamp(movie[1])
        h_date = date_time.strftime("%d %b %Y")
        print(f"{movie[0]} (in {h_date})")
    print("-----------------------")

def print_watched_movies(username, movies):
    print(f"--- {username}'s watched movies ---")
    for movie in movies:
        print(f"{movie[1]}")
    print("-----------------------")

def prompt_watch_movie():
    username = input("Username: ")
    title = input("Enter movie title you've watched: ")
    database.watch_movie(username, title)

#===================== MAIN =====================

def main():
    database.create_tables()
    print(welcome)
    while (user_input := input(menu)) != "6":
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
            print_watched_movies(username, movies)
        else:
            print("Invalid input, please try again!")

#================================================

if __name__ == "__main__":
    main()
