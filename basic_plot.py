import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Div



output_file("basic_plot.html", title="Billboard Top 100 Song Lyrics 1964-2015")

df = pd.read_csv('billboard.csv')

df = df[df.Lyrics.notnull()]

df['Words'] = df.Lyrics[df.Lyrics.notnull()].apply(lambda x: x.split())

df['N_Words'] = df.Words.apply(lambda x: len(x) if type(x) == list else None)
df = df[df.N_Words > 1]


df['Colour'] = "olive"
df['Alpha'] = [0.8] * len(df)


desc = Div(text=open("description.html", 'r').read(), width=800)
source = ColumnDataSource(data=dict(x=[], y=[], artist=[], colour=[], song=[], year=[], rank=[], alpha=[]))

source.data = dict(
                y=df['N_Words'],
                x=df['Year'],
                artist=df['Artist'],
                colour=df['Colour'],
                song=df["Song"],
                year=df["Year"],
                rank=df["Rank"],
                alpha=df["Alpha"],
        )



hover = HoverTool(tooltips=[
    ("Title", "@song"),
    ("Artist", "@artist"),
    ("Year", "@year"),
    ("Max Chart", "@rank")
])



title = "%d songs selected"%len(df)

# create a new plot with the toolbar below
p = figure(plot_width=1200, plot_height=800,
           title=title, toolbar_location="below", tools=[hover])


p.circle(x='x', y='y', size=7, color='colour', source=source, line_color=None, fill_alpha='alpha')

p.yaxis.axis_label = "Lyrics Word Count"
p.xaxis.axis_label = "Year"

show(p)
