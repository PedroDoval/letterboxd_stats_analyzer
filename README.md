This is a tool for analyze the data of your Letterboxd history and represent it with plots.

# Installation
`pip install -r requirements`


# How to use

#### Get the data
Export your Letterboxd data as a zip from here.
#### Configuration
Configure the `config.yaml file
Export the zip data in the `input_dir` directory
#### Run
```commandline
python3 main.py
```



# Examples
 - WordCloud of your reviews:

 <img src="imgs/wordcloud.png" alt="wordcloud" width="400"/>

 - Distribution of films reviewed each month of the year:

 <img src="imgs/films_by_month.png" alt="wordcloud" width="400"/>

 - Distribution of films reviewed each day of the week:

 <img src="imgs/films_by_week.png" alt="wordcloud" width="400"/>

 - Distribution of films reviewed each year:

 <img src="imgs/films_by_year.png" alt="wordcloud" width="400"/>

 - Distribution of the ratings given:

 <img src="imgs/rate_distrib.png.png" alt="wordcloud" width="400"/>
