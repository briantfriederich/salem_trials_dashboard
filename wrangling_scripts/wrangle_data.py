import pandas as pd
import plotly.graph_objs as go

def cleanplacesdf(dataset):
    df = pd.read_csv(dataset)
    df.columns = ["accused_witch", "residence", "month_of_accusation",
    "month_of_execution", "sort"]

    places = df.groupby(["residence"])["residence"].count()
    places = places.to_frame("places_count").reset_index()

    return places


def cleantimelinedf(dataset):
    df = pd.read_csv(dataset)
    df.columns = ["accused_witch", "residence", "month_of_accusation",
    "month_of_execution", "sort"]

    timeline_acc = df.groupby(["month_of_accusation"])["month_of_accusation"].count()
    timeline_acc = timeline_acc.to_frame("accusation_count").reset_index()
    timeline_acc = timeline_acc.rename(columns={"month_of_accusation": "month"})

    timeline_ex = df.groupby(["month_of_execution"])["month_of_execution"].count()
    timeline_ex = timeline_ex.to_frame("execution_count").reset_index()
    timeline_ex = timeline_ex.rename(columns={"month_of_execution": "month"})
    timeline_ex[["month"]] = timeline_ex[["month"]].astype(int)

    timeline = timeline_acc.merge(timeline_ex, how="left", on="month")
    timeline["execution_count"].fillna(0, inplace = True)
    timeline[["execution_count"]] = timeline[["execution_count"]].astype(int)
    timeline = timeline[timeline.month != -1]

    return timeline

def cleanparrisdf(dataset, keepcolumns = ["Petition", "Church to 1696"]):
    df = pd.read_csv(dataset)
    df = df[keepcolumns]

    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    graph_one = []
    df = cleanplacesdf('data/Accused-Witches-Data-Set.csv')
    lineslist = ["accusation_count", "execution_count"]
    for line in lineslist:
        x_val = df["month"].variable_x.tolist()
        y_val = df[line].variable_y.tolist()
    graph_one.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'lines',
      name = line
      )
    )

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df = cleanplacesdf('data/Accused-Witches-Data-Set.csv')
    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = cleanplacesdf('data/Salem-Village-Data-Set.csv')
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures
