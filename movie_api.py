#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hosseind
"""


# Loading reqired libraries
from fastapi import FastAPI, Query
import sqlite3
import uvicorn
import json
import os

#%%

# Using fastAPI framework to implement the web API
app = FastAPI()
# Define the path to the IMDb SQLite database file
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname('/Users/hosseind/Downloads/'),'movie.sqlite'))

#%%
# Create the interface to run SQL-requests against the database
def execute_sql_query(query):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# List all directors in the database
# The web API using GET-methods to list films and directors
# API Response in JSON format
@app.get("/dirctors")
def get_directors():
    query = "SELECT DISTINCT name FROM directors GROUP BY id"
    directors = execute_sql_query(query)
    return {"directors": [director[0] for director in directors]}

# List all films in the database
@app.get("/films")
def get_movies():
    query = "SELECT original_title FROM movies"
    movies = execute_sql_query(query)
    return {"movies": [movie[0] for movie in movies]}

# List the five directors whose films have the highest average (vote) range
@app.get("/top_5_directors")
def get_top_directors(Limit: int = Query(5, description="Number of top directors"),):
    query = f"""
    SELECT DISTINCT name, vote_average FROM directors AS t1
    JOIN movies AS t2 ON t1.id = t2.director_id
    ORDER BY vote_average DESC
    LIMIT {Limit}
    """
    top_directors = execute_sql_query(query)    
    return {"top_directors": [director[0] for director in top_directors], "Average Rating": [director[1] for director in top_directors]}

# List films in the database that can be filtered and sorted by director name & film title
@app.get("/list_of_films")
def list_films(
    director: str = Query(None, description="Filter by director name"),
    title: str = Query(None, description="Filter by film title"),
    sort_by: str = Query(None, description="Sort by director name (name) or film title (title)")
):
    query = """
    SELECT movies.*, directors.name AS name
    FROM movies 
    JOIN directors ON movies.director_id = directors.id
    WHERE 1=1
    """

    if director:
        query += f" AND name = '{director}'"
    if title:
        query += f" AND title = '{title}'"

    if sort_by:
        query += f" ORDER BY {sort_by}"

    films = execute_sql_query(query)
    film_data = [{"director_name": film[13], "movie_title": film[6]} for film in films]
    return {"list_films": film_data}
#directors = list_films("James Cameron","Avatar",'name')

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)

#uvicorn movie_api:app --reload




