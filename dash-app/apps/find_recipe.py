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

tab_filter_content = dbc.Card(
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

tab_original_content = dbc.Card(
    dbc.CardBody(
        [

        dbc.Select(
            id="select",
            options=[
                {"label": "Entrée", "value": "1"},
                {"label": "Plat", "value": "2"},
                {"label": "Dessert", "value": "3"},
    ],
),
           html.Div(id='reco_original'),
        ]
    ),
)





tab_text_content = dbc.Card(
    dbc.CardBody(
        [
           html.Div(
    [
        dbc.Input(id="text-enter", placeholder="Donne le nom d'une recette...", type="text"),
        html.Br(),
        html.Div(id="reco-text"),
    ]
),
        ]
    ),
)



card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Par recette", tab_id="tab_text"),
                    dbc.Tab(label="Par filtres", tab_id="tab_filter"),
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

@app.callback(Output("reco-text", "children"), [Input("text-enter", "value")])
def output_text(value):
    return html.P(value)

@app.callback(Output("reco-original", "children"), [Input("select", "value")])
def output_text(value):
    return html.P(value)