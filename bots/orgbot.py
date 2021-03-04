import re
import datetime
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(PATH + "/../mclare.env")
ORG_FILE = os.getenv("ORG_FILE")


def create_org_bar_chart(days, task_count):
    fig = go.Figure(go.Bar(x=task_count, y=days, orientation='h',
                           text=task_count, textposition='auto',
                           textangle=0,
                           textfont=dict(color='black'),
                           marker=dict(color=task_count, colorscale='sunset')
                           ))
    fig['layout'].update(width=224, height=448, plot_bgcolor='#fff',
                         font=dict(family="Dank Mono, Consolas, monospace",
                                   color='black',
                                   size=28),
                         xaxis=dict(showgrid=False,
                                    showline=False,
                                    showticklabels=False,
                                    zeroline=False),
                         yaxis=dict(showgrid=False,
                                    showline=False,
                                    showticklabels=True,
                                    zeroline=False),
                         margin=dict(l=10, r=10, t=10, b=10, pad=3),

                         bargap=0.5,
                         )
    return fig


def read_org_file(org_file):
    date_bins = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    now = datetime.date.today()
    prev_line = ""
    with open(org_file) as fp:
        for line in fp:
            m = ""  # default
            # Standard todo find
            if ("CLOSED" in line):
                m = re.search(r"(\d{4}-\d{2}-\d{2})", line).group(1)
            # repeating task todo find 
            elif ("- State \"DONE\"" in line):
                m = re.search(r"(\d{4}-\d{2}-\d{2})", line).group(1)
            if m:
                found_date = datetime.date.fromisoformat(m)
                difference = (now - found_date).days
                if difference < 7:
                    date_bins[difference] += 1
            else:
                prev_line = line
    return date_bins


def get_org_image(toFile=True):
    dateFormatted = datetime.date.today().strftime("%a")
    vals = read_org_file(ORG_FILE)
    x = list(vals.keys())
    task_count = list(vals.values())
    days = [
        (datetime.date.today() - datetime.timedelta(i)).strftime("%a").upper()
        for i in x
    ]
    days.reverse()
    task_count.reverse()
    subplots = create_org_bar_chart(days, task_count)
    if toFile:
        subplots.write_image(PATH + '/../assets/update/org.png',
                             format="png",
                             width=224,
                             height=448)
    else:
        return subplots


if __name__ == "__main__":
    subplots = get_org_image()

