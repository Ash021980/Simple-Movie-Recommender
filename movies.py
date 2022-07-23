import requests_with_caching
from omdb_apikey import api_key

API_KEY = api_key


def get_movies_from_tastedive(title: str, qtype: str = "movies", limit: int = 5) -> dict:
    """Function that makes the API call to tastedive.com in order to retrieve similar/related
       movies.  Returns the response object as a dictionary.
       :rtype: dict
       :returns: json response object as a dictionary"""
    baseurl = "https://tastedive.com/api/similar"
    params = {"q": title, "type": qtype, "limit": limit}

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
    return_lst = []
    if len(movie_lst) >= 1:
        for title in movie_lst:
            return_lst.extend(extract_movie_titles(get_movies_from_tastedive(title)))
    else:
        return return_lst
    return list(set(return_lst))


def get_movie_data(title: str, dtype: str = "json") -> dict:
    baseurl = "http://www.omdbapi.com/"
    key = API_KEY
    params = {"apikey": key, "t": title, "r": dtype}
    resp = requests_with_caching.get(baseurl, params=params)
    if type(resp) is dict:
        return resp
    return resp.json()


def get_movie_rating(func: get_movie_data) -> int:
    movie_d = func
    ratings_lst = movie_d["Ratings"]
    rating = 0

    for d in ratings_lst:
        if d["Source"] == "Rotten Tomatoes":
            rating_str = d["Value"]
            rating = int(rating_str.strip("%"))
    return rating


def get_sorted_recommendations(titles: list) -> list:
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


lst_of_movies = input("Select the movie(s) you would like recommendations based on. Separated by a comma(,):\n").split(
    ",")
print(get_sorted_recommendations(lst_of_movies))
