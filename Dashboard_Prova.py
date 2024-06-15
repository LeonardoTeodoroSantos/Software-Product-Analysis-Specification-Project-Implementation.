from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# ---------------------------------------------------------------------------------------------
# Reading dates
df = pd.read_excel("Estudos.xlsx", engine='openpyxl')

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
            ], style={}, md=1),
        dbc.Col([
            html.H5(children="Dados relacionados ao Estudo dos brasileiros")
        ], align="center", md=10, style={"color": "#A4A6A9"}),
    ], style={"margin-left": "50px", "margin-right": "50px"}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Button("BRASIL", color="primary",
                               size="sm",
                               id="location-button",
                               outline=True)
                    ], style={}, md=6),
                dbc.Col([
                    html.Div(id="div-test", children=[
                        dcc.Dropdown(opcoes,
                                     id="list_years",
                                     value=2022,
                                     style={"color": "#A4A6A9",
                                            "fontColor": "#A4A6A9"})
                    ])
                ], md=6)
            ], style={"margin-right": "33px"}),
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Ensino Infantil Público",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#62C462"},
                                id="Ens-infa"),
                        html.Span("Ensino Infantil Privado",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#EE5F5B"},
                                id="Ens-infa-pri"),
                        ])
                ], color="info",
                         outline=True,
                         style={"margin-top": "15px",
                                "box-shadow":
                                    "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], style={"margin-right": "45px"}),
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Ensino Fundamental Público",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#62C462"},
                                id="Ens-fun"),
                        html.Span("Ensino Fundamental Privado",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#EE5F5B"},
                                id="Ens-fun-pri"),
                        ])
                ], color="info",
                         outline=True,
                         style={"margin-top": "50px",
                                "box-shadow":
                                    "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], style={"margin-right": "45px"}),
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Ensino Médio Público",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#62C462"},
                                id="Ens-med"),
                        html.Span("Ensino Médio Privado",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#EE5F5B"},
                                id="Ens-med-pri"),
                        ])
                ], color="info",
                         outline=True,
                         style={"margin-top": "50px",
                                "box-shadow":
                                    "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], style={"margin-right": "45px"}),
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Ensino Superior Público",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#62C462"},
                                id="Ens-Sup"),
                        html.Span("Ensino Superior Privado",
                                  style={"color": "#A4A6A9"},
                                  className="card-text"),
                        html.H3(style={"color": "#EE5F5B"},
                                id="Ens-Sup-pri"),
                        ])
                ], color="info",
                         outline=True,
                         style={"margin-top": "50px",
                                "box-shadow":
                                    "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)"})
                ], style={"margin-right": "45px"}),
            ], md=3),
        dbc.Col([
            dbc.Row([
                dcc.Graph(id="bar-graph", figure=fig1)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="pie-graph", figure=fig2)
                ], md=6),
                dbc.Col([
                    dcc.Graph(id="line-graph", figure=fig3)
                ], md=6)
            ])
            ], md=9)
        ], style={"margin-left": "50px",
                  "margin-right": "50px",
                  "margin-top": "15px"})
], style={"height": "100vh"}, fluid=True)


# ---------------------------------------------------------------------------------------------
# callbacks
@app.callback(
    [
        Output("Ens-infa", "children"),
        Output("Ens-infa-pri", "children"),
        Output("Ens-fun", "children"),
        Output("Ens-fun-pri", "children"),
        Output("Ens-med", "children"),
        Output("Ens-med-pri", "children"),
        Output("Ens-Sup", "children"),
        Output("Ens-Sup-pri", "children"),
        ],
    [Input("list_years", "value"), Input("location-button", "children")]
)
def display_status(value, location):
    if location == "BRASIL":
        df_data_on_date = Bra[Bra["Data"] == value]
    else:
        df_data_on_date = Est[(Est["Estados"] == location) &
                              (Est["Data"] == value)]

    EnsInf = f"{(df_data_on_date['Ens Inf (Pública)'].values[0]):.1f}%"
    EnsInfPri = f"{(df_data_on_date['Ens Inf (Privada)'].values[0]):.1f}%"
    EnsFun = f"{(df_data_on_date['Ens fun (Pública)'].values[0]):.1f}%"
    EnsFunPri = f"{(df_data_on_date['Ens fun (Privada)'].values[0]):.1f}%"
    EnsMed = f"{(df_data_on_date['Ens méd (Pública)'].values[0]):.1f}%"
    EnsMedPri = f"{(df_data_on_date['Ens méd (Privada)'].values[0]):.1f}%"
    EnsSup = f"{(df_data_on_date['Ens sup (Pública)'].values[0]):.1f}%"
    EnsSupPri = f"{(df_data_on_date['Ens sup (Privada)'].values[0]):.1f}%"
    return (EnsInf,
            EnsInfPri,
            EnsFun,
            EnsFunPri,
            EnsMed,
            EnsMedPri,
            EnsSup,
            EnsSupPri
            )


@app.callback(
    Output("bar-graph", "figure"),
    [Input("list_years", "value")]
)
def update_graphline(value):
    df_data_on_states = Est[Est['Data'] == value]
    df_data_on_states = df_data_on_states.sort_values(
        by='No mínimo 12 anos de estudo (%)',
        ascending=False)

    fig1 = px.bar(df_data_on_states, x='Estados',
                  y='No mínimo 12 anos de estudo (%)')
    fig1.update_layout(
        showlegend=False,
        yaxis_ticksuffix='%',
        yaxis_tickformat=',.1f',
        xaxis_title=None,
        yaxis=dict(title="Mínimo 12 anos de estudo"),
        margin=dict(l=5, r=5, b=0, t=40),
        title=dict(text="Pessoas com pelo menos 12 anos de estudos (%)",
                   font=dict(size=20)),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font_color='#A4A6A9',
    )
    fig1.update_traces(marker_color='#5BC0DE')
    return fig1


@app.callback(
    Output("pie-graph", "figure"),
    [Input("list_years", "value"), Input("location-button", "children")]
)
def update_pie(value, location):
    if location == "BRASIL":
        graphpie = Bra[Bra['Data'] == value]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=graphpie["Sem instrução"],
                              x=graphpie['Brasil'],
                              name="Sem instrução",
                              marker_color="#5BC0DE"
                              )
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino fundamental incompleto"],
                              x=graphpie['Brasil'],
                              name="Ensino fundamental incompleto",
                              marker_color="#4D91AB")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino fundamental completo"],
                              x=graphpie['Brasil'],
                              name="Ensino fundamental completo",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino médio incompleto"],
                              x=graphpie['Brasil'],
                              name="Ensino médio incompleto",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino médio completo"],
                              x=graphpie['Brasil'],
                              name="Ensino médio completo",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino superior incompleto"],
                              x=graphpie['Brasil'],
                              name="Ensino superior incompleto",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino superior completo"],
                              x=graphpie['Brasil'],
                              name="Ensino superior completo",
                              marker_color="#ABCEDE")
                       )
        fig2.update_layout(
            title=dict(text="Nível de instrução", font=dict(size=20)),
            margin=dict(l=10, r=10, b=0, t=35),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#A4A6A9')
        return fig2
    else:
        graphpie = Est[(Est['Estados'] == location) & (Est['Data'] == value)]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=graphpie["Sem instrução"],
                              x=graphpie['Estados'],
                              name="Sem instrução",
                              marker_color="#5BC0DE"
                              )
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino fundamental incompleto"],
                              x=graphpie['Estados'],
                              name="Ensino fundamental incompleto",
                              marker_color="#4D91AB")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino fundamental completo"],
                              x=graphpie['Estados'],
                              name="Ensino fundamental completo",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino médio incompleto"],
                              x=graphpie['Estados'],
                              name="Ensino médio incompleto",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino médio completo"],
                              x=graphpie['Estados'],
                              name="Ensino médio completo",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino superior incompleto"],
                              x=graphpie['Estados'],
                              name="Ensino superior incompleto",
                              marker_color="#ABCEDE")
                       )
        fig2.add_trace(go.Bar(y=graphpie["Ensino superior completo"],
                              x=graphpie['Estados'],
                              name="Ensino superior completo",
                              marker_color="#ABCEDE")
                       )
        fig2.update_layout(
            title=dict(text="Nível de instrução", font=dict(size=20)),
            margin=dict(l=10, r=10, b=0, t=35),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#A4A6A9')
        return fig2


@app.callback(
    Output("line-graph", "figure"),
    [Input("list_years", "value"), Input("location-button", "children")]
)
def update_linegraph(value, location):
    if location == "BRASIL":
        df_on_line = Bra[Bra['Data'] == value]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(y=df_on_line['6 a 14 anos, no ensino fundamental'],
                              x=df_on_line['Brasil'],
                              name='6 a 14 anos, no fundamental',
                              marker_color="#ABCEDE"))
        fig3.add_trace(go.Bar(y=df_on_line['11 a 14 anos, nos anos finais do ensino fundamental'],
                              x=df_on_line['Brasil'],
                              name='11 a 14 anos, terminando fundamental',
                              marker_color="#40B5E0"))
        fig3.add_trace(go.Bar(y=df_on_line['15 a 17 anos, no ensino médio'],
                              x=df_on_line['Brasil'],
                              name='15 a 17 anos, no médio',
                              marker_color="#1888AD"))
        fig3.add_trace(go.Bar(y=df_on_line['18 a 24 anos, no ensino superior'],
                              x=df_on_line['Brasil'],
                              name='18 a 24 anos, no superior',
                              marker_color="#325E70"))
        fig3.update_layout(
            title=dict(text="Nível de instrução", font=dict(size=20)),
            margin=dict(l=10, r=10, b=0, t=35),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#A4A6A9',
            bargap=0.0,
            bargroupgap=0.10)
        return fig3
    else:
        df_on_line = Est[(Est['Estados'] == location) & (Est['Data'] == value)]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(y=df_on_line['6 a 14 anos, no ensino fundamental'],
                              x=df_on_line['Estados'],
                              name='6 a 14 anos, no fundamental',
                              marker_color="#ABCEDE"))
        fig3.add_trace(go.Bar(y=df_on_line['11 a 14 anos, nos anos finais do ensino fundamental'],
                              x=df_on_line['Estados'],
                              name='11 a 14 anos, terminando fundamental',
                              marker_color="#40B5E0"))
        fig3.add_trace(go.Bar(y=df_on_line['15 a 17 anos, no ensino médio'],
                              x=df_on_line['Estados'],
                              name='15 a 17 anos, no médio',
                              marker_color="#1888AD"))
        fig3.add_trace(go.Bar(y=df_on_line['18 a 24 anos, no ensino superior'],
                              x=df_on_line['Estados'],
                              name='18 a 24 anos, no superior',
                              marker_color="#325E70"))
        fig3.update_layout(
            title=dict(text="Nível de instrução", font=dict(size=20)),
            margin=dict(l=10, r=10, b=0, t=35),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#A4A6A9',
            bargap=0.0,
            bargroupgap=0.10)
        return fig3


@app.callback(
    Output("location-button", "children"),
    [Input("bar-graph", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["label"]
        return "{}".format(state)
    else:
        return "BRASIL"


if __name__ == '__main__':
    app.run(debug=True)
