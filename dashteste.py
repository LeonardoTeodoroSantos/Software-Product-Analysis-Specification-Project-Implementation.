from dash import Dash, html, dcc, Input, Output, callback
from dash_bootstrap_templates import ThemeSwitchAIO
import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Styles
url_theme2 = dbc.themes.FLATLY
url_theme1 = dbc.themes.DARKLY
template_theme2 = 'flatly'
template_theme1 = 'darkly'

# Reading dates
df2 = pd.read_excel('Regiões.xlsx', engine='openpyxl')
df3 = pd.read_excel('CargoOcupadoEmPorcentagem.xlsx', engine='openpyxl')

# tratamento da coluna 'Ano' com somente o ano desta data.
df2['Ano'] = df2['ano'].dt.year
df2.drop('ano', axis=1, inplace=True)

# tratamento de algumas colunas para numeros inteiros.
df2['População em idade de trabalhar'] = df2[
    'População em idade de trabalhar\n(1 000 pessoas)'].astype(int)
df2['População na força de trabalho'] = df2[
    'População na força de trabalho\n(1 000 pessoas)'].astype(int)
df2['População ocupada'] = df2[
    'População ocupada\n(1 000 pessoas)'].astype(int)
df2['População ocupada em trabalhos formais'] = df2[
    'População ocupada em trabalhos formais (1)\n(1 000 pessoas)'].astype(int)
df2['População desocupada'] = df2[
    'População desocupada\n(1 000 pessoas)'].astype(int)
df2['População na força de trabalho potencial'] = df2[
    'População na força de trabalho potencial\n(1 000 pessoas)'].astype(int)
df2['População subutilizada'] = df2[
    'População subutilizada\n(1 000 pessoas)'].astype(int)
df2 = df2.drop(
    ['População em idade de trabalhar\n(1 000 pessoas)',
     'População na força de trabalho\n(1 000 pessoas)',
     'População ocupada\n(1 000 pessoas)',
     'População ocupada em trabalhos formais (1)\n(1 000 pessoas)',
     'População desocupada\n(1 000 pessoas)',
     'População na força de trabalho potencial\n(1 000 pessoas)',
     'População subutilizada\n(1 000 pessoas)'], axis=1)

# Tratando os dados do "df3"
df3.dropna(how='all', inplace=True)
df3['Ano'] = df3['Ano'].dt.year
df3.drop('coeficiente', axis=1, inplace=True)
# pd.options.display.float_format = '{:.2f}'.format
# pd.set_option('display.precision', 2)
# A variavel "reg" é a tabela nova, com "regiões" tratadas
reg = df3.loc[(df3['Regiões'] == 'Norte') | (df3['Regiões'] == 'Nordeste')
              | (df3['Regiões'] == 'Sudeste') | (df3['Regiões'] == 'Sul')
              | (df3['Regiões'] == 'Centro-Oeste')
              ]
reg = reg.drop(['Estados', 'Total_Brasil', 'Total'], axis=1)
pd.options.display.float_format = '{:.2f}'.format

# Criação da variavel "est" para representar os estados com dados já tratados
est = df3
est = est.dropna(subset=['Estados'])
est = est.drop(['Regiões', 'Total_Brasil', 'Total'], axis=1)

# Criando a variavel "bra", para representar os valores do Brasil
bra = df3
bra = bra.dropna(subset='Total_Brasil')
bra = bra.drop(['Regiões', 'Estados', 'Total'], axis=1)

# Criação de variáveis

opcoes = list(df2['Ano'].unique())
opcoes.append('Todos os anos')

fig2 = px.bar_polar(
        df2, r="População ocupada",
        theta="Regiões",
        color="Regiões",)
fig2.update_layout(
    polar_angularaxis_ticktext=[
        'Nordeste', 'Norte', 'Centro-Oeste', 'Sudeste', 'Sul'])

fig3 = px.bar(df2, x='Regiões',
              y='População desocupada',
              color="Regiões",
              title='População Desocupada')

fig4 = px.bar(reg, x='Regiões',
              y=['Empregado com carteira de trabalho assinada',
                 'Empregado sem carteira de trabalho assinada',
                 'Militar ou funcionário público estatutário',
                 'Conta própria', 'Empregador',
                 'Outros'])


# Função para fazer o grafico
def est_bar():
    df5 = df3.groupby('Regiões').sum().reset_index()
    fig = px.bar(df5,
                 y="Empregado com carteira de trabalho assinada",
                 x="Regiões",
                 color='Regiões',
                 barmode="relative")
    fig.update_layout(
        title='Carteira de trabalho assinada por região')
    return fig


app.layout = dbc.Container([
    # Row 1
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
            html.H3('Dados do IBGE'),
            dcc.Dropdown(
                opcoes, value=2022, id='list_years',
                className="botton year"
                )
        ], sm=8, md=12)
    ]),
    # Row 2
    dbc.Row([
        dbc.Col([
            # Graph 1
            dcc.Graph(
                id='grafico_todos_anos',
                figure=fig2,
                className="graph-dash"
            )
        ], sm=10, md=6),
        dbc.Col([
            # Graph 2
            dcc.Graph(
                id='graph4_reg',
                figure=fig4,
                className='graph-dash2',
            )
        ], sm=10, md=6),
        # Row 3
        dbc.Row([
            dbc.Col([
                # Graph 3
                dcc.Graph(
                    id='grafico_sexo',
                    figure=fig3,
                    className="graph-dash3"
                    )
            ], sm=10, md=6),
            dbc.Col([
                dbc.Card([
                    dbc.Button('🡠',
                               id='back-button',
                               outline=True, size="sm",
                               className='button-int',
                               style={'display': 'none'}),
                    dbc.Col(
                        dcc.Graph(id='graph', figure=est_bar(),
                                  className='graph-dash4'))
                ])
            ], sm=10, md=6)
        ])
    ])
])


@callback(
    Output('graph', 'figure'),
    Output('back-button', 'style'),    # to hide/unhide the back button
    Input('graph', 'clickData'),    # for getting the vendor name from graph
    Input('back-button', 'n_clicks'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def drilldown(click_data, n_clicks, toggle):
    template = template_theme1 if toggle else template_theme2
    # usando o contexto de callback para verificar qual entrada foi disparada
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == 'graph':
        # obter o nome do vendor em clickData
        if click_data is not None:
            vendor = click_data['points'][0]['label']
            if vendor in df3.Regiões.unique():
                # criando df para vendor clicado
                # vendor_sales_df = df3[df3['Regiões'] == vendor]
                # gerando gráfico de barras de vendas de produtos
                if vendor == 'Norte':
                    est_tra = df3.loc[(df3['Estados'] == 'Rondônia')
                                      | (df3['Estados'] == 'Acre')
                                      | (df3['Estados'] == 'Amazonas')
                                      | (df3['Estados'] == 'Roraima')
                                      | (df3['Estados'] == 'Pará')
                                      | (df3['Estados'] == 'Amapá')
                                      | (df3['Estados'] == 'Tocantins')]
                    fig = px.line(
                        est_tra,
                        x='Ano',
                        y="Empregado com carteira de trabalho assinada",
                        color='Estados', template=template)
                    fig.update_layout(
                        title='<b>Carteira de trabalho assinada no {}<b>'
                        .format(vendor)),
                    return fig, {'display': 'block'}
                if vendor == 'Nordeste':
                    est_tra = df3.loc[(df3['Estados'] == 'Maranhão')
                                      | (df3['Estados'] == 'Piauí')
                                      | (df3['Estados'] == 'Ceará')
                                      | (df3[
                                          'Estados'] == 'Rio Grande do Norte')
                                      | (df3['Estados'] == 'Paraíba')
                                      | (df3['Estados'] == 'Pernambuco')
                                      | (df3['Estados'] == 'Alagoas')
                                      | (df3['Estados'] == 'Sergipe')
                                      | (df3['Estados'] == 'Bahia')]
                    fig = px.line(
                        est_tra,
                        x='Ano',
                        y='Empregado com carteira de trabalho assinada',
                        color='Estados', template=template)
                    fig.update_layout(
                            title='<b>Carteira de trabalho assinada no {}<b>'
                            .format(vendor))
                    return fig, {'display': 'block'}
                if vendor == 'Centro-Oeste':
                    est_tra = df3.loc[(df3['Estados'] == 'Mato Grosso do Sul')
                                      | (df3['Estados'] == 'Mato Grosso')
                                      | (df3['Estados'] == 'Goiás')
                                      | (df3['Estados'] == 'Distrito Federal')]
                    fig = px.line(
                        est_tra,
                        x='Ano',
                        y='Empregado com carteira de trabalho assinada',
                        color='Estados', template=template)
                    fig.update_layout(
                            title='<b>Carteira de trabalho assinada no {}<b>'
                            .format(vendor))
                    return fig, {'display': 'block'}
                if vendor == 'Sudeste':
                    est_tra = df3.loc[(df3['Estados'] == 'Minas Gerais')
                                      | (df3['Estados'] == 'Espírito Santo')
                                      | (df3['Estados'] == 'Rio de Janeiro')
                                      | (df3['Estados'] == 'São Paulo')]
                    fig = px.line(
                        est_tra,
                        x='Ano',
                        y='Empregado com carteira de trabalho assinada',
                        color='Estados', template=template)
                    fig.update_layout(
                            title='<b>Carteira de trabalho assinada no {}<b>'
                            .format(vendor))
                    return fig, {'display': 'block'}
                if vendor == 'Sul':
                    est_tra = df3.loc[(
                        df3['Estados'] == 'Paraná')
                        | (df3['Estados'] == 'Santa Catarina')
                        | (df3['Estados'] == 'Rio Grande do Sul')]
                    fig = px.line(
                        est_tra,
                        x='Ano',
                        y='Empregado com carteira de trabalho assinada',
                        color='Estados', template=template)
                    fig.update_layout(
                            title='<b>Carteira de trabalho assinada no {}<b>'
                            .format(vendor))
                    return fig, {'display': 'block'}
            else:   # escondendo o botão Voltar
                return est_bar(), {'display': 'none'}

    else:
        return est_bar(), {'display': 'none'}


@callback(
        Output('graph4_reg', 'figure'),
        Output('grafico_todos_anos', 'figure'),
        Output('grafico_sexo', 'figure'),
        Input('list_years', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
        )
def update_output(value, toggle):
    template = template_theme1 if toggle else template_theme2
    if value == 'Todos os anos':
        fig2 = px.bar_polar(
            df2, r="População ocupada",
            theta="Regiões",
            color="População ocupada",
            template=template)
        fig2.update_layout(
            title='População Ocupada por Região',
            polar_angularaxis_ticktext=[
                'Nordeste', 'Norte', 'Centro-Oeste', 'Sudeste', 'Sul'])
    else:
        tabela_filtrada = df2.loc[df2['Ano'] == value, :]
        fig2 = px.bar_polar(
            tabela_filtrada, r="População ocupada",
            theta="Regiões",
            color="População ocupada",
            template=template)
        fig2.update_layout(
            title='Popoluação Ocupada por Região',
            polar_angularaxis_ticktext=['Nordeste', 'Norte',
                                        'Centro-Oeste', 'Sudeste', 'Sul'])
    if value == 'Todos os anos':
        fig4 = px.bar(reg, x='Regiões',
                      y=['Empregado com carteira de trabalho assinada',
                         'Empregado sem carteira de trabalho assinada',
                         'Militar ou funcionário público estatutário',
                         'Conta própria', 'Empregador',
                         'Outros'], template=template)
        fig4.update_layout(title="Distribuição de ocupações",
                           xaxis_title="Regiões",
                           yaxis_title="Dados somados",
                           legend_title="Dados coletados por ocupação")
    else:
        graph4 = reg.loc[reg['Ano'] == value, :]
        fig4 = px.bar(graph4, x='Regiões',
                      y=['Empregado com carteira de trabalho assinada',
                         'Empregado sem carteira de trabalho assinada',
                         'Militar ou funcionário público estatutário',
                         'Conta própria', 'Empregador', 'Outros'],
                      template=template)
        fig4.update_layout(title="Distribuição de ocupações",
                           xaxis_title="Regiões",
                           yaxis_title="Dados somados",
                           legend_title="Dados coletados por ocupação")
    if value == 'Todos os anos':
        fig3 = px.bar(df2, x='Regiões',
                      y='População desocupada',
                      color="Regiões",
                      title='População Desocupada',
                      template=template)
    else:
        dfano = df2.loc[df2['Ano'] == value, :]
        fig3 = px.bar(dfano, x='Regiões',
                      y='População desocupada',
                      color="Regiões",
                      title='População Desocupada',
                      template=template)
    return fig4, fig2, fig3


if __name__ == '__main__':
    app.run(debug=True)
