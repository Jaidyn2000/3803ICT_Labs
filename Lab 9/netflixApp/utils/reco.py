# -*- coding: utf-8 -*-
import pickle
import numpy as np
import os
from utils.load import get_similarity_scores, get_idx_to_mid, get_mid_to_idx, \
    get_movies, get_movie_name

idx_to_mid = None
mid_to_idx = None
movies = None
similarity_scores = None

def load_files():
    global similarity_scores
    global idx_to_mid
    global mid_to_idx
    global movies
    similarity_scores = get_similarity_scores()
    idx_to_mid = get_idx_to_mid()
    mid_to_idx = get_mid_to_idx()
    movies = get_movies()


def getSimScores(mid):
    idx = mid_to_idx[int(mid)]
    return similarity_scores[idx]

def getRankedRecos(sims):
    nMovies = []
    recommendations = np.argsort(sims)[-1::-1]
    movieIDs = [idx_to_mid[x] for x in recommendations]
    for mid in movieIDs:
        sim = sims[mid_to_idx[mid]]
        name = movies[mid]['title']
        nMovies.append((mid, sim, name))
    
    return nMovies


def get_sim_scores(list_mids):
    similarityScores = []
    for mid in list_mids:
        similarityScores.append(getSimScores(mid))
    
    return similarityScores


def get_reco(list_mids, N=10, exclude_selection=True):
    # TODO: Create the function that returns a list of N recommendations
    # (in the format list of tuples (mid, score, name))
    # based on a list of mids selected
    # [BONUS]: remove movies selected by user from final recommendations
    # when exclude_selection is set to True
    # We start by loading the files as global variable
    load_files()

    # I took the average similarity score for every movie selected
    sims = get_sim_scores(list_mids)
    similarityScores = [] 
    for i in range(len(sims[0])):
        temp = 0
        for j in range(len(sims)):
            temp += sims[j][i]
        temp /= len(sims)
        similarityScores.append(temp)
    if not exclude_selection:
        return getRankedRecos(similarityScores)[:N]
    else:
        return getRankedRecos(similarityScores)[len(list_mids):N+len(list_mids)]
