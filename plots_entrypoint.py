import plot_utils


class Plotter:
    def __init__(self, web_service, output_dir):
        self.web_service = web_service
        self.output_dir = output_dir

    def plot_distribution_films_by_month(self, month_distribution_data):
        title = "Películas cada mes"
        filename = "films_by_month"
        plot_utils.plot_bars_messages(
            month_distribution_data,
            title,
            self.output_dir,
            "Mes",
            filename,
            bg_transparent=self.web_service,
        )

    def plot_distribution_films_by_week(self, week_distribution_data):
        title = "Películas cada día de la semana"
        filename = "films_by_week"
        plot_utils.plot_bars_messages(
            week_distribution_data,
            title,
            self.output_dir,
            "Dia de la semana",
            filename,
            bg_transparent=self.web_service,
        )

    def plot_distribution_films_by_year(self, year_distribution):
        title = "Películas cada año"
        filename = "films_by_year"
        plot_utils.plot_bars_messages(
            year_distribution,
            title,
            self.output_dir,
            "Año",
            filename,
            bg_transparent=self.web_service,
        )

    def plot_lists_data(self, lists_data, config):
        filename = "list_pies_plot"
        plot_utils.plot_lists_pies(lists_data, config, filename)

    def plot_rewatched_info(self, rewatched_rate, rewatched_percentage):
        title = "Rate of rewatched films (" + str(rewatched_percentage) + "%)"
        filename = "pie_rewatched"
        plot_utils.plot_pie_messages(rewatched_rate, title, self.output_dir, filename)

    def plot_ratings_entrypoint(self, ratings_data, diary):
        (
            max_films,
            max_rate,
            min_films,
            min_rate,
            not_rated,
            percentage,
        ) = ratings_data.values()
        rated_rate = {"Rated": len(diary) - not_rated, "Not rated": not_rated}
        title = "Rated films (" + str(percentage) + "%)"
        filename = "pie_rated"
        plot_utils.plot_pie_messages(rated_rate, title, self.output_dir, filename)
        filename = "table_rates"
        plot_utils.plot_table(
            max_films,
            max_rate,
            min_films,
            min_rate,
            self.output_dir,
            filename,
            bg_transparent=self.web_service,
        )

    def plot_ratings_distribution_entrypoint(self, ratings_distribution, avg_rate):
        title = "Distribución de votos en el año (Media: {:.2f})".format(
            round(avg_rate, 2)
        )
        filename = "rate_distrib.png"
        plot_utils.plot_bars_messages(
            ratings_distribution,
            title,
            self.output_dir,
            "Votación",
            filename,
            bg_transparent=self.web_service,
        )

    def plot_reviews_wordcloud(self, texts, config):
        plot_utils.wordcloud(
            texts, config["output_dir"], bg_transparent=self.web_service
        )
