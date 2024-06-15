import dash
from dash import html, dcc, Input, Output
from dash import register_page, get_asset_url, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json

register_page(__name__, name="AC2", path='/pg2', external_stylesheets=[dbc.themes.YETI])

CENTER_LAT, CENTER_LON = -15.764401, -51.294193

# ---------------------------------------------------------------------------------------------
# Reading dates
df = pd.read_excel("Rend. per capita.xlsx", engine='openpyxl')

brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# ---------------------------------------------------------------------------------------------
# Criando varáveis para o df, Renda per Capita
PerCapitaBra = df
PerCapitaBra = PerCapitaBra.drop(['Regiões', 'Estados', 'UF'], axis=1)
PerCapitaBra = PerCapitaBra.dropna(axis=0)
PerCapitaBra['Data'] = PerCapitaBra['Data'].dt.year

PerCapitaEst = df
PerCapitaEst = PerCapitaEst.drop(['Regiões', 'Brasil'], axis=1)
PerCapitaEst = PerCapitaEst.dropna(axis=0)
PerCapitaEst['Data'] = PerCapitaEst['Data'].dt.year

# Criação de variáveis para Dropdown
# Criar um dropdown com Regiões do Brasil que mudam o "color" do graph-line
opcoes = list(PerCapitaEst['Data'].unique())

# ---------------------------------------------------------------------------------------------
# Criando as figs
fig1 = px.choropleth_mapbox(
    PerCapitaEst, locations="UF",
    color='Total_Médio',
    center={"lat": -16.95, "lon": -47.78},
    zoom=4,
    geojson=brazil_states,
    color_continuous_scale="Purples",
    opacity=0.4)
fig1.update_layout(
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
    )

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=PerCapitaBra['Data'],
                          y=PerCapitaBra['Total_Médio']))
fig2.update_layout(autosize=True,
                   margin=dict(l=10, r=10, t=10, b=10)
                   )

# ---------------------------------------------------------------------------------------------
# Layout HTML
layout = dbc.Container([
    # Row 1
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=get_asset_url("ibge.png"),
                         height=50),
                html.H5(
                    children="Dados do IBGE sobre Padrão de vida e Rendimentos"),
                dbc.Button("BRASIL", color="info", id="button-location",
                           size="lg")
                ], style={}),
            html.P("Selecione o ano desejado:", style={"margin-top": "15px"}),
            html.Div(id="div-test", children=[
                dcc.Dropdown(opcoes,
                             id='list_years',
                             optionHeight=25,
                             value=2022,
                             style={"width": "50%",
                                    "border": "0px solid black",
                                    "color": "#FFFFFF",
                                    }
                             )
                ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Renda per Capita sem auxílio",
                                      className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-s-auxilio"),
                            html.Span("Renda per Capita com auxílio",
                                      className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-c-auxilio"),
                        ])
                    ], color="info",
                             outline=True,
                             style={"background": "#D6E4E8",
                                    "margin-top": "5px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Renda média Homem", className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-homem"),
                            html.Span("Renda média Mulher", className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-mulher"),
                        ])
                    ], color="info",
                             outline=True,
                             style={"background": "#D6E4E8",
                                    "margin-top": "5px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Renda por raça (Branca)",
                                      className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-branca"),
                            html.Span("Renda por raça (Preta)",
                                      className="card-text"),
                            html.H3(style={"color": "#4682b4"},
                                    id="rend-preta"),
                        ])
                    ], color="info",
                             outline=True,
                             style={"background": "#D6E4E8",
                                    "margin-top": "5px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=4),
            ]),
            # Graph 1
            html.Div([
                html.P("Dados refente a Per Capita:",
                       style={"margin-top": "25px"}),
                dcc.Graph(id='line_graph', figure=fig2, className="graph-line")
                ]),
            ], md=6, style={"padding": "25px"}),
        dbc.Col([
            dcc.Loading(id="loading-1", type="default",
                        children=[dcc.Graph(
                            id='graph_map',
                            figure=fig1,
                            className="graph-map",
                            style={"height": "100vh", "margin-right": "5px"})
                                  ]
                        )
            ], md=6)
        ])
], fluid=True)

# ---------------------------------------------------------------------------------------------
# callbacks


@callback(
    [
        Output("rend-s-auxilio", "children"),
        Output("rend-c-auxilio", "children"),
        Output("rend-homem", "children"),
        Output("rend-mulher", "children"),
        Output("rend-branca", "children"),
        Output("rend-preta", "children"),
        ],
    [Input("list_years", "value"), Input("button-location", "children")]
)
def display_status(value, location):
    if location == "BRASIL":
        df_data_on_date = PerCapitaBra[PerCapitaBra["Data"] == value]
    else:
        df_data_on_date = PerCapitaEst[(PerCapitaEst["UF"] == location) &
                                       (PerCapitaEst["Data"] == value)]

    total_novo = f"R${(df_data_on_date['Total_Médio (Sbef)'].values[0]):,.2f}"

    homem_novo = f"R${(df_data_on_date['Total_Médio'].values[0]):,.2f}"

    media_homem = f"R${(df_data_on_date['Homem_Médio'].values[0]):,.2f}"

    media_mulher = f"R${(df_data_on_date['Mulher_Médio'].values[0]):,.2f}"

    raça_branca = f"R${(df_data_on_date['Branca_Médio'].values[0]):,.2f}"

    raça_preta = f"R${(df_data_on_date['Preta_Médio'].values[0]):,.2f}"
    return (total_novo,
            homem_novo,
            media_homem,
            media_mulher,
            raça_branca,
            raça_preta,)


@callback(Output("line_graph", "figure"),
          [Input("button-location", "children")])
def plot_line_graph(location):
    if location == "BRASIL":
        df_data_on_location = PerCapitaBra.copy()
    else:
        df_data_on_location = PerCapitaEst[PerCapitaEst['UF'] == location]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location["Homem_branco_Médio"],
                              name="Homem Branco"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Homem_preto_ou_pardo_Médio"],
                              name="Homem Preto ou Pardo"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location["Mulher_branca_Médio"],
                              name="Mulher Branca"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Mulher_preta_ou_parda_Médio"],
                              name="Mulher Preta ou Parda"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Homem_branco_Médio (Sbef)"],
                              name="Homem Branco (Sem Benefício)"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Homem_preto_ou_pardo_Médio (Sbef)"],
                              name="Homem Preto ou Pardo (Sem Benefício)"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Mulher_branca_Médio (Sbef)"],
                              name="Mulher Branca (Sem Benefício)"))
    fig2.add_trace(go.Scatter(x=df_data_on_location["Data"],
                              y=df_data_on_location[
                                  "Mulher_preta_ou_parda_Médio (Sbef)"],
                              name="Mulher Preta ou Parda (Sem Benefício)"))
    fig2.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        legend=dict(orientation="h"),
        yaxis_tickprefix='R$ ',
        yaxis_tickformat=',.2f',
        hovermode='x',
        paper_bgcolor="#D4DADC",
        plot_bgcolor="#D4DADC"
    ),
    fig2.update_yaxes(
        color="#050505",
        tickfont_size=12
        )
    fig2.update_xaxes(
        color="#050505",
        tickfont_size=12
    )
    return fig2


@callback(
    Output("graph_map", "figure"),
    [Input("list_years", "value")]
)
def update_map(value):
    df_data_on_states = PerCapitaEst[PerCapitaEst['Data'] == value]

    fig1 = px.choropleth_mapbox(
        df_data_on_states, locations="UF",
        color='Total_Médio',
        center={"lat": CENTER_LAT, "lon": CENTER_LON},
        zoom=3.8,
        geojson=brazil_states,
        color_continuous_scale="RdBu",
        range_color=[680, 3200],
        opacity=0.7,
        labels={"Total_Médio": "Per Capita Média"})
    fig1.update_layout(
        autosize=True,
        margin=go.layout.Margin(l=0, r=0, t=0, b=0),
        showlegend=False,
        mapbox_style='carto-positron',
        coloraxis_colorbar=dict(
            tickprefix="R$ ",
            tickformat=',.2f',
            title_font_color='#050505',
            title_font_size=15,
            tickfont=dict(color="#050505"),
            tickfont_size=12
        )
        )
    return fig1


@callback(
    Output("button-location", "children"),
    [Input("graph_map", "clickData"), Input("button-location", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "button-location.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    else:
        return "BRASIL"
