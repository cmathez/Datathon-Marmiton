## Application Dash for Datathon 
## A delicious cooking recipes analyses
## Foulon Tatiana, Mathez Céline, Santa-Maria Clara
## Data Analyst Wild Code School Bordeaux 
## 01-13-2020 to 01-15-2021



### Import ###

## app.py : create app variable 

import dash
import dash_bootstrap_components as dbc



### Create Dash App ###

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY]) 

server = app.server
