import numpy as np
import pandas as pd
import time
import re
import ast

# Dask
import dask.array as da
import dask.dataframe as dd
from dask_ml import preprocessing
from dask_ml.metrics import euclidean_distances
from dask_ml.cluster import KMeans
from dask_ml.cluster import SpectralClustering


def processMetadata():
    # This function makes some fixes on the file metadata_movies.csv to make easier to extract features from it.
    # Loading the movies_metadata and convert "id" column to "int32".
    metadata = pd.read_csv('../input/movies_metadata.csv',
                           low_memory=False, dtype={'id': 'str'})
    metadata['id'] = metadata['id'].apply(
        lambda x: re.sub(r'\d+\-\d+\-\d+', "0", x))
    metadata['id'] = metadata['id'].astype("int32")
    # Transform the column "genres" from Metadata into an array with only the names of the genres.


def getGenres(row):
        # Returns the values of key "name" from the genres dictionary.
        genres = [dct['name'] for dct in row]
        return genres
    metadata['genres'] = metadata['genres'].apply(
        lambda x: getGenres(ast.literal_eval(x)))
    # Loading the id links between metadata and ratings and merging it on metadata.
    links = pd.read_csv('../input/links.csv', index_col='movieId')
    metadata = metadata.merge(
        links['tmdbId'], how='left', left_on='id', right_on=links.index)
    metadata.to_csv("../input/movies_metadata_fixed.csv", index=False)
    return metadata


def genresDummies(metadata):
    # This function receives a DataFrame with two columns (id and genres) and returns a new dataframe
    # with dummy columns for all genres.
    genres = metadata[['id', 'genres']]
    genres_dummies = genres.join(
        genres['genres'].str.join('|').str.get_dummies())
    genres_dummies.drop("genres", axis=1, inplace=True)
    genres_dummies.set_index('id')
    genres_dummies.to_csv("../input/genres_dummies.csv", index=False)
    return genres_dummies


def main():
    genresDummies(processMetadata())  # Create genres_dummies.csv
    # ratings = dd.read_csv('/content/drive/My Drive/movie-recommender-input/ratings.csv')
    ratings = dd.read_csv('../input/ratings.csv')
    ratings.compute()
    ratings = addMoviesCount(ratings)


if __name__ == "__main__":
    main()
