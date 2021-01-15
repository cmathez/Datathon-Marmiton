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

df_starter_N = pd.read_csv("data/df_entrees.csv")
df_meal_N = pd.read_csv("data/df_plats.csv")
df_dessert_N = pd.read_csv("data/df_desserts.csv")

df_recipes_N = pd.concat([df_starter_N,df_meal_N,df_dessert_N])
df_recipes_N['Xmas recipe'] = True


## No christmas data

df_starter = pd.read_csv("data/df_entrees_pas_noel.csv")
df_starter['category']='aperitif/starter'
df_meal = pd.read_csv("data/df_plats_pas_noel.csv")
df_meal['category']='meal'
df_desserts = pd.read_csv("data/df_desserts_pas_noel.csv")
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
        dbc.Input(id="text-enter", placeholder="Donnez l'url d'une recette marmiton...", type="text"),
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
def get_recommandation(value):
    if len(df[df['links']==value])==0:
        return html.P("La recette demandée n'est pas disponible")
    
    else :
        dff = df.copy()
        df_reco = choose_recipe(DataProcessing(dff),value)
        reco_layout = html.Div(
            dbc.Row([
                dbc.Col([
                    dbc.NavLink(df_reco.loc[0,'title'], className = 'display-reco', active=True, href=df_reco.loc[0,'links'], external_link=True,),
                    html.Hr(),
                    html.P(f"Note {df_reco.loc[0,'rate']} | Likes {df_reco.loc[0,'likes']} | Pour {df_reco.loc[0,'number people']} personnes")

                ]),

                dbc.Col([
                    dbc.NavLink(df_reco.loc[1,'title'], className = 'display-reco', active=True, href=df_reco.loc[1,'links'], external_link=True,),
                    html.Hr(),
                    html.P(f"Note {df_reco.loc[1,'rate']} | Likes {df_reco.loc[1,'likes']} | Pour {df_reco.loc[1,'number people']} personnes")


                ]),

                dbc.Col([
                    dbc.NavLink(df_reco.loc[2,'title'], className = 'display-reco', active=True, href=df_reco.loc[2,'links'], external_link=True,),
                    html.Hr(),
                    html.P(f"Note {df_reco.loc[2,'rate']} | Likes {df_reco.loc[2,'likes']} | Pour {df_reco.loc[2,'number people']} personnes")


                ])
            ])
        )

        return reco_layout

@app.callback(Output("reco-original", "children"), [Input("select", "value")])
def output_text(value):
    return html.P(value)
