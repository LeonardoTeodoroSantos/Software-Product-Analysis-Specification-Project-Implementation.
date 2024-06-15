from dash import Dash, html, dcc, Input, Output
from dash import callback, register_page, get_asset_url
import plotly.express as px
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

register_page(__name__, name="AC3", path='/pg3', external_stylesheets=[dbc.themes.YETI])

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
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo",
                         src=get_asset_url("ibge.png"),
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


@callback(
    [
        Output("esg-trat", "children"),
        Output("esg-n-trat", "children"),
        Output("lixo-cole", "children"),
        Output("lixo-n-cole", "children"),
        Output("agua-trat", "children"),
        Output("agua-n-trat", "children"),
        ],
    [Input("list_years", "value"), Input("location-button", "children")]
)
def display_status(value, location):
    if location == "BRASIL":
        df_data_on_date = Bra[Bra["Data"] == value]
    else:
        df_data_on_date = Est[(Est["Estados"] == location) &
                              (Est["Data"] == value)]

    esgtrat = f"{(df_data_on_date['esgoto trat pelo Estado'].values[0]):.1f}%"
    esgntrat = f"{(df_data_on_date['esgoto n trat pelo Estado'].values[0]):.1f}%"
    lixocole = f"{(df_data_on_date['Coletado diretamente por serviço de limpeza(lixo)'].values[0]):.1f}%"
    lixoncole = f"{(df_data_on_date['não coletado, queimado, enterrado etc(lixo)'].values[0]):.1f}%"
    aguatra = f"{(df_data_on_date['Rede geral de distribuição(agua)'].values[0]):.1f}%"
    aguantrata = f"{(df_data_on_date['Poços, fonte ou nascente / outra forma(agua)'].values[0]):.1f}%"
    return (esgtrat,
            esgntrat,
            lixocole,
            lixoncole,
            aguatra,
            aguantrata,
            )


@callback(
    Output("graph1-lg", "figure"),
    [Input("location-button", "children")]
)
def update_linegraph(location):
    if location == "BRASIL":
        df_on_line = Bra.copy()
    else:
        df_on_line = Est[Est['Estados'] == location]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=df_on_line['Telha sem laje de concreto'],
                              x=df_on_line['Data'],
                              mode="lines",
                              name='Telha sem laje de concreto',
                              legendgroup="group",
                              legendgrouptitle_text='Materiais dos telhados',
                              marker_color="#F04124"))
    fig1.add_trace(go.Scatter(y=df_on_line['Telha com laje de concreto'],
                              x=df_on_line['Data'],
                              mode="lines",
                              legendgroup="group",
                              name='Telha com laje de concreto',
                              marker_color="#F04124"))
    fig1.add_trace(go.Scatter(y=df_on_line['Somente laje de concreto'],
                              x=df_on_line['Data'],
                              mode="lines",
                              legendgroup="group",
                              name='Somente laje de concreto',
                              marker_color="#F04124"))
    fig1.add_trace(go.Scatter(
        y=df_on_line[
            '(Paredes Externas)Alvenaria ou taipa com revestimentos'],
        x=df_on_line['Data'],
        mode="lines",
        name='Alvenaria ou taipa revestidas',
        legendgroup="group2",
        legendgrouptitle_text='Materiais das paredes',
        marker_color="#43AC6A"
        ))
    fig1.add_trace(go.Scatter(y=df_on_line[
        '(Paredes Externas) Alvenaria sem revestimento'],
                              x=df_on_line['Data'],
                              mode="lines",
                              name='Alvenaria sem revestimentos',
                              legendgroup="group2",
                              marker_color="#43AC6A"))
    fig1.add_trace(go.Scatter(
        y=df_on_line[
            '(Paredes Externas) Madeira apropriada para construção (aparelhada)'],
        x=df_on_line['Data'],
        mode="lines",
        name='Madeira apropriada para construção',
        legendgroup="group2",
        marker_color="#43AC6A"))
    fig1.add_trace(go.Scatter(
        y=df_on_line[
            '(Paredes Externas) Outro material /  Madeira aproveitada / Taipa sem revestimento'],
        x=df_on_line['Data'],
        mode="lines",
        name='Outros materiais piores',
        legendgroup="group2",
        marker_color="#43AC6A"))
    fig1.add_trace(go.Scatter(
        y=df_on_line['Cerâmica, lajota ou pedra'],
        x=df_on_line['Data'],
        mode="lines",
        name='Cerâmica, lajota ou pedra',
        legendgroup="group3",
        legendgrouptitle_text='Materiais dos pisos',
        marker_color="#5BC0DE"))
    fig1.add_trace(go.Scatter(
        y=df_on_line['Madeira apropriada para construção (aparelhada)'],
        x=df_on_line['Data'],
        mode="lines",
        name='Madeira apropriada para construção',
        legendgroup="group3",
        marker_color="#5BC0DE"))
    fig1.add_trace(go.Scatter(
        y=df_on_line['Cimento'],
        x=df_on_line['Data'],
        mode="lines",
        name='Cimento',
        legendgroup="group3",
        marker_color="#5BC0DE"))
    fig1.add_trace(go.Scatter(
        y=df_on_line['Terra / Outro material'],
        x=df_on_line['Data'],
        mode="lines",
        name='Terra ou Outros materiais',
        legendgroup="group3",
        marker_color="#5BC0DE"))
    fig1.update_layout(
        margin=dict(l=10, r=10, b=0, t=10),
        legend=dict(orientation="h"),
        yaxis_ticksuffix='%',
        yaxis_tickformat=',.1f',
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font_color='#A4A6A9'
        )
    return fig1


@callback(
    Output("graph1-sm", "figure"),
    [Input("list_years", "value"), Input("location-button", "children")]
)
def update_barpolar(value, location):
    if location == "BRASIL":
        df_on_polar = Bra[Bra['Data'] == value]
    else:
        df_on_polar = Est[(Est['Estados'] == location) &
                          (Est['Data'] == value)]

    fig2 = go.Figure()
    fig2.add_trace(go.Barpolar(r=df_on_polar['Automóvel'],
                               theta=[140],
                               marker_color='#286F89',
                               name='Automóvel'
                               )
                   )
    fig2.add_trace(go.Barpolar(r=df_on_polar['Máquina de lavar roupa'],
                               theta=[198],
                               width=60,
                               marker_color='#4D91AB',
                               name='Máquina de lavar roupa'
                               )
                   )
    fig2.add_trace(go.Barpolar(r=df_on_polar['Telefone (fixo ou ao menos um celular)'],
                               theta=[255],
                               marker_color='#79B0C7',
                               name='Celular ou fixo'
                               )
                   )
    fig2.add_trace(go.Barpolar(r=df_on_polar['Geladeira'],
                               theta=[306],
                               marker_color='#ABCEDE',
                               name='Geladeira'
                               )
                   )
    fig2.add_trace(go.Barpolar(r=df_on_polar['Microcomputador'],
                               theta=[80],
                               marker_color='#0C4557',
                               name='Microcomputador'
                               )
                   )
    fig2.add_trace(go.Barpolar(r=df_on_polar['Motocicleta'],
                               theta=[10],
                               width=72,
                               marker_color='#04181E',
                               name='Motocicleta',
                               )
                   )
    fig2.update_layout(
        title="Bens adquiridos",
        polar=dict(
            radialaxis_angle=320,
            radialaxis=dict(range=[0, 100]),
            angularaxis=dict(showticklabels=False,
                             visible=True)
            ),
        polar_radialaxis_ticksuffix='%',
        polar_radialaxis_color="#000000",
        legend=dict(
                orientation="h"),
        paper_bgcolor="#FFFFFF",
        margin=dict(l=10, r=10, b=0, t=30),
        font_color='#A4A6A9',
        )
    return fig2


@callback(
    Output("graph2-lg", "figure"),
    [Input("list_years", "value")]
)
def update_graphauto(value):
    df_data_on_states = Est[Est['Data'] == value]
    df_data_on_states = df_data_on_states.sort_values(by='Automóvel',
                                                      ascending=False)

    fig3 = px.bar(df_data_on_states, x='Estados', y='Automóvel')
    fig3.update_layout(
        showlegend=False,
        yaxis_ticksuffix='%',
        yaxis_tickformat=',.1f',
        xaxis_title=None,
        yaxis=dict(title="Automóveis"),
        margin=dict(l=5, r=5, b=0, t=40),
        title=dict(text="Parte da população que têm automóvel",
                   font=dict(size=25)),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font_color='#A4A6A9',
    )
    fig3.update_traces(marker_color='#5BC0DE')
    return fig3


@callback(
    Output("graph2-sm", "figure"),
    [Input("list_years", "value"), Input("location-button", "children")]
)
def update_graph4(value, location):
    if location == "BRASIL":
        df3 = Bra[Bra['Data'] == value]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(y=df3["Até dois moradores por cômodo utilizado como dormitório"],
                              x=df3['Brasil'],
                              name="Até dois moradores por cômodo usado de dormitório",
                              marker_color="#5BC0DE"
                              )
                       )
        fig4.add_trace(go.Bar(y=df3["Até três moradores por banheiro de uso exclusivo"],
                              x=df3['Brasil'],
                              name="Até três moradores por banheiro de uso exclusivo",
                              marker_color="#4D91AB")
                       )
        fig4.add_trace(go.Bar(y=df3["Mais de dois cômodos não utilizados como dormitório ou banheiro"],
                              x=df3['Brasil'],
                              name="Mais de dois cômodos não usados de dormitório ou banheiro",
                              marker_color="#ABCEDE")
                       )
        fig4.update_layout(
            margin=dict(l=10, r=10, b=0, t=10),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#A4A6A9')
        return fig4
    else:
        df3 = Est[(Est['Estados'] == location) & (Est['Data'] == value)]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(y=df3["Até dois moradores por cômodo utilizado como dormitório"],
                              x=df3['Estados'],
                              name="Até dois moradores por cômodo usado de dormitório",
                              marker_color="#5BC0DE"
                              )
                       )
        fig4.add_trace(go.Bar(y=df3["Até três moradores por banheiro de uso exclusivo"],
                              x=df3['Estados'],
                              name="Até três moradores por banheiro de uso exclusivo",
                              marker_color="#4D91AB")
                       )
        fig4.add_trace(go.Bar(y=df3["Mais de dois cômodos não utilizados como dormitório ou banheiro"],
                              x=df3['Estados'],
                              name="Mais de dois cômodos não usados de dormitório ou banheiro",
                              marker_color="#ABCEDE")
                       )
        fig4.update_layout(
            margin=dict(l=10, r=10, b=0, t=10),
            legend=dict(orientation="h"),
            yaxis_ticksuffix='%',
            yaxis_tickformat=',.1f',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color='#000000'
        )
        return fig4


@callback(
    Output("graph-pie", "figure"),
    [Input("location-button", "children")]
)
def update_pie(location):
    if location == "BRASIL":
        df_data_on_location = Bra.copy()
    else:
        df_data_on_location = Est[Est["Estados"] == location]
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
            y=df_data_on_location['Próprio - já pago (Cond.Ocupa.)'],
            x=df_data_on_location['Data'],
            name="Imóvel próprio (já pago)",
            marker_color='#ABCEDE'
            ))
    fig5.add_trace(go.Bar(
            y=df_data_on_location['Alugado (Cond.Ocupa.)'],
            x=df_data_on_location['Data'],
            name="Imóvel alugado",
            marker_color='#40B5E0'
    ))
    fig5.add_trace(go.Bar(
            y=df_data_on_location['Outra Forma (soma)'],
            x=df_data_on_location['Data'],
            name="Outras formas",
            marker_color='#1888AD'
    ))
    fig5.add_trace(go.Bar(
            y=df_data_on_location['Próprio - pagando (Cond.Ocupa.)'],
            x=df_data_on_location['Data'],
            name="Imóvel Próprio (ainda pagando)",
            marker_color='#325E70'
    ))
    fig5.update_layout(
        yaxis=dict(title="", ticksuffix="%"),
        barmode='stack',
        autosize=False,
        margin=dict(l=0, r=0, b=50, t=0),
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font_color='#A4A6A9'
    )
    fig5.update_yaxes(
        color="#A4A6A9",
        tickfont_size=12
        )
    fig5.update_xaxes(
        color="#A4A6A9",
        tickfont_size=12
    )
    return fig5


@callback(
    Output("graph-bar-inv", "figure"),
    [Input("list_years", "value")]
)
def update_map(value):
    df_data_on_states = Est[Est['Data'] == value]
    df_data_on_states = df_data_on_states.sort_values(by='Acesso à Internet')

    fig6 = px.bar(df_data_on_states, x='Acesso à Internet',
                  y='Estados', orientation='h')
    fig6.update_layout(
        showlegend=False,
        yaxis_title=None,
        xaxis=dict(title="", ticksuffix="%", tickmode='array',
                   tickvals=[0, 25, 50, 75, 100]),
        margin=dict(l=0, r=0, b=0, t=40),
        title=dict(text="Acesso à Internet", font=dict(size=25)),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font_color='#A4A6A9',
    )
    fig6.update_traces(marker_color='#5BC0DE')
    return fig6


@callback(
    Output("location-button", "children"),
    [Input("graph-bar-inv", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["label"]
        return "{}".format(state)
    else:
        return "BRASIL"
