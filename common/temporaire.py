'''
Fichier pour comparer des aéroports
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
# count = 0
# for aeroport in aeroports:
#     count += 1
#     print(f"{count} - {aeroport}")

aeroport = 'MAYOTTE-MARCEL HENRY'
test = df.query("APT_NOM=='MAYOTTE-MARCEL HENRY'")
type(test)

aeroport1 = 'LA REUNION-ROLAND GARROS'
test1 = df.query("APT_NOM=='LA REUNION-ROLAND GARROS'")
type(test1)

aeroport2 = 'ST-PIERRE-PIERREFONDS'
test2 = df.query("APT_NOM=='ST-PIERRE-PIERREFONDS'")
type(test2)

aeroport3 = 'LA ROCHELLE-ILE DE RE'
test3 = df.query("APT_NOM=='LA ROCHELLE-ILE DE RE'")
type(test3)

year = test['ANMOIS'].astype(str).str[:4].unique()

COLORS = {'LA REUNION-ROLAND GARROS':'#1b9e77', 'ST-PIERRE-PIERREFONDS':'#d95f02', 'LA ROCHELLE-ILE DE RE':'#7570b3', 
          'MAYOTTE-MARCEL HENRY':'#e7298a', "NICE-COTE D'AZUR":'#66a61e'}

trace = go.Scatter( x=test['ANMOIS'].astype(str).str[-2:].values,
                    y=test['APT_PAX_dep'], 
                    mode='markers+lines', 
                    name=aeroport,
                    hovertemplate=f"<b>{aeroport}</b><br>Mois: %{{x}}<br>Passagers: %{{y}}<extra></extra>",
                    marker=dict(color=COLORS[aeroport], size=10)
                )

trace1 = go.Scatter( x=test1['ANMOIS'].astype(str).str[-2:].values,
                    y=test1['APT_PAX_dep'], 
                    mode='markers+lines', 
                    name=aeroport1,
                    hovertemplate=f"<b>{aeroport1}</b><br>Mois: %{{x}}<br>Passagers: %{{y}}<extra></extra>",
                    marker=dict(color=COLORS[aeroport1], size=10)
                )

trace2 = go.Scatter( x=test2['ANMOIS'].astype(str).str[-2:].values,
                    y=test2['APT_PAX_dep'], 
                    mode='markers+lines', 
                    name=aeroport2,
                    hovertemplate=f"<b>{aeroport2}</b><br>Mois: %{{x}}<br>Passagers: %{{y}}<extra></extra>",
                    marker=dict(color=COLORS[aeroport2], size=10)
                )

trace3 = go.Scatter( x=test3['ANMOIS'].astype(str).str[-2:].values,
                    y=test3['APT_PAX_dep'], 
                    mode='markers+lines', 
                    name=aeroport3,
                    hovertemplate=f"<b>{aeroport3}</b><br>Mois: %{{x}}<br>Passagers: %{{y}}<extra></extra>",
                    marker=dict(color=COLORS[aeroport3], size=10)
                )

data = [trace, trace1, trace2, trace3]

layout = go.Layout(
    title=f"Passagers au départ des aéroports en {year[0]}",
    xaxis=dict(title='Mois(ANMOIS)'),
    yaxis=dict(title="Passagers au départ de l'aeroport"),
    showlegend=True,
    legend=dict(x=0.01, y=0.99)
)

fig = go.Figure(data=data, layout=layout)

fig.update_layout(hovermode="x")

write_html(fig, file='fig.html', auto_open=False, include_plotlyjs='cdn')
