from collections import Counter, OrderedDict
import os
import dateparser
import yaml
import logging
import plot_utils
import typer
import pandas as pd
import datetime
import data_processor
import plots_entrypoint

# Declaring the typer application
app = typer.Typer()


@app.command()
def plot(config_file):
    print("Starting analysis.")  # Press Ctrl+F8 to toggle the breakpoint.

    with open(config_file, "r") as f_stream:
        config = yaml.load(f_stream, Loader=yaml.FullLoader)

    year = config["year"]
    output_dir = config["output_dir"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    profile = data_processor.read_profile(config["input_dir"])
    print("User: " + str(profile['Username']))

    plotter = plots_entrypoint.Plotter(web_service=False, output_dir=output_dir)

    # For all history
    diary_full = data_processor.get_diary(os.path.join(config["input_dir"], 'diary.csv'), year=None)
    year_distribution = data_processor.get_year_distribution(diary_full)
    plotter.plot_distribution_films_by_year(year_distribution)

    # For one year only
    diary_year = data_processor.get_diary(os.path.join(config["input_dir"], 'diary.csv'), year)

    # Custom data filter
    #start_date = None
    #end_date = None
    ##diary = diary[diary["datetime"].apply(lambda x: check_dates(x, start_date, end_date))]

    ratings_data = data_processor.analyze_ratings(diary_year)
    plotter.plot_ratings_entrypoint(ratings_data, diary_year)

    ratings_distribution, avg_rate = data_processor.analyze_ratings_distribution(diary_year)
    plotter.plot_ratings_distribution_entrypoint(ratings_distribution, avg_rate)

    lists_data = data_processor.analyze_lists(config)
    plotter.plot_lists_data(lists_data, config)

    month_distribution_data = data_processor.analyze_distribution_films_by_month(diary_year, year)
    plotter.plot_distribution_films_by_month(month_distribution_data)

    week_distribution_data = data_processor.analyze_distribution_films_by_week(diary_year, year)
    plotter.plot_distribution_films_by_week(week_distribution_data)

    rewatched_rate, rewatched_percentage = data_processor.get_rewatched_rate(diary_year)
    plotter.plot_rewatched_info(rewatched_rate, rewatched_percentage)

    if config["get_wordcloud"]:
        reviews_texts = data_processor.get_reviews_texts(config, year=year)
        plotter.plot_reviews_wordcloud(reviews_texts, config)



if __name__ == "__main__":
    app()
