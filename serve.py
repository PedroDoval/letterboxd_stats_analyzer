import zipfile
from flask import Flask, render_template, request, redirect, url_for
import plots_entrypoint
import data_processor
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
# https://speckyboy.com/custom-file-upload-fields/

@app.route('/', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        year = int(request.form.get('year'))

        remove_files_dir('static/output')
        remove_files_dir('data/lists')

        if uploaded_file.filename != '':

            targetdir = os.path.join(os.getcwd(), 'data/')
            outputdir = os.path.join('static', 'output')
            file_path = os.path.join(targetdir, uploaded_file.filename)
            uploaded_file.save(file_path)

            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(targetdir)

            input_dir = 'data/'
            config = {"input_dir": input_dir, "output_dir": outputdir, 'year': year}

            # Get profile
            profile = data_processor.read_profile(config["input_dir"])

            plotter = plots_entrypoint.Plotter(web_service=True, output_dir=outputdir)

            # For all history
            diary_full = data_processor.get_diary(os.path.join(config["input_dir"], 'diary.csv'), year=None)
            year_distribution = data_processor.get_year_distribution(diary_full)
            plotter.plot_distribution_films_by_year(year_distribution)


            # For all years
            diary_year = data_processor.get_diary(os.path.join(input_dir, 'diary.csv'), year)

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

            reviews_texts = data_processor.get_reviews_texts(config, year=year)
            plotter.plot_reviews_wordcloud(reviews_texts, config)

        plot_files = os.listdir(outputdir)
        plot_files = [file for file in plot_files]
        # https://html5-templates.com/preview/infinite-scroll-image-gallery.html citar!!!
        return render_template('accepted.html', plot_files=plot_files, user=profile['Username'], year=year)
        #return render_template('accepted.html') #redirect(url_for('index'))
    except Exception as e:
        print(e.with_traceback())
        ## detectar errores de: año no existe
        ## de no es un zip
        ## de error inesperado
        return render_template('index.html', error=True)

def remove_files_dir(dir):

    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if __name__ == '__main__':
    app.run(host='192.168.1.35', port=5001, debug=True, threaded=False)

# sudo ufw allow 5001/tcp