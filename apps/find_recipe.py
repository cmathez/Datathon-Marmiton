## Page with recommandation algorithm

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

    # To maniplutate data
import random
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

df_ing = pd.read_csv("data/df_ingredients.csv")


filters = html.Div(id = "block-filters", children = [
                    html.P('Catégories :'),
                    dbc.RadioItems(         # to create filter (by day, week, month, year)
                        id='category',
                        options=[{'label': i, 'value': i} for i in ['Entrées/Apéritifs', 'Plats', 'Desserts','']],
                        value='',
                        inline=True,
                        ),
                    html.Hr(),
                    html.P('Ingredients :'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="ingredient1", value="", type="text")
                        ]),
                        dbc.Col([
                            dbc.Input(id="ingredient2", value="", type="text")
                        ]),
                        dbc.Col([
                            dbc.Input(id="ingredient3", value="", type="text")
                        ])
                    ]),
                    html.Hr(),
                    html.P('Nombre de personnes :'),
                    dbc.Input(id="nbpers", value="", type="text"),
                    html.Hr(),
                    html.P('Coût :'),
                    dbc.RadioItems(         
                        id='cout',
                        options=[{'label': i, 'value': i} for i in ['€', '€€', '€€€','']],
                        value='',
                        inline=True,),
                        html.Hr(),
                    html.P('Difficulté :'),
                    dbc.RadioItems(         
                        id='difficulty',
                        options=[{'label': i, 'value': i} for i in ['Très facile', 'Facile', 'Moyen','Difficile','']],
                        value='',
                        inline=True,),
                        html.Hr(),
                    html.P('Temps de préparation :'),
                    dcc.Slider(
                        id = "time",
                        min=0,
                        max=120,
                        step=None,
                        marks={
                            0: '',
                            15: '15 min',
                            30: '30 min',
                            45: '45 min',
                            60: '1h',
                            90: '1h30',
                            120 :'> 2h',
                        },
                        value=15
                    )  
                    ]
                )

tab_filter_content = dbc.Card(
    dbc.CardBody(
        [
           filters,
           html.Br(),
           html.Div(id='reco_filter'),
        ]
    )
           

    )

tab_original_content = dbc.Card(
    dbc.CardBody(
        [

        dbc.Select(
            id="lunch_time",
            options=[
                {"label": "Entrées/Apéritifs", "value": "Entrées/Apéritifs"},
                {"label": "Plats", "value": "Plats"},
                {"label": "Desserts", "value": "Desserts"},
        ],
        value = "Entrées/Apéritifs"
),
           html.Br(),
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
def get_recommandation_text(value):
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

@app.callback(Output("reco-original", "children"), [Input("lunch_time", "value")])
def get_recommandation_ori(value):
    total_ingredients_=ing_list(df_ing)

    if value == "Entrées/Apéritifs":
        dff=df_recipe_N[df_recipe_N['category']=='aperitif/starter'].copy()
        

    elif value == "Plats":
        dff=df_recipe_N[df_recipe_N['category']=='meal'].copy()
        
    elif value == "Desserts":
        dff=df_recipe_N[df_recipe_N['category']=='dessert'].copy()
        
    print(dff)
    dff["time_cooking"] = dff["time_cooking"].apply(lambda x: time_format(x))
    dff["total_time"] = dff["total_time"].apply(lambda x: time_format(x))
    dff["likes"] = dff["likes"].apply(lambda x: likes(x))
    

    dff['time_cooking'].fillna(0, inplace = True)
    dff['total_time'].fillna(0,inplace=True)
    dff['time_preparation'].fillna(0,inplace=True)
    
    l_ingre = []
    for item in range(len(dff["ingredients"])):
        ingredients = dff.loc[item,"ingredients"]
        l_ = ingredients_clean(ingredients, total_ingredients_)
        l_ingre.append(l_)

    columns_ = list(dff.columns)
    columns_.append("ingredients_clean")  
    dff = pd.concat([dff, pd.DataFrame(l_ingre)], axis=1)
    dff.columns = columns_  

    dico=freq_ingredients(total_ingredients(dff))
    #df_ori =

    l_ind=[(v,k) for k,v in dico.items()]

    l_ind=sorted(l_ind)

    freq=list(set([l_ind[i][0] for i in range(len(l_ind))]))

    freq_min=freq[:2]
    ing = [k for k,v in dico.items() if v in freq_min]

    l_ing = random.sample(ing,10)

    l_ind=[]

    for ing in l_ing :
        for i in range(len(dff)):
            if ing in dff.loc[i,'ingredients_clean']:
                l_ind.append(i)

    df_audacieux = dff[dff.index.isin(l_ind)]

    df_audacieux=df_audacieux[df_audacieux['rate']>=4].reset_index(drop=True)

    c_ind=random.sample(range(0,len(df_audacieux)),3)

    df_ori= df_audacieux[df_audacieux.index.isin(c_ind)].reset_index(drop = True).head(3)
    print(df_ori)

    ori_layout = html.Div(
        dbc.Row([
            dbc.Col([
                dbc.NavLink(df_ori.loc[0,'title'], className = 'display-reco', active=True, href=df_ori.loc[0,'links'], external_link=True,),
                html.Hr(),
                html.P(f"Note {df_ori.loc[0,'rate']} | Likes {df_ori.loc[0,'likes']} | Pour {df_ori.loc[0,'number people']} personnes")

            ]),

            dbc.Col([
                dbc.NavLink(df_ori.loc[1,'title'], className = 'display-reco', active=True, href=df_ori.loc[1,'links'], external_link=True,),
                html.Hr(),
                html.P(f"Note {df_ori.loc[1,'rate']} | Likes {df_ori.loc[1,'likes']} | Pour {df_ori.loc[1,'number people']} personnes")


            ]),

            dbc.Col([
                dbc.NavLink(df_ori.loc[2,'title'], className = 'display-reco', active=True, href=df_ori.loc[2,'links'], external_link=True,),
                html.Hr(),
                html.P(f"Note {df_ori.loc[2,'rate']} | Likes {df_ori.loc[2,'likes']} | Pour {df_ori.loc[2,'number people']} personnes")


            ])
        ])
    )
    return ori_layout



@app.callback(Output("reco_filter", "children"), 
[Input("category", "value"),
Input("ingredient1", "value"),
Input("ingredient2", "value"),
Input("ingredient2", "value"),
Input("nbpers", "value"),
Input("cout", "value"),
Input("difficulty", "value"),
Input("time", "value")])
def get_reco_filter(cat, ing1, ing2, ing3, nb, cost, diff, time):
    

    dff = df_recipes_N.copy()
    dff['time_preparation'] = dff['time_preparation'].apply(lambda x : time_format(x))
    dff['number people'] = dff['number people'].apply(lambda x : 0 if x=='no data' else int(x))
    if ing1 != "":
        ing1=ing1.lower()
        dff= dff[dff['ingredients'].str.contains(ing1)].reset_index(drop=True)
    

    if ing2 != "":
        ing2=ing2.lower()
        dff= dff[dff['ingredients'].str.contains(ing2)].reset_index(drop=True)
    
    if ing3 != "":
        ing3=ing3.lower()
        dff=dff[dff['ingredients'].str.contains(ing3)].reset_index(drop=True)

    
    if nb!='':
        nb_pers=int(nb)
        dff=dff[dff['number people']>=nb_pers].reset_index(drop=True)

    if cost!='':
        dff=dff[dff['cost']==cost].reset_index(drop=True)

    if diff !='':
        dff[dff['difficulty']==diff].reset_index(drop=True)

    if cat!='':
        dff=dff[dff['category']==cat].reset_index(drop=True)

    if time!='':
        time=int(time)
        dff=dff[dff['time_preparation']<=time].reset_index(drop=True)


    df_filter=dff.sort_values(by='rate', ascending=False).reset_index(drop = True).head(3)


    if len(df_filter)==0:
        return html.P("pas de recette trouvée!")
    else:
        filter_layout = html.Div(
                    dbc.Row([
                        dbc.Col([
                            dbc.NavLink(df_filter.loc[0,'title'], className = 'display-reco', active=True, href=df_filter.loc[0,'links'], external_link=True,),
                            html.Hr(),
                            html.P(f"Note {df_filter.loc[0,'rate']} | Likes {df_filter.loc[0,'likes']} | Pour {df_filter.loc[0,'number people']} personnes")

                        ]),

                        dbc.Col([
                            dbc.NavLink(df_filter.loc[1,'title'], className = 'display-reco', active=True, href=df_filter.loc[1,'links'], external_link=True,),
                            html.Hr(),
                            html.P(f"Note {df_filter.loc[1,'rate']} | Likes {df_filter.loc[1,'likes']} | Pour {df_filter.loc[1,'number people']} personnes")


                        ]),

                        dbc.Col([
                            dbc.NavLink(df_filter.loc[2,'title'], className = 'display-reco', active=True, href=df_filter.loc[2,'links'], external_link=True,),
                            html.Hr(),
                            html.P(f"Note {df_filter.loc[2,'rate']} | Likes {df_filter.loc[2,'likes']} | Pour {df_filter.loc[2,'number people']} personnes")


                        ])
                    ])
                )
        return filter_layout

    
    
        
