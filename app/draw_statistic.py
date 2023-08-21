from datetime import date

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

color_line = ["#B2CB07"]
bacground_color = "#454D58"
color_set = {'axes.facecolor': '#1D1D1B', 'figure.facecolor': '#1D1D1B', 'grid.color': '#000000',
             'xtick.color': '#7D7D7D', 'ytick.color': '#7D7D7D', 'axes.edgecolor': '#595959'}


def statistic_per_day(data, start_date, name_of_image):
    "Draw graphic which include values per point"
    ndata = np.array(data)
    data_frame = pd.DataFrame(dict(time=pd.date_range(start_date, periods=len(data)),
                                   value=ndata))
    print(data_frame)
    g = sns.relplot(x="time", y="value", kind="line", data=data_frame)
    g.savefig(name_of_image)
    pass


def statistic_per_week(data):
    tips = sns.load_dataset("tips")
    plot = sns.catplot(data=tips,
                       x="day",
                       y="tip",
                       kind='bar',
                       ci=50,
                       hue="sex",
                       palette="Accent", legend=False)

    plot.fig.suptitle("Value of Tips Given to Waiters, by Days of the Week and Sex",
                      fontsize=24, fontdict={"weight": "bold"})


def statistic_per_month(data):
    pass


def statistic_per_year(data):
    pass


def draw_graphic_by_values(list_of_values, name_of_image):
    x = range(len(list_of_values))

    data = {'value': list_of_values, 'step': x}
    data_set = pd.DataFrame(data)
    custom_pallet = sns.set_palette(sns.color_palette(color_line))
    sns.set(rc=color_set, palette=custom_pallet)
    g = sns.relplot(x="step", y="value", kind="line", data=data_set)
    g.savefig(name_of_image)


def draw_pipe_diagram(dict_of_values):
    color_set = {'axes.facecolor': '#1D1D1B', 'figure.facecolor': '#1D1D1B', 'grid.color': '#000000',
                 'xtick.color': '#7D7D7D', 'ytick.color': '#7D7D7D', 'axes.edgecolor': '#595959'}
    colors = sns.color_palette('hls')

    name_of_category = dict_of_values.keys()
    values_by_category = dict_of_values.values()
    color_set['text.color'] = 'white'
    for i, w in color_set.items():
        plt.rcParams[i] = w
    explode = []
    for i in range(len(dict_of_values)):
        explode.append(0.02)

    patches, texts, autotexts = plt.pie(values_by_category, labels=name_of_category, colors=colors, startangle=90,
                                        autopct='%1.0f%%',
                                        explode=explode)

    plt.legend(patches, values_by_category, title='Coins by subcategories', loc='center left', bbox_to_anchor=(0, 0))

    plt.savefig('round_diagram')
    plt.clf()
    plt.close()
    return 'round_diagram.png'
