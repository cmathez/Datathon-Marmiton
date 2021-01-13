## Page with recommandation algorithm

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

tab_text_content = dbc.Card(
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

tab_filter_content = dbc.Card(
    dbc.CardBody(
        [
           html.P('Test_top'),
        ]
    ),
)
tab_original_content = dbc.Card(
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
                    dbc.Tab(label="Nom de recette", tab_id="tab_text"),
                    dbc.Tab(label="Filtres", tab_id="tab_filter"),
                    dbc.Tab(label="Recette audacieuse", tab_id="tab_original"),
                ],
                id="card-tabs-find",
                card=True,
                active_tab="tab_text",
            )
        ),
        html.Br(),
        dbc.CardBody(html.Div(id="card-content-find", className="card-text")),
    ]
)

layout = html.Div([card])


@app.callback(
    Output("card-content-find", "children"), [Input("card-tabs-find", "active_tab")]
)
def display_tab_content(active_tab):
    if active_tab == "tab_text":    
        return tab_text_content
    elif active_tab == 'tab_filter':
        return tab_filter_content
    elif active_tab == 'tab_original':
        return tab_original_content
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {active_tab} was not recognised..."),
        ]
    )