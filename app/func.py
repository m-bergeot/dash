import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from app.utils import get_data_pokemon, get_data_covid
from dash.dependencies import Input, Output
from scipy.interpolate import interp1d  #utile pour calculer le radius


def index_page():
    data_covid = get_data_covid()
    covid_df = data_covid['covid_df']
    covid_data_Yesterday = data_covid['covid_data_Yesterday']
    confirmed_by_date_US_xUS = data_covid['confirmed_by_date_US_xUS']
    confirmed_top_countries = data_covid['confirmed_top_countries']
    Top10_country = data_covid['Top10_country']
    print("covid_data_Yesterday")
    print(covid_data_Yesterday)
    us_brazil_restoftheworld = px.line(
        confirmed_by_date_US_xUS,
        x="date",
        y="Confirmed",
        color='US_flg',
        title='Comparison between Us & Brazil and the rest of the world')
    evolution_country = px.line(confirmed_top_countries,
                                x="date",
                                y="Confirmed",
                                color='Country',
                                title='Evolution of the cases')

    T10_heading = html.H2(id='nav-T10-link',
                          children='Top 10 confirmed case',
                          className='mt-5 pb-3 text-center')

    Top10 = px.bar(Top10_country, x='Country', y='Confirmed')

    # fixing the size of circle to plot in the map

    margin = covid_data_Yesterday['Confirmed'].values.tolist()
    print(margin)
    circle_range = interp1d([1, max(margin)], [0.2, 12])
    circle_radius = circle_range(margin)

    # global map heading

    global_map_heading = html.H2(children='World map view',
                                 className='mt-5 py-4 pb-3 text-center')

    # ploting the map
    token = "pk.eyJ1IjoibWVsYW5pZWJlcmdlb3QiLCJhIjoiY2s5MWc3MTRzMDNtNDNsbzdmc3kyZDdjciJ9.vdQ6g6JLvJty_GzBZ_wzNA"

    map_fig = px.scatter_mapbox(covid_data_Yesterday,
                                lat="Lat",
                                lon="Long",
                                hover_name="Country",
                                hover_data={
                                    "Lat": False,
                                    "Long": False,
                                    "Confirmed": True,
                                    "Dead": True
                                },
                                color_discrete_sequence=["#e60039"],
                                zoom=2,
                                height=500,
                                size_max=50,
                                size=circle_radius)
    map_fig.update_layout(mapbox_style="light",
                          margin={
                              "r": 0,
                              "t": 0,
                              "l": 0,
                              "b": 0
                          },
                          height=520,
                          hovermode='closest',
                          mapbox_accesstoken=token)

    # navbar code
    navbar = dbc.NavbarSimple(children=[
        html.Div("Melanie Bergeot x SoyHuCe",
                 style={
                     'color': '#fff',
                     "fontSize": "1.25rem"
                 })
    ],
                              brand="COVID-19 Data Visualization ergefg",
                              brand_href="/",
                              color="dark",
                              dark=True,
                              className="p-3 fixed-top")

    content = html.Div([
        navbar,
        dbc.Container(children=[
            global_map_heading,
            dcc.Graph(id='global_graph', figure=map_fig)
        ]),
        dbc.Container(
            children=[T10_heading,
                      dcc.Graph(id='Top10', figure=Top10)]),
    ])

    return content


def covid_page():
    content = ""
    """
    content = html.Div([
        html.Div([
            dbc.Button("Go to covid stats ", color="dark", className="mr-1", href='/covid')
            dbc.Button("Go to covid stats ",
                       color="dark",
                       className="mr-1",
                       href='/covid')
        ],
                 className='text-center container',
                 style={'paddingTop': "50px"})
    """
    return content


def pokemon_page():
    data = get_data_pokemon()
    df = pd.DataFrame({
        "height": [x['height'] for x in data],
        "weight": [x['weight'] for x in data],
        "pokemon": [x['name'] for x in data],
        "image": [x['image'] for x in data],
        "size": [x['weight'] / x['height'] for x in data]
    })
    fig = px.scatter(df,
                     x="height",
                     y="weight",
                     size='size',
                     text="pokemon",
                     hover_data=["pokemon"])
    fig = px.scatter(df,
                     x="height",
                     y="weight",
                     size='size',
                     text="pokemon",
                     hover_data=["pokemon"])
    content = ""
    """
    content = html.Div([
        html.Div([
            dbc.Button("Back to home", color="dark", className="mr-1", href='/'),
            dbc.Button(
                "Back to home", color="dark", className="mr-1", href='/'),
            html.Div([dcc.Graph(id='Pokemon and their height', figure=fig)],
                     style={"paddingTop": "40px"})
        ],
                 className='text-center container',
                 style={'paddingTop': "50px"})
    """
    return content
