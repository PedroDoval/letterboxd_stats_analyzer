import nltk
import plot_utils
from data_processor import get_profile_info, get_month_distribution, get_month_distribution_all_year, get_year_distribution, get_reviews, analyze_ratings, get_weekday_distribution, get_diary, filter_year, extend_dates, analyze_lists, get_rewatched_rate
import os

output_dir = None

def analyze_month(diary, year=None):
    month_distribution = get_month_distribution_all_year(diary) if year == None else get_month_distribution(diary)
    title = "Películas cada mes"
    filename = "films_by_month"
    plot_utils.plot_bars_messages(month_distribution, title, output_dir, filename)


def analyze_week(diary, year=None):
    weekday_distribution = get_weekday_distribution(diary)
    title = "Películas cada día de la semana"
    filename = "films_by_week"
    plot_utils.plot_bars_messages(weekday_distribution, title, output_dir, filename)

def analyze_list(diary, config, year=None):
    lists = analyze_lists(config)
    filename = "list_pies_plot"
    plot_utils.plot_lists_pies(lists, config, filename)

def analyze_rewatched(diary):
    rewatched_rate, percentage = get_rewatched_rate(diary)
    title = "Rate of rewatched films (" + str(percentage) + "%)"
    filename = "pie_rewatched"
    plot_utils.plot_pie_messages(rewatched_rate, title, output_dir, filename)

def analyze_ratings_entrypoing(diary):
    max_films, max_rate, min_films, min_rate, not_rated, percentage = analyze_ratings(diary)
    rated_rate = {"Rated": len(diary)-not_rated, "Not rated": not_rated }
    title = "Rated films (" + str(percentage) + "%)"
    filename = "pie_rated"
    plot_utils.plot_pie_messages(rated_rate, title, output_dir, filename)
    filename = "table_rates"
    plot_utils.plot_table(max_films, max_rate, min_films, min_rate, output_dir, filename)

def analyze_reviews(config, year):
    reviews = get_reviews(os.path.join(config["input_dir"], 'reviews.csv'), year)
    print(reviews.head())
    reviews_texts = reviews.Review
    print(list(reviews_texts))
    ##remove stopwords
    nltk.download('stopwords')
    text = " ".join(cat for cat in reviews_texts)
    stopwords = nltk.corpus.stopwords.words('spanish') + ['pues', 'con']
    texts = remove_stopwords(text, stopwords)

    plot_utils.wordcloud(texts, config["output_dir"])

def analyze_year(diary, config):
    year_distribution = get_year_distribution(diary)
    title = "Películas cada año"
    filename = "films_by_year"
    plot_utils.plot_bars_messages(year_distribution, title, output_dir, filename)

def read_profile(inputdir):
    profiledf = get_profile_info(os.path.join(inputdir,'profile.csv'))
    profile = profiledf.to_dict('records')[0]
    return profile


def remove_stopwords(text,stopwords):
    text = " ".join([word for word in text.split() if word.lower() not in stopwords])
    return text