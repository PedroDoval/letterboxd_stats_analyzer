from wordcloud import WordCloud
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def plot_bars_messages(count_messages, title, output_dir, xlabel, filename=None):
    filename = title.replace("/", "-") if filename is None else filename
    values = count_messages.values()
    names = count_messages.keys()

    fig = plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel("Nº películas")
    plt.xticks(rotation=65, ha="right")
    plt.title(title, fontweight="bold")
    plt.bar(names, values, color='#00e054', edgecolor='black')
    fig.savefig(os.path.join(output_dir, filename + ".png"), transparent=True, bbox_inches='tight')
    #plt.show()


def plot_pie_messages(count_messages, title, output_dir, filename=None):
    filename = title.replace("/", "-") if filename is None else filename

    values = count_messages.values()
    names = count_messages.keys()

    fig = plt.figure()
    plt.title(title, fontweight="bold")
    colors = ['#00e054', '#ff8000']
    plt.pie(values, labels=names, colors=colors)#, edgecolor='black')
    fig.savefig(os.path.join(output_dir, filename + ".png"), transparent=True, bbox_inches='tight')
    #plt.show()


def plot_day_and_hour(df, title, user, output_dir, filename=None):
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(title)

    max_value = max(list(df[df.columns].max())) * 0.8
    print(max_value)
    ax = sns.heatmap(
        df,
        annot=True,
        cmap="Greens",
        annot_kws={"size": 35 / np.sqrt(len(df))},
        fmt="g",
        vmin=0,
        vmax=max_value,
    )
    plt.xticks(rotation=50, fontsize=8)
    plt.yticks(fontsize=8)
    fig.savefig(os.path.join(output_dir, "plot_day_and_hour_" + user + ".png"), transparent=True, bbox_inches='tight')
    # colorbar = ax.collections[0].colorbar
    # colorbar.set_ticks([0, 2.2])
    # plt.show()


def plot_pie_messages(count, title, output_dir, filename=None):
    filename = title.replace("/", "-") if filename is None else filename

    values = count.values()
    names = count.keys()

    fig = plt.figure()
    plt.title(title, fontweight="bold")
    colors = ['#00e054', '#ff8000']
    plt.pie(values, labels=names, colors=colors, autopct=lambda p: '{:.0f}'.format(p * sum(values) / 100), shadow=True)
    fig.savefig(os.path.join(output_dir, filename + ".png"), transparent=True, bbox_inches='tight')
    #plt.show()


def plot_lists_pies(lists, config, filename=None):
    title = "user_lists"
    filename = title.replace("/", "-") if filename is None else filename


    fig = plt.figure()
    fig.suptitle('Listas y % de películas vistas', fontweight="bold")
    # 2 rows 2 columns
    rows = int(len(lists)/2)
    if len(lists)%2 == 1: rows += 1
    i=0
    j=0
    index = 0
    colors = ['#00e054', '#ff8000']
    for lista in lists:
        values = [lista["num_watched"], lista["size"]-lista["num_watched"]]
        # first row, first column

        ax1 = plt.subplot2grid((rows, 2), (i,j))

        plt.pie(values, colors=colors,shadow=True)
        plt.title(lista["name"] + " " + '({:.0f}/{:.0f})'.format(values[0], sum(values) ))
        if index % 2 == 1:
            i+=1
            j=0
        else:
            j=1
        index += 1

    patches, texts = ax1.pie(values, colors=colors, startangle=90)  # use this plot to show the legend
    plt.legend(patches, ['seen', 'unseen'], bbox_to_anchor=(2.3, 2), prop={'size': 10}, loc='best')  # show the legend defined in labels
    fig.savefig(os.path.join(config["output_dir"], filename + ".png"), transparent=True, bbox_inches='tight')
    #plt.show()

def equalize_size_list(lista, maxsize):
    while len(lista) < maxsize:
        lista.append("")
    return lista

def plot_table(max_films, max_rate, min_films, min_rate, output_dir, filename):

    max_len = max(len(max_films), len(min_films))

    max_films = equalize_size_list(list(max_films), max_len)
    min_films = equalize_size_list(list(min_films), max_len)
    data = np.array([list(max_films), list(min_films)]).transpose()
    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = plt.table(cellText=data,
        rowLabels=["" for i in range(0,max_len)],
        colLabels=["Highest score ("+str(max_rate)+"★)","Worst score ("+str(min_rate)+"★)"],
        loc='center',
        cellLoc ='center',
    )
    table[(0,0)].set_facecolor("#00e054")
    table[(0,1)].set_facecolor("#00e054")
    #ax.set_title("Movies with higher or smaller rating")
    fig.savefig(os.path.join(output_dir, filename + ".png"), transparent=True)# bbox_inches='tight')
    #plt.show()

def wordcloud(texts, output_dir):
    # Creating word_cloud with text as argument in .generate() method
    # https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html #cividis

    word_cloud = WordCloud(collocations=False, colormap='copper', background_color=None, mode='RGBA', contour_width=1).generate(texts)
    # Display the generated Word Cloud
    #plt.imshow(word_cloud, interpolation='bilinear')
    #plt.axis("off")
    word_cloud.to_file(os.path.join(output_dir, "wordcloud" + ".png"))
    #fig.savefig(os.path.join(output_dir, "wordcloud" + ".png"), transparent=True)
    #plt.show()
