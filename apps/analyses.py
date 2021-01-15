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

df_starter_N = pd.read_csv("data/df_entrees.csv")
df_meal_N = pd.read_csv("data/df_plats.csv")
df_dessert_N = pd.read_csv("data/df_desserts.csv")

df_ingredients = pd.read_csv("data/df_ingredients.csv")


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


##### Creation static figure #######

## Comparison 

df_s = df_starter_N.copy()
df_m = df_meal_N.copy()
df_d = df_dessert_N.copy()

dff_s = get_df_to_figcomp(df_s)
dff_m = get_df_to_figcomp(df_m)
dff_d = get_df_to_figcomp(df_d)

figcomp = go.Figure(data=[
    go.Bar(name='Entrées/Apéritif', x=dff_s['theme'], y=dff_s['moy']),
    go.Bar(name='Plat', x=dff_m['theme'], y=dff_m['moy']),
    go.Bar(name='Dessert', x=dff_d['theme'], y=dff_d['moy'])
])

figcomp.update_layout(barmode='group',
                  title=
                  dict(text="Difficulté, Note et Coût moyen selon la catégorie",
                       font=dict(size=26)),
                  yaxis_title="Moyenne",
                  font=dict(size=16,color='black'),
                  legend=dict(
                      font=dict(size=20,color="black")))

##### Create layout #####

filters = html.Div(id = "block-filters", children = [
                    html.P('Note :', className = 'label-filter'),
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
                    html.P('Coût :', className = 'label-filter'),
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
                    html.P('Difficulté :', className = 'label-filter'),
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
                    html.P('Temps de préparation :', className = 'label-filter'),
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

title_1 = dbc.Jumbotron(className = 'title', children = 
        [
            html.H1("Quels ingrédients dans vos plats ?", className = "text-noel"),
        ]
)

title_2 = dbc.Jumbotron(className = 'title', children =
        [
            html.H1("La répartition des recettes de Noël !", className = "text-noel"),
        ]
    )

title_3 = dbc.Jumbotron(className = 'title', children =
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
            title_2,
            dbc.Row([
                dbc.Col(dcc.Graph(id = "graph_cost"), width={"size" : 5}),
                dbc.Col(dcc.Graph(id = "graph_diff"), width={"size" : 6}),
            ]),
            ]
        )
           
        ]
    ),
)



tab_all_content = dbc.Card(
    dbc.CardBody(
        [
           html.Div([
               html.H3('Comparaison selon la catégorie de recettes'),
               dcc.Graph(figure = figcomp)
           ]),
           html.Div([
               html.H3('Wordcloud des étapes de préparation selon le niveau de difficulté'),
               dbc.Row([
                   dbc.Col([html.P('Niveau très facile'),html.Img(src = "", alt = 'Image home', height = "300")]),
                   dbc.Col([html.P('Niveau facile'),html.Img(src = "", alt = 'Image home', height = "300")])
                   ]),
           ]),
               dbc.Row([
                   dbc.Col([html.P('Niveau moyen'),html.Img(src = "", alt = 'Image home', height = "300"),
                   dbc.Col([html.P('Niveau difficile'),html.Img(src = "", alt = 'Image home', height = "300")
                   ])
               ])
            ]),
        ]
    ))


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
    
    if tab != "tab_all":

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
        df.columns = columns_  
        
        # calcul des fréquences:
        keys = []
        nb_frequencies = []
        for key, value in freq_ingredients(total_ingredients(df)).most_common(20):
            keys.append(key) # on récupère la liste des mots
            nb_frequencies.append(value) # on récupère la liste des occurrences pour chaque mot

        fig = go.Figure()

        fig.add_trace(go.Bar(x=keys, y=nb_frequencies,
            marker_color = "darkred"
        ))


        fig.update_layout(
                title_text='Ingrédients les plus fréquents', # title of plot
                title_x = 0.5,  #centrage du titre
                xaxis_title_text='ingrédient', # xaxis label
                yaxis_title_text='distribution', # yaxis label
                bargap=0.07, # pour la taille de l'espace entre les bins  
                plot_bgcolor="#303030",
                paper_bgcolor='#262626',
                hovermode="x",
                width = 800,
                font=dict(color='white')
                )
        fig.update_traces(marker=dict(line=dict(width=0)))
        fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='grey')

        return fig


@app.callback(
    Output("graph_cost", "figure"), 
    [Input("card-tabs", "active_tab"),]
)
def display_graph_rep_cost(tab):
    if tab == "tab_starter":
        df = df_starter_N.copy()
    elif tab == "tab_meal":
        df = df_meal_N.copy()
    elif tab == "tab_dessert":
        df = df_dessert_N.copy()

    if tab != "tab_all":

        fig = px.histogram(df, x="cost", color_discrete_sequence=["darkred"] )


        fig.update_layout(
                title_text='Répartition des recettes selon le coût', # title of plot
                title_x = 0.5,  #centrage du titre
                xaxis_title_text='Coût', # xaxis label
                yaxis_title_text='Distribution', # yaxis label
                bargap=0.07, # pour la taille de l'espace entre les bins  
                plot_bgcolor="#303030",
                paper_bgcolor='#262626',# pour changer la couleur du background
                hovermode="x",
                width = 400,
                font=dict(color='white')
                )

        return fig

@app.callback(
    Output("graph_diff", "figure"), 
    [Input("card-tabs", "active_tab"),]
)
def display_graph_rep_diff(tab):
    if tab == "tab_starter":
        df = df_starter_N.copy()
    elif tab == "tab_meal":
        df = df_meal_N.copy()
    elif tab == "tab_dessert":
        df = df_dessert_N.copy()

    if tab != "tab_all":

        fig = px.histogram(df, x="difficulty", color_discrete_sequence=["darkred"])

        fig.update_layout(
        title_text='Répartion des recettes selon la difficulté', # title of plot
        title_x = 0.5,  #centrage du titre
        xaxis_title_text='Difficulté', # xaxis label
        yaxis_title_text='Distribution', # yaxis label
        plot_bgcolor="#303030",
        paper_bgcolor='#262626',# pour changer la couleur du background
        hovermode="x",
        width = 400,
        font=dict(color='white')
        )

        return fig

        

