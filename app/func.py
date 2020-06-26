import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from app.utils import get_data_covid
from dash.dependencies import Input, Output
from scipy.interpolate import interp1d  #utile pour calculer le radius


def index_page():
    data_covid = get_data_covid()
    covid_df = data_covid['covid_df']
    covid_data_Yesterday = data_covid['covid_data_Yesterday']
    confirmed_by_date_US_xUS = data_covid['confirmed_by_date_US_xUS']
    confirmed_top_countries = data_covid['confirmed_top_countries']
    Top10_country = data_covid['Top10_country']
    country_df=data_covid['country_df']
    print("covid_data_Yesterday")
    print(covid_data_Yesterday)
    us_brazil_restoftheworld = px.line(
        confirmed_by_date_US_xUS,
        x="date",
        y="Confirmed",
        color='US_flg',
        title='Comparison between Us & Brazil and the rest of the world')

    Evolution_heading = html.H2(id='nav-ev-link', children='Evolution of the cases', className='mt-5 pb-3 text-center')
    evolution_country = px.line(confirmed_top_countries,
                                x="date",
                                y="Confirmed",
                                color='Country'
                               )

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
                              brand="COVID-19 Data Visualization ",
                              brand_href="/",
                              color="dark",
                              dark=True,
                              className="p-3 fixed-top")

    # world_cases
    world_cases = dbc.Container(
    [
        html.H2('World CASES', style = {'text-align': 'center'}),
        
        dbc.Row(
            [
                dbc.Col(children = [html.H4('Confirmed'), 
                        html.Div(country_df['Confirmed'].sum(), className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H4('Recovered', style = {'padding-top': '0px'}),
                        html.Div(country_df['Recovered'].sum(), className='text-success', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Death', style = {'padding-top': '0px'}), 
                        html.Div(country_df['Deaths'].sum(), className='text-danger', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('New Cases', style = {'padding-top': '0px'}), 
                        html.Div(covid_data_Yesterday['new_cases'].sum(), className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
            
            ]
        , className='my-4 shadow justify-content-center'),
            
    ]
    )
    content = html.Div([
        navbar,
        dbc.Container(children=[
            global_map_heading,
            dcc.Graph(id='global_graph', figure=map_fig)
        ]),
        world_cases,
        dbc.Container(
            children=[T10_heading,
                      dcc.Graph(id='Top10', figure=Top10)
        ]),    
        dbc.Container(children = [Evolution_heading, dcc.Graph(id='evolution_country', figure=evolution_country)
        ]),
         dbc.Container(children = [dcc.Graph(id='us_brazil_restoftheworld', figure=us_brazil_restoftheworld)
        ]),
    ])

    return content