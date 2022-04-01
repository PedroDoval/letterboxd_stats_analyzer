import math
import numpy as np
from collections import Counter, OrderedDict
import os
import dateparser
import logging
import pandas as pd
import datetime
import utils

def get_diary(diary_file, year=None):
    diary = pd.read_csv(diary_file)
    print(diary.head())
    diary = extend_dates(diary)
    if year:
        diary = filter_year(diary, year)
    return diary

def get_profile_info(profile_file):
    profile = pd.read_csv(profile_file)
    return profile

def extend_dates(diary):
    def parsedate(x):
        try:
            x = dateparser.parse(x)
        except:
            x = ""
        return x
    diary["datetime"] = diary["Watched Date"].apply(lambda x: parsedate(x))
    diary["month"] = diary["datetime"].apply(lambda x: x.month)
    diary["year"] = diary["datetime"].apply(lambda x: x.year)
    diary["weekday"] = diary["datetime"].apply(lambda x: x.weekday())
    print(diary.head())
    return diary

def check_dates(date, start_date, end_date):
    if start_date is not None:
        if date < start_date:
            return False
    if end_date is not None:
        if date > end_date:
            return False
    return True


def get_weekday_distribution(diary):


    weekdays = [date.strftime("%a") for date in diary.datetime]
    counter_weekday = dict(Counter(weekdays))
    print(counter_weekday)
    counter_weekday = dict(OrderedDict(
        sorted(counter_weekday.items(), key=lambda x: utils.weekdays_order_en.index(x[0]))
    ))

    print("Counter weekdays")
    print(counter_weekday)
    return counter_weekday


def filter_year(diary, year):

    diary = diary[diary["year"] == year]
    return diary


def get_month_distribution_all_year(diary):
    group_months = diary.groupby(["month", "year"]).size().reset_index(name="count_movies")
    group_months["unique_month"] = group_months.apply(lambda x: str(x.year) + "-" + str(x.month), axis=1)
    group_months = group_months.sort_values(by=['year', 'month'])

    print("Count by month-year")
    print(group_months)

    month_distribution = dict()
    for index, row in group_months.iterrows():
        month_distribution[row.unique_month] = row.count_movies

    print(month_distribution)
    return month_distribution

def get_month_distribution(diary):

    months = [date.strftime("%b") for date in diary.datetime]
    counter_months = dict(Counter(months))
    print(counter_months)
    counter_months = dict(OrderedDict(
        sorted(counter_months.items(), key=lambda x: utils.months_order_en.index(x[0]))
    ))

    print("Counter months")
    print(counter_months)
    return counter_months

def get_year_distribution(diary):

    counter_years = dict(Counter(diary.year))
    print(counter_years)


    print("Counter years")
    print(counter_years)
    return counter_years

def get_watched_df(config):
    watched_df = pd.read_csv(os.path.join(config["input_dir"], "watched.csv"))
    return watched_df


def analyze_lists(config):
    """Películas vistas en cada lista"""
    """ Se podría obtener la URL de la lista"""
    watched_df = get_watched_df(config)
    watched_names = watched_df["Name"]
    watched_URIS = watched_df["Letterboxd URI"]

    path_lists = os.path.join(config["input_dir"], 'lists')
    lists = list()
    for file in os.listdir(path_lists):
        if not file.endswith(".csv"): continue
        file_path = os.path.join(path_lists, file)
        print(file.replace(".csv",""))
        list_df = pd.read_csv(file_path, skiprows=4)
        list_film_names = list_df["Name"]
        list_film_URIs = list_df["URL"]

        num_watched = len(set(watched_URIS).intersection(list_film_URIs))
        percentage = get_fraction(num_watched,len(list_film_URIs))
        print(str(num_watched) + " / " + str(len(list_film_URIs)) + "  --  " + str(percentage) + "%")

        lists.append({'name':file.replace(".csv",""), 'num_watched':num_watched, 'size':len(list_film_URIs), "percentage":percentage})

    return lists


def get_fraction(value,total):
    percentage = round(100*value/total,1)
    return percentage


def get_rewatched_rate(diary):

    size_diary = len(diary)
    size_rewatched = list(diary["Rewatch"]).count('Yes')
    size_new_watched = size_diary - size_rewatched
    dict_rewatched = {"New watchs": size_new_watched, "Rewatched": size_rewatched}
    print(dict_rewatched)
    percentage = get_fraction(size_rewatched, size_diary)
    return dict_rewatched, percentage

def analyze_ratings(diary):
    ratings = list(diary["Rating"])
    print(ratings)
    #print(type(ratings[3]))
    max_rate = np.nanmax(ratings)
    min_rate = np.nanmin(ratings)

    max_films = diary[diary["Rating"]==max_rate].Name
    min_films = diary[diary["Rating"] == min_rate].Name


    not_rated = len([0 for x in ratings if math.isnan(x)])
    percentage = 100 - get_fraction(not_rated, len(ratings))
    print("Not rated films: " + str(not_rated) + "/" + str(len(ratings)) + " ("+str(percentage) +"%)")

    return max_films, max_rate, min_films, min_rate, not_rated, percentage

def analyze_ratings_distribution(diary):
    ratings = list(diary["Rating"])
    ratings = [2*r for r in ratings if str(r) != 'nan' ]
    rate_distr = dict(Counter(ratings))
    for value in utils.points_to_stars.keys():
        if value not in rate_distr:
            rate_distr[value] = 0

    return rate_distr


def get_reviews(review_file, year=None):
    reviews = pd.read_csv(review_file)
    reviews = extend_dates(reviews)
    if year:
        reviews = filter_year(reviews, year)
    return reviews