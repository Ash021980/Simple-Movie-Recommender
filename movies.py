import requests_with_caching
from omdb_apikey import api_key

API_KEY = api_key


def get_movies_from_tastedive(title: str, q_type: str = "movies", limit: int = 5) -> dict:
    """Function that makes the API call to tastedive.com in order to retrieve similar/related
       movies.  Returns the response object as a dictionary.

       :rtype: dict
       :returns: json response object as a dictionary"""

    baseurl = "https://tastedive.com/api/similar"
    params = {"q": title, "type": q_type, "limit": limit}

    resp = requests_with_caching.get(baseurl, params=params)

    if type(resp) is dict:
        return resp

    return resp.json()


def extract_movie_titles(func: get_movies_from_tastedive) -> list:
    """Function to extract the movie titles from the dictionary received from the tastedive API.
       Returns a list of movie titles.

       :rtype: list
       :returns: list of movie titles"""

    resp_js = func
    resp_lst = resp_js["Similar"]["Results"]
    names_lst = [d["Name"] for d in resp_lst]

    return names_lst


def get_related_titles(movie_lst: list) -> list:
    """Function to collect the related movie titles. Returns a list consisting of the
       distinct movie names. ie no duplicate titles.

       :rtype: list
       :returns: list of related movie titles """

    return_lst = []

    if len(movie_lst) >= 1:
        for title in movie_lst:
            return_lst.extend(extract_movie_titles(get_movies_from_tastedive(title)))
    else:
        return return_lst

    return list(set(return_lst))


def get_movie_data(title: str, d_type: str = "json") -> dict:
    """Function that uses the OMBD API to get data for a specific movie.  Caches the
       response to assist with future calls.  Returns a dict of the movie's data.

       :rtype: dict
       :returns: dictionary containing the movies info"""

    baseurl = "http://www.omdbapi.com/"
    key = API_KEY
    params = {"apikey": key, "t": title, "r": d_type}
    resp = requests_with_caching.get(baseurl, params=params)

    if type(resp) is dict:
        return resp

    return resp.json()


def get_movie_rating(func: get_movie_data) -> int:
    """Function that get the Rotten Tomatoes rating for a given movie.
       Returns the rating as an int.

       :rtype: int
       :returns: the movie's rating as an int"""

    movie_d = func
    ratings_lst = movie_d["Ratings"]
    rating = 0

    for d in ratings_lst:
        if d["Source"] == "Rotten Tomatoes":
            rating_str = d["Value"]
            rating = int(rating_str.strip("%"))

    return rating


def get_sorted_recommendations(titles: list) -> list:
    """Function that sorts the movies by their ratings.  Returns a list of movie titles
       sorted from most recommended to least recommended.

       :rtype: list
       :returns: sorted list of movie recommendation from most recommended to least"""

    rating_d = {}
    empty_lst = []

    if len(titles) >= 1:
        related_movies = get_related_titles(titles)
    else:
        return empty_lst

    for movie in related_movies:
        rating = get_movie_rating(get_movie_data(movie))
        rating_d[movie] = rating

    movie_lst = sorted(list(rating_d.keys()), key=lambda x: -rating_d[x])

    return movie_lst


# Ask the user to enter one or more movies.
lst_of_movies = input("Select the movie(s) you would like recommendations based on. Separated by a comma(,):\n").split(
    ",")

# Print the results to the console
print(get_sorted_recommendations(lst_of_movies))
