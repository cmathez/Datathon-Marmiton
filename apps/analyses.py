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


    # To dataviz

import plotly.express as px
import plotly.graph_objects as go

df_starter_N = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_entrees.csv")
df_meal_N = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_plats.csv")
df_dessert_N = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_desserts.csv")

df_ingredients = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_ingredients.csv")


df_recipes_N = pd.concat([df_starter_N,df_meal_N,df_dessert_N])
df_recipes_N['Xmas recipe'] = True


## No christmas data

df_starter = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_entrees_pas_noel.csv")
df_starter['category']='aperitif/starter'
df_meal = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_plats_pas_noel.csv")
df_meal['category']='meal'
df_desserts = pd.read_csv("/Users/tatianafoulon/Desktop/data/wild_school/hackathon/datathon_2/Datathon-Marmiton/data/df_desserts_pas_noel.csv")
df_desserts['category'] = 'dessert'

df_recipes = pd.concat([df_starter,df_meal,df_desserts])
df_recipes['Xmas recipe'] = False
df_recipes.drop('gender', axis = 1, inplace = True)
df_recipes.rename(columns = {"link":"links"}, inplace = True)
df = pd.concat([df_recipes_N, df_recipes]).reset_index()




filters = html.Div(id = "block-filters", children = [
                    dbc.Select(
                        id="rate",
                        options=[
                            {"label": "Tout", "value": "Tout"},
                            {"label": "Note basse", "value": "1"},
                            {"label": "Note moyenne", "value": "2"},
                            {"label": "Note élevée", "value": "3"}
                    ], value = "Tout"
                    ),
                    html.Hr(),
                    dbc.Select(
                        id="cost",
                        options=[
                            {"label": "Tout", "value": "Tout"},
                            {"label": "Assez cher", "value": "Assez cher"},
                            {"label": "Coût moyen", "value": "Coût moyen"},
                            {"label": "Bon marché", "value": "bon marché"}
                    ], value = "Tout"
                    ),
                    html.Hr(),
                    dbc.Select(
                        id="difficulty",
                        options=[
                            {"label": "Tout", "value": "Tout"},
                            {"label": "Niveau moyen", "value": "Niveau moyen"},
                            {"label": "Facile", "value": "Facile"},
                            {"label": "Trés facile", "value": "Trés facile"},
                            {"label": "Difficile", "value": "Difficile"}
                    ], value = "Tout"
                    ),
                    html.Hr(),
                    dbc.Select(
                        id="time",
                        options=[
                            {"label": "Tout", "value": "Tout"},
                            {"label": "Rapide (< 30 min)", "value": "rapide"},
                            {"label": "Moyen (entre 30 et 90 min)", "value": "moyen"},
                            {"label": "Long (> 90 min)", "value": "long"}
                            
                    ], value = "Tout"
                    ),
])

title_1 = dbc.Jumbotron(
        [
            html.H1("Quels ingrédients dans vos plats ?", className = "text-noel"),
        ]
    )

title_2 = dbc.Jumbotron(
        [
            html.H1("La difficulté dans les préparations...", className = "text-noel"),
        ]
    )

tab_theme_content = dbc.Card(
    dbc.CardBody(
        [
        html.Div(
            [title_1,
            dbc.Row([
                dbc.Col(dcc.Graph(id = "freq_ing"), width={"size" : 10}),
                dbc.Col(filters, width={"size" : 2}),
            ]),
            html.Hr(className="my-2"),
            title_2
            ]
        )
           
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
                    dbc.Tab(label="Appéritif/Entrée", tab_id="tab_starter"),
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
    if active_tab == "tab_starter" or active_tab == 'tab_meal' or active_tab == 'tab_dessert':    
        return tab_theme_content
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


# update ingredients frequencies graph
@app.callback(
    Output("freq_ing", "figure"), 
    [Input("card-tabs", "active_tab"),
    Input("rate", "value"), 
    Input("cost", "value"),
    Input("difficulty", "value"),
    Input("time", "value"),
    ]
)

def display_graph(tab, rate, cost, difficulty, time):
    if tab == "tab_starter":
        df = df_starter_N.copy()
    elif tab == "tab_meal":
        df = df_meal_N.copy()
    elif tab == "tab_dessert":
        df = df_dessert_N.copy()

    # input rate :
    if rate == "1":
        df = df[df["rate"] <= 3]
    elif rate == "2":
        df = df[df["rate"] > 3]
        df = df[df["rate"] <= 4]
    elif rate == "3":
        df = df[df["rate"] > 4]
    

    # input cost 
    if cost == "Assez cher":
        df = df[df["cost"] == "assez cher"]
    elif cost == "Coût moyen":
        df = df[df["cost"] == "Coût moyen"]
    elif cost == "bon marché":
        df = df[df["cost"] == "bon marché"]

    # input difficulty :
    if difficulty == "Niveau moyen":
        df = df[df["difficulty"] == "Niveau moyen"]
    elif difficulty == "Facile":
        df = df[df["difficulty"] == "facile"]
    elif difficulty == "Trés facile":
        df = df[df["difficulty"] == "très facile"]
    elif difficulty == "Difficile":
        df = df[df["difficulty"] == "difficile"]


    # input time : 
    df["time_preparation"] = df["time_preparation"].apply(lambda x: time_format(x))
    if time == "rapide":
        df = df[df["time_preparation"] <= 30]
    elif time == "moyen":
        df = df[df["time_preparation"] > 30]
        df = df[df["time_preparation"] <= 90 ]
    elif time == "long":
        df = df[df["time_preparation"] > 90]

    
    df = df.reset_index(drop=True)

    if tab != "tab_all":
        
  
        # récupération list ingrédients marmiton
        total_ingredients_ = ing_list(df_ingredients)

        # retraitements dataset :
        
        df["time_cooking"] = df["time_cooking"].apply(lambda x: time_format(x))
        df["total_time"] = df["total_time"].apply(lambda x: time_format(x))
        df["likes"] = df["likes"].apply(lambda x: likes(x))
        

        df['time_cooking'].fillna(0, inplace = True)
        df['total_time'].fillna(0,inplace=True)
        df['time_preparation'].fillna(0,inplace=True)

        l_ingre = []
        for item in range(len(df["ingredients"])):
            ingredients = df.loc[item,"ingredients"]
            l_ = ingredients_clean(ingredients, total_ingredients_)
            l_ingre.append(l_)

        columns_ = list(df.columns)
        columns_.append("ingredients_clean")  
        df = pd.concat([df, pd.DataFrame(l_ingre)], axis=1)
        print(df)   
        df.columns = columns_
        print(df.shape)
        
        
        # calcul des fréquences:
        keys = []
        nb_frequencies = []
        for key, value in freq_ingredients(total_ingredients(df)).most_common(20):
            keys.append(key) # on récupère la liste des mots
            nb_frequencies.append(value) # on récupère la liste des occurrences pour chaque mot

        fig = go.Figure()

        fig.add_trace(go.Bar(x=keys, y=nb_frequencies,
            marker_color = "darkred", # couleur des bins
            #xbins=dict(start=1.5, end=4.5), autobinx=False),
        ))


        fig.update_layout(
                title_text='Ingrédients les plus fréquents', # title of plot
                title_x = 0.5,  #centrage du titre
                xaxis_title_text='ingrédient', # xaxis label
                yaxis_title_text='distribution', # yaxis label
                bargap=0.05, # pour la taille de l'espace entre les bins  
                plot_bgcolor="#EBEDEF",# pour changer la couleur du background
                hovermode="x",
                width = 800,
                )

        return fig



