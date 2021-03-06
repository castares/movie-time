import numpy as np
import pandas as pd
import time

# Dask
import dask.array as da
import dask.dataframe as dd
from dask_ml import preprocessing
from dask_ml.metrics import euclidean_distances
from dask_ml.cluster import KMeans
from dask_ml.cluster import SpectralClustering


def userGenresMatrix(ratings_ddf, genres_dummies):
    # Receives the ratings Dask Dataframe with ratings count per user and genres dummies already added.
    # Returns a matrix with userId and the sum of genres dummies per user.
    g_userid = ratings_ddf.groupby('userId')
    users_genres = g_userid[genres_dummies.columns].sum()
    users_genres = users_genres.drop('id', axis=1)
    return users_genres


def dataScaling(users_genres):
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(users_genres)
    return scaler.transform(users_genres)


def getClustersIndex(clusters, users_genres):
    clusters = dd.from_dask_array(clusters, )
    clusters = clusters.reset_index().rename(columns={0: 'cluster'})
    users_genres = users_genres.reset_index()
    clusters_index = dd.merge(users_genres, clusters,
                              left_index=True, right_on='index')
    return clusters_index[['userId', 'cluster']]


def dropZeroColumns(df):
    # Remove columns with value max = 0 from a given Pandas DataFrame.
    to_drop = [e for e in df.columns if df[e].max() == 0]
    df = df.drop(columns=to_drop)
    return df


def main():
    pass


if __name__ == "__main__":
    main()
