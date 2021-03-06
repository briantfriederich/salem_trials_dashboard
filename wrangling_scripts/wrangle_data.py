import pandas as pd
import plotly.graph_objs as go

def cleanplacesdf(dataset):
    df = pd.read_csv(dataset)
    df.columns = ["accused_witch", "residence", "month_of_accusation",
    "month_of_execution", "sort"]

    places = df.groupby(["residence"])["residence"].count()
    places = places.to_frame("places_count").reset_index()

    longlatdf = {' Amesbury ':[42.8584, -70.9300], ' Andover ':[42.6583, -71.1368],
                 ' Beverly ':[42.5584, -70.8800], ' Billerica ':[42.5584, -71.2689],
                 ' Boston ':[42.3601, -71.0589], ' Boxford ':[42.6612, -70.9967],
                 ' Charlestown ':[42.3782, -71.0602], ' Chelmsford ':[42.5998, -71.3673],
                 ' Gloucester ':[42.6159, -70.6620], ' Haverhill ':[42.7762, -71.0773],
                 ' Ipswich ':[42.6792, -70.8412], ' Lynn ':[42.4668, -70.9495],
                 ' Malden ':[42.4251, -71.0662], ' Manchester ':[42.5778, -70.7676],
                 ' Marblehead ':[42.5000, -70.8578], ' Piscataqua, Maine ':[43.0881, -70.7361],
                 ' Reading ':[42.5257, -71.0953], ' Rowley ':[42.7167, -70.8787],
                 ' Salem Town ':[42.5195, -70.8967], ' Salem Village ':[42.5750, -70.9321],
                 ' Salisbury ':[42.8417, -70.8606], ' Topsfield ':[42.6376, -70.9495],
                 ' Wells, Maine ':[43.3222, -70.5805], ' Woburn ':[42.4793, -71.1523]}

    places['longlat'] = places['residence'].map(longlatdf)
    places[['long', 'lat']] = pd.DataFrame(places.longlat.values.tolist(), index=places.index)
    places['text'] = places['places_count'].map(str) + " accused in" + places['residence']

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
    df.columns = ["name", "petition", "church"]
    df = df.groupby(["church", "petition"])["name"].count()
    df = df.to_frame("petition_count").reset_index()

    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    graph_one = []
    df = cleanparrisdf('data/Salem-Village-Data-Set.csv')
    sources = [0,0,0,1,1,1]
    targets = [2,3,4,2,3,4]
    values = df["petition_count"].tolist()

    data_one = dict(
        type = 'sankey',
        node = dict(
            pad = 10,
            thickness = 30,
            line = dict(
                color = "black",
                width = 0.5
            ),
            label = ["Church Member", "Non-Church Member", "Anti-Parris Signatory", "Non-Signatory", "Pro-Parris Signatory"],
            color = ["red", "blue", "black", "grey", "white"]
        ),
        link = dict(
            source = sources,
            target = targets,
            value = values
        ))

    layout_one = dict(
        title = 'Salem Residents\' Stance on Minister Samuel Parris in 1695'
    )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df = cleantimelinedf('data/Accused-Witches-Data-Set.csv')
    x_val = df["month"].tolist()
    y_val1 = df["accusation_count"].tolist()
    y_val2 = df["execution_count"].tolist()

    graph_two.append(
      go.Scatter(
      x = x_val,
      y = y_val1,
      mode = 'lines+markers',
      name = "People Accused of Witchcraft"
      )
    )
    graph_two.append(
      go.Scatter(
      x = x_val,
      y = y_val2,
      mode = 'lines+markers',
      name = "People Executed for Witchcraft"
      )
    )

    labels = ["February", "March", "April", "May", "June", "July", "August", "September", "October", "November"]

    layout_two = dict(title = 'Salem Witch Trial Victim Count Over Time',
                xaxis = dict(title = 'Month (1692)', tickvals=[k+2 for k in range(len(labels))], ticktext=labels, tickangle=315),
                yaxis = dict(title = 'Number of People'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = cleanplacesdf('data/Accused-Witches-Data-Set.csv')
    graph_three.append(
        go.Scattergeo(
            lon = df['long'],
            lat = df['lat'],
            text = df['text'],
            marker = dict(
                size = df['places_count'],
                sizeref = 2. * max(df['places_count'])/100,
                color = 'red',
                line = dict(width = 0 )
            )
        )
    )

    layout_three = dict(
        title = 'Towns Affected (Bubbles Proportional to Number Accused)',
        geo = dict(
            showframe = False,
            projection=dict( type='orthographic' ),
            showland = True,
            oceancolor = 'rgb(204, 255, 255)',
            showocean= True,
            landcolor = 'rgb(229, 255, 204)',
            lonaxis = dict( range= [-71.7 , -70.3] ),
            lataxis = dict( range= [42.3, 43.5] )
        )
    )

    figures = []
    figures.append(dict(data=[data_one], layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures
