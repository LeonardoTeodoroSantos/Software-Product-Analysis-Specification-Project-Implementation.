from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# ---------------------------------------------------------------------------------------------
# Reading dates
df = pd.read_excel("CondMoradia.xlsx", engine='openpyxl')

# ---------------------------------------------------------------------------------------------
# Criando varáveis para o df
Bra = df
Bra = Bra.drop(["Regiões", "Estados"], axis=1)
Bra = Bra.dropna(axis=0)
Bra['Data'] = Bra['Data'].dt.year

Reg = df
Reg = Reg.drop(["Brasil", "Estados"], axis=1)
Reg = Reg.dropna(axis=0)
Reg['Data'] = Reg['Data'].dt.year

Est = df
Est = Est.drop(["Brasil", "Regiões"], axis=1)
Est = Est.dropna(axis=0)
Est['Data'] = Est['Data'].dt.year

# Criação de variáveis para Dropdown
# Criar um dropdown com Regiões do Brasil que mudam o "color" do graph-line
opcoes = list(Est['Data'].unique())

# ---------------------------------------------------------------------------------------------
# Criando as figs
fig1 = go.Figure()
fig2 = go.Figure()
fig3 = go.Figure()
fig4 = go.Figure()
fig5 = go.Figure()
fig6 = go.Figure()

# ---------------------------------------------------------------------------------------------
# Layout HTML
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo",
                         src=app.get_asset_url("ibge.png"),
                         height=50,
                         style={}
                         )
                ])
            ], align="center", style={"margin-left": "25px"}),
        dbc.Col([
            html.H5(children="Dados relacionados a moradia dos brasileiros")
        ], align="center", md=8, style={"color": "#A4A6A9"}),
        dbc.Col([
            dbc.Row([
                html.P("Selecione o ano desejado:",
                       style={"margin-bottom": "0px",
                              "margin-top": "10px",
                              "color": "#A4A6A9"},
                       )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id="div-test", children=[
                        dcc.Dropdown(opcoes, id="list_years",
                                     value=2022, style={"color": "#A4A6A9",
                                                        "fontColor": "#A4A6A9"})
                        ]),
                ]),
                dbc.Col([
                    dbc.Button("BRASIL", color="primary",
                               size="sm",
                               id="location-button",
                               outline=True)
                ])
            ], style={"margin-top": "0px"})
        ], md=3, style={})
    ], style={"margin-left": "50px", "margin-right": "50px"}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Esgoto tratado pelo Estado",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#62C462"},
                                    id="esg-trat"),
                            html.Span("Sem esgoto tratado pelo Estado",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#EE5F5B"},
                                    id="esg-n-trat"),
                            ])
                        ], color="info",
                             outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow":
                                        "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                    ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Lixo coletado devidamente",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#62C462"},
                                    id="lixo-cole"),
                            html.Span("Não coletado, queimado, enterrado etc",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#EE5F5B"},
                                    id="lixo-n-cole"),
                            ])
                        ], color="success",
                             outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow":
                                        "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                    ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Água por Rede geral de distribuição",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#62C462"},
                                    id="agua-trat"),
                            html.Span("Poços, fonte ou nascente / outra forma",
                                      style={"color": "#A4A6A9"},
                                      className="card-text"),
                            html.H3(style={"color": "#EE5F5B"},
                                    id="agua-n-trat"),
                            ])
                        ], color="warning",
                             outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow":
                                        "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                    ]),
                ], style={"margin-left": "50px"}),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="graph1-lg",
                              figure=fig1,
                              style={"box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=8),
                dbc.Col([
                    dcc.Graph(id="graph1-sm",
                              figure=fig2,
                              style={"box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=4)
                ], style={"margin-left": "50px",
                          "margin-top": "20px"}),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="graph2-lg",
                              figure=fig3,
                              style={"box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=8),
                dbc.Col([
                    dcc.Graph(id="graph2-sm",
                              figure=fig4,
                              style={"box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], md=4)
                ], style={"margin-top": "20px",
                          "margin-left": "50px",
                          "margin-bottom": "50px"})
        ]),
        dbc.Col([
            dbc.Row([
                dcc.Graph(id="graph-pie",
                          figure=fig5,
                          style={"height": "30hv",
                                 "margin-top": "10px",
                                 "margin-bottom": "0px"})
            ]),
            dbc.Row([
                dcc.Graph(id="graph-bar-inv",
                          figure=fig6,
                          style={"height": "655px"})
            ])
        ], style={"margin-right": "50px"}, md=3)
    ])
], fluid=True)


# ---------------------------------------------------------------------------------------------
# callbacks


if __name__ == '__main__':
    app.run(debug=True)
