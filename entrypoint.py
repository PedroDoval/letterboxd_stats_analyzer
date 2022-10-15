import nltk
import plot_utils
from data_processor import get_month_distribution, get_month_distribution_all_year, get_year_distribution, get_weekday_distribution
import os

output_dir = None



def plot_distribution_films_by_month(month_distribution_data, web_service=False):
    title = "Películas cada mes"
    filename = "films_by_month"
    plot_utils.plot_bars_messages(month_distribution_data, title, output_dir, filename, transparent=web_service)

def plot_distribution_films_by_week(week_distribution_data, web_service=False):
    title = "Películas cada día de la semana"
    filename = "films_by_week"
    plot_utils.plot_bars_messages(week_distribution_data, title, output_dir, "Día de la semana", filename, transparent=web_service)

def plot_distribution_films_by_year(year_distribution, web_service=False):
    title = "Películas cada año"
    filename = "films_by_year"
    plot_utils.plot_bars_messages(year_distribution, title, output_dir, "Año", filename, transparent=web_service)




def plot_lists_data(lists_data, config):
    filename = "list_pies_plot"
    plot_utils.plot_lists_pies(lists_data, config, filename)

def plot_rewatched_info(rewatched_rate, rewatched_percentage):
    title = "Rate of rewatched films (" + str(rewatched_percentage) + "%)"
    filename = "pie_rewatched"
    plot_utils.plot_pie_messages(rewatched_rate, title, output_dir, filename)

def plot_ratings_entrypoint(ratings_data, diary):
    max_films, max_rate, min_films, min_rate, not_rated, percentage = ratings_data.values()
    rated_rate = {"Rated": len(diary)-not_rated, "Not rated": not_rated }
    title = "Rated films (" + str(percentage) + "%)"
    filename = "pie_rated"
    plot_utils.plot_pie_messages(rated_rate, title, output_dir, filename)
    filename = "table_rates"
    plot_utils.plot_table(max_films, max_rate, min_films, min_rate, output_dir, filename)

def plot_ratings_distribution_entrypoint(ratings_distribution, avg_rate):
    title = "Distribución de votos en el año (Media: {:.2f})".format(round(avg_rate,2))
    filename = "rate_distrib.png"
    plot_utils.plot_bars_messages(ratings_distribution, title, output_dir, "Votación", filename)


def plot_reviews_wordcloud(texts, config):
    plot_utils.wordcloud(texts, config["output_dir"])





