'''
Fichier pour création de la map data
'''

import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_html

df = pd.read_csv('../data/2018-data.csv', sep=";")
type(df)

years = df['ANMOIS']
type(years)
years = years.unique()
type(years)

aeroports = df['APT_NOM']
type(aeroports)
aeroports = aeroports.unique()
type(aeroports)

# print(years)
# print(aeroports)

year = "201801"
aeroport = 'MAYOTTE-MARCEL HENRY'
test = df.query("APT_NOM=='MAYOTTE-MARCEL HENRY' and ANMOIS==201807")
type(test)

COLORS = {'Asia':'#1b9e77', 'Europe':'#d95f02', 'Africa':'#7570b3', 'MAYOTTE-MARCEL HENRY':'#e7298a', 'Oceania':'#66a61e' }

trace = go.Scatter( x=test['APT_PAX_dep'],
                    y=test['APT_PAX_arr'],
                    mode='markers' )

data = [trace]

layout = go.Layout(
    title=f"Passager en direction de {aeroport} ({year})",
    xaxis=dict(title='Passagers au départ (APT_PAX_dep)'),
    yaxis=dict(title="Passagers à l'arrivée (APT_PAX_arr)")
)

fig = go.Figure(data=data, layout=layout)

write_html(fig, file='fig.html', auto_open=False, include_plotlyjs='cdn')
