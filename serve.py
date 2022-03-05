import zipfile
from flask import Flask, render_template, request, redirect, url_for
import entrypoint
from data_processor import get_diary
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
        #year = 2021
        user = "peeeedrito"

        remove_files_dir('static/output')

        if uploaded_file.filename != '':

            targetdir = os.path.join(os.getcwd(), 'data/files')
            outputdir = os.path.join('static', 'output')
            entrypoint.output_dir = outputdir
            file_path = os.path.join(targetdir, uploaded_file.filename)
            uploaded_file.save(file_path)

            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(targetdir)

            input_dir = 'data/files'
            config = {"input_dir": input_dir, "output_dir": outputdir, 'year': year}

            # Get profile
            profile = entrypoint.read_profile(config["input_dir"])

            # For all history
            diary_full = get_diary(os.path.join(config["input_dir"], 'diary.csv'), year=None)
            entrypoint.analyze_year(diary_full, config)
            entrypoint.analyze_reviews(config, year=None)

            # For all years
            diary = get_diary(os.path.join(input_dir, 'diary.csv'), year)
            entrypoint.analyze_ratings_entrypoing(diary)
            entrypoint.analyze_list(diary, config, year)
            entrypoint.analyze_month(diary, year)
            entrypoint.analyze_week(diary, year)
            entrypoint.analyze_rewatched(diary)


        plot_files = os.listdir(outputdir)
        plot_files = [file for file in plot_files]
        # https://html5-templates.com/preview/infinite-scroll-image-gallery.html citar!!!
        return render_template('accepted.html', plot_files=plot_files, user=profile['Username'], year=year)
        #return render_template('accepted.html') #redirect(url_for('index'))
    except:
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