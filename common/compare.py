'''
Fichier pour comparer un même aéroport au cours des 4 années
'''

import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_html

df18 = pd.read_csv('../data/2018-data.csv', sep=";")
df19 = pd.read_csv('../data/2019-data.csv', sep=";")
df20 = pd.read_csv('../data/2020-data.csv', sep=";")
df21 = pd.read_csv('../data/2021-data.csv', sep=";")

df18['year'] = 2018
df19['year'] = 2019
df20['year'] = 2020
df21['year'] = 2021

df_all = pd.concat([df18, df19, df20, df21], ignore_index=True)

aeroport_name = 'PARIS-CHARLES DE GAULLE'  # Valeur de test. A modifier dynamiquement plus tard

data_aeroport = df_all[df_all['APT_NOM'] == aeroport_name]

colors = {2018: '#1b9e77', 2019: '#d95f02', 2020: '#7570b3', 2021: '#e7298a'}

traces = []
for year in [2018, 2019, 2020, 2021]:
    data_year = data_aeroport[data_aeroport['year'] == year].sort_values('ANMOIS')
    
    if len(data_year) > 0:
        trace = go.Scatter(
            x=data_year['ANMOIS'].astype(str).str[-2:].values,
            y=data_year['APT_PAX_dep'],
            mode='markers+lines',
            name=str(year),
            hovertemplate=f"<b>{year}</b><br>Mois: %{{x}}<br>Passagers: %{{y}}<extra></extra>",
            marker=dict(color=colors[year], size=10),
            line=dict(width=2)
        )
        traces.append(trace)

layout = go.Layout(
    title=f"Passagers au départ de {aeroport_name} (2018-2021)",
    xaxis=dict(title='Mois'),
    yaxis=dict(title="Passagers au départ"),
    showlegend=True,
    legend=dict(x=0.01, y=0.99),
    hovermode="x"
)

fig = go.Figure(data=traces, layout=layout)

write_html(fig, file='fig.html', auto_open=False, include_plotlyjs='cdn')

print(f"Graphique créé pour l'aéroport: {aeroport_name}")
