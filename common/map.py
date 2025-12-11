'''
Fichier pour comparer tous les aéroports d'une année
'''

import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_html

df = pd.read_csv('../data/2018-data.csv', sep=";")

aeroports = df['APT_NOM']
type(aeroports)
aeroports = aeroports.unique()
type(aeroports)

year = df['ANMOIS'].astype(str).str[:4].unique()[0]

airport_stats = df.groupby('APT_NOM').agg({
    'APT_PAX_dep': 'mean',
    'APT_PAX_arr': 'mean'
}).reset_index()

airport_stats.columns = ['APT_NOM', 'avg_dep', 'avg_arr']

trace = go.Scatter(
    x=airport_stats['avg_dep'],
    y=airport_stats['avg_arr'],
    mode='markers',
    name='Aéroports',
    text=airport_stats['APT_NOM'],
    hovertemplate="<b>%{text}</b><br>Au départ: %{x:.0f}<br>A l'arrivée: %{y:.0f}<extra></extra>",
    marker=dict(color='#1f77b4', size=8),
)

data = [trace]

layout = go.Layout(
    title=f"Moyenne des passagers au départ et à l'arrivée par aéroport en {year}",
    xaxis=dict(title='Passagers au départ (moyenne)', type='log'),
    yaxis=dict(title=f"Passagers à l'arrivée (moyenne)", type='log'),
    showlegend=True,
    legend=dict(x=0.01, y=0.99),
    hovermode="closest"
)

fig = go.Figure(data=data, layout=layout)

write_html(fig, file='fig.html', auto_open=False, include_plotlyjs='cdn')
