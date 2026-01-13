from dash import Dash, html

def creation_app_dash(srv_Flask):
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/map/", suppress_callback_exceptions=True)

    header = html.Div(className = 'header', 
    children = [
    html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
    html.H1("Map", className = "titre_header_accueil")
    ])

    app_Dash.layout =  html.Div([
    html.Link(rel="stylesheet", href="/static/css/index.css"),
    header
    ])