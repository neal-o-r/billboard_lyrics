import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import layout, widgetbox


df = pd.read_csv('billboard.csv')

df = df[df.Lyrics.notnull()]

df['Words'] = df.Lyrics[df.Lyrics.notnull()].apply(lambda x: x.split())

df['N_Words'] = df.Words.apply(lambda x: len(x) if type(x) == list else None)
df = df[df.N_Words > 1]


df['Colour'] = "olive"
df['Alpha'] = [0.8] * len(df)


desc = Div(text=open("description.html", 'r').read(), width=800)

min_year = Slider(title="Year of Release", value=1965, start=1965, end=2015, step=1)
max_year = Slider(title="End Year of Release", value=2015, start=1965, end=2015, step=1)

min_chart = Slider(title="Min Chart Position", value=1, start=1, end=100, step=1)
max_chart = Slider(title="Max Chart Position", value=100, start=1, end=100, step=1)

lyrics = TextInput(title="Search Lyrics (matches blue)")
artist = TextInput(title="Search for Artist (matches red)")


# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], artist=[], colour=[], song=[], year=[], rank=[], alpha=[]))

hover = HoverTool(tooltips=[
    ("Title", "@song"),
    ("Artist", "@artist"),
    ("Year", "@year"),
    ("Max Chart", "@rank")
])

p = figure(plot_height=800, plot_width=1000, title="", toolbar_location=None, tools=[hover])
p.circle(x="x", y="y", source=source, size=7, color="colour", line_color=None, fill_alpha="alpha")
p.yaxis.axis_label = "Lyrics Word Count"
p.xaxis.axis_label = "Year"


def select_frame():

        selected = df.copy(deep=True)
        max_year_val = max_year.value
        min_year_val = min_year.value

        max_ch_val = max_chart.value
        min_ch_val = min_chart.value
        mask = ((df.Year >= min_year_val) &
                (df.Year <= max_year_val) &
                (df.Rank >= min_ch_val)   &
                (df.Rank <= max_ch_val))

        selected = selected[mask]
        
        if (lyrics.value != ""):

                mask = selected['Lyrics'].str.lower().str.contains(lyrics.value.strip().lower())
                selected.loc[mask, 'Colour'] = 'blue'
                selected.loc[mask, 'Alpha']  = 0.8
                selected.loc[~mask, 'Colour'] = 'gray'
                selected.loc[~mask, 'Alpha'] = 0.4

        if (artist.value != ""):

                mask = selected['Artist'].str.lower().str.contains(artist.value.strip().lower())
                selected.loc[mask, 'Colour'] = 'red'
                selected.loc[mask, 'Alpha']  = 0.8
                selected.loc[~mask, 'Colour'] = 'gray'
                selected.loc[~mask, 'Alpha'] = 0.4


        return selected


def update():
        
        df_plot = select_frame()

        p.title.text = ("%d songs selected. Lyrics Search: %d; Artist Search: %d " %(len(df_plot), sum(df_plot.Colour =='blue'), sum(df_plot.Colour == 'red')))
        
        source.data = dict(
                y=df_plot['N_Words'],
                x=df_plot['Year'],
                artist=df_plot['Artist'],
                colour=df_plot['Colour'],
                song=df_plot["Song"],
                year=df_plot["Year"],
                rank=df_plot["Rank"],
                alpha=df_plot["Alpha"],
        )
                



controls = [min_year, max_year, min_chart, max_chart, lyrics, artist]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout([
    [desc],
    [inputs, p],
], sizing_mode=sizing_mode)

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Billboard Top 100 Song Lyrics 1964-2015"


