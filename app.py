import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import analyses, find_recipe, trend
from dash import app

### Create Dash architecture ###


          
jumbotron = dbc.Jumbotron(
    [
        dbc.Row(
                [
                    dbc.Col(
                            html.Img(src = "https://www.cuisinevault.com/wp-content/uploads/2018/12/Christmas-Cooking-Guide.jpg", alt = 'Image home', height = "300")
                                
                        ),
                    dbc.Col([html.H1("Les recettes de Noël en graphiques", className="display-3")
                ],
                align="center",
            ),
        html.Hr(className="my-2"),
        #html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ]
), 
])

nav = dbc.Nav( className = 'nav', children = [   
    
        dbc.NavLink("Analyses de Noël", className = 'item', active=True, href="/analyses", external_link=True,),
        dbc.NavLink("Tendance de Noël", className = 'item',  href="/trend", external_link=True,),
        dbc.NavLink("Trouve ton repas de Noël", className = 'item',  href="/find_recipe", external_link=True,),
   ],
    vertical="md",
)





content = html.Div(id="page-content")

app.layout = html.Div([
                html.Div([
                        jumbotron,
                    html.Div([

                    dbc.Row([
                        dbc.Col(id='col-left',children = [dcc.Location(id='url'), nav], width = 1.5),
                        dbc.Col([content], width={"size" : 9})],
                        justify="start",
                        
                    ),
        ]),
]),
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):

    if pathname == "/analyses" or pathname == "/":
        return analyses.layout
    if pathname == "/trend":
        return trend.layout
    if pathname == "/find_recipe":
        return find_recipe.layout

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
