## Page with recommandation algorithm

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app

    # To maniplutate data

from DataProcessing import *
import pandas as pd
import numpy as np


    # To dataviz

import plotly.express as px
import plotly.graph_objects as go


### Import data files and condat df
## Christmas data 


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


###### create static figure

dff=df.copy()

fig_boxplot = px.box(dff, x="category", y="rate", color='Xmas recipe')

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Quelles sont les tendances à Noël ?", tab_id="tab_trend"),
                ],
                id="card-tabs-trend",
                card=True,
                active_tab="tab_trend",
            )
        ),
        html.Br(),
        dbc.CardBody(html.Div(id="card-content-trend", className="card-text")),
    ]
)

tab_trend_content = html.Div([
    html.Div(
    [   
        dbc.Input(id="enter-ing", placeholder="Entre un ingrédient ...", type="text", debounce=True),
        html.Br(),
        dcc.Graph(id="result-enter-ing"),
    ])
,
    html.Div([
        html.H3("Les notes diffèrent elles selon si c'est une recette de Noël"),
        dcc.Graph(fig_boxplot)
    ])
])

layout = html.Div([card])


@app.callback(
    Output("card-content-trend", "children"), [Input("card-tabs-trend", "active_tab")]
)
def display_tab_content(active_tab):
    if active_tab == "tab_trend":    
        return tab_trend_content


@app.callback(Output("result-enter-ing", "figure"), [Input("enter-ing", "value")])
def output_text(value):


    list_ing_recipe_N = df_recipes_N['ingredients'].to_list()
    list_ing_recipe = df_recipes['ingredients'].to_list()

    freq_ing_N = sum([1 if value.lower() in recipe.lower() else 0 for recipe in list_ing_recipe_N])
    freq_ing = sum([1 if value.lower() in recipe.lower() else 0 for recipe in list_ing_recipe])


    if freq_ing == 0 and freq_ing_N ==0:
        print('ok')
        return html.P("Cet ingrédient n'est pas présent dans nos recettes")

    else:
        labels = ['Noël', 'Pas Noël']
        values = [freq_ing_N, freq_ing]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
        return fig