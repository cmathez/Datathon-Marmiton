## Page with analyses

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

    # To maniplutate data

from DataProcessing import *
import pandas as pd
import numpy as np
import pytz

    # To dataviz

import plotly.express as px
import plotly.graph_objects as go

df_starter_N = pd.read_csv("data\df_entrees.csv")
df_meal_N = pd.read_csv("data\df_plats.csv")
df_dessert_N = pd.read_csv("data\df_desserts.csv")

df_recipes_N = pd.concat([df_starter_N,df_meal_N,df_dessert_N])
df_recipes_N['Xmas recipe'] = True


## No christmas data

df_starter = pd.read_csv("data\df_entrees_pas_noel.csv")
df_starter['category']='aperitif/starter'
df_meal = pd.read_csv("data\df_plats_pas_noel.csv")
df_meal['category']='meal'
df_desserts = pd.read_csv("data\df_desserts_pas_noel.csv")
df_desserts['category'] = 'dessert'

df_recipes = pd.concat([df_starter,df_meal,df_desserts])
df_recipes['Xmas recipe'] = False
df_recipes.drop('gender', axis = 1, inplace = True)
df_recipes.rename(columns = {"link":"links"}, inplace = True)
df = pd.concat([df_recipes_N, df_recipes]).reset_index()




filters = html.Div(id = "block-filters", children = [
                    dcc.RadioItems(         # to create filter (by day, week, month, year)
                        id='crossfilter',
                        options=[{'label': i, 'value': i} for i in ['day', 'week', 'month', 'year']],
                        value='month',
                        labelStyle={'display': 'inline-block'})]
                )

tab_starter_content = dbc.Card(
    dbc.CardBody(
        [
           filters,
           dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname  was not recognised..."),
        ]
    )
           
        ]
    ),
)

tab_meal_content = dbc.Card(
    dbc.CardBody(
        [
           html.P('Test_top'),
        ]
    ),
)
tab_dessert_content = dbc.Card(
    dbc.CardBody(
        [
           html.P('Test_raw'),
        ]
    ),
)

tab_all_content = dbc.Card(
    dbc.CardBody(
        [
           html.P('Test_raw'),
        ]
    ),
)


card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Entrée", tab_id="tab_starter"),
                    dbc.Tab(label="Plat", tab_id="tab_meal"),
                    dbc.Tab(label="Dessert", tab_id="tab_dessert"),
                    dbc.Tab(label="Tout", tab_id="tab_all")
                ],
                id="card-tabs",
                card=True,
                active_tab="tab_starter",
            )
        ),
        html.Br(),
        dbc.CardBody(html.Div(id="card-content", className="card-text")),
    ]
)

layout = html.Div([card])


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def display_tab_content(active_tab):
    if active_tab == "tab_starter":    
        return tab_starter_content
    elif active_tab == 'tab_meal':
        return tab_meal_content
    elif active_tab == 'tab_dessert':
        return tab_dessert_content
    elif active_tab == 'tab_all':
        return tab_all_content
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {active_tab} was not recognised..."),
        ]
    )