from collections import Counter, OrderedDict
import os
import dateparser
import yaml
import logging
import plot_utils
import typer
import pandas as pd
import datetime
from data_processor import get_month_distribution, get_month_distribution_all_year, get_weekday_distribution, get_diary, filter_year, extend_dates, analyze_lists, get_rewatched_rate
import entrypoint

# Declaring the typer application
app = typer.Typer()


@app.command()
def plot(config_file):
    print("Starting analysis")  # Press Ctrl+F8 to toggle the breakpoint.

    with open(config_file, "r") as f_stream:
        config = yaml.load(f_stream, Loader=yaml.FullLoader)

    year = config["year"]
    output_dir = config["output_dir"]
    entrypoint.output_dir = output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    profile = entrypoint.read_profile(config["input_dir"])
    print("User: " + str(profile['Username']))
    # For all history
    diary_full = get_diary(os.path.join(config["input_dir"], 'diary.csv'), year=None)
    entrypoint.analyze_year(diary_full, config)
    entrypoint.analyze_reviews(config, year=None)

    # For one year only
    diary = get_diary(os.path.join(config["input_dir"], 'diary.csv'), year)

    #start_date = None
    #end_date = None
    ##diary = diary[diary["datetime"].apply(lambda x: check_dates(x, start_date, end_date))]


    entrypoint.analyze_ratings_entrypoing(diary)
    entrypoint.analyze_list(diary, config, year)
    entrypoint.analyze_month(diary, year)
    entrypoint.analyze_week(diary, year)
    entrypoint.analyze_rewatched(diary)
    entrypoint.analyze_ratings_distribution_entrypoint(diary)



if __name__ == "__main__":
    app()
