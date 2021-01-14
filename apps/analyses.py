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