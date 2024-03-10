from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# aqui eu conecto no arquivo excel
df = pd.read_excel('sexecor.xlsx', engine='openpyxl')
df2 = pd.read_excel('Regiões.xlsx', engine='openpyxl')

# tratamento do data frame sexecor
df.dropna(how='all', inplace=True)
datasexo = pd.DatetimeIndex(df['ano'])
df['Ano'] = datasexo.year
df.drop('ano', axis=1, inplace=True)
sexo_tratado = df[df['Sexo'].str.len() > 4]
sexo_tratado.drop(
    ['Sexo e cor ou raça (2)',
     'Cor ou raça (2)', 'Total_ao_ano'], axis=1, inplace=True)
sexo_tratado['População em idade de trabalhar'] = sexo_tratado[
    'População em idade de trabalhar\n(1 000 pessoas)'].astype('int')
sexo_tratado['População na força de trabalho'] = sexo_tratado[
    'População na força de trabalho\n(1 000 pessoas)'].astype('int')
sexo_tratado['População ocupada'] = sexo_tratado[
    'População ocupada\n(1 000 pessoas)'].astype('int')
sexo_tratado['População ocupada em trabalhos formais'] = sexo_tratado[
    'População ocupada em trabalhos formais (1)\n(1 000 pessoas)'].astype(int)
sexo_tratado['População desocupada'] = sexo_tratado[
    'População desocupada\n(1 000 pessoas)'].astype('int')
sexo_tratado['População na força de trabalho potencial'] = sexo_tratado[
    'População na força de trabalho potencial\n(1 000 pessoas)'].astype('int')
sexo_tratado['População subutilizada'] = sexo_tratado[
    'População subutilizada\n(1 000 pessoas)'].astype('int')
sexo_tratado.drop(
    ['População em idade de trabalhar\n(1 000 pessoas)',
     'População na força de trabalho\n(1 000 pessoas)',
     'População ocupada\n(1 000 pessoas)',
     'População ocupada em trabalhos formais (1)\n(1 000 pessoas)',
     'População desocupada\n(1 000 pessoas)',
     'População na força de trabalho potencial\n(1 000 pessoas)',
     'População subutilizada\n(1 000 pessoas)'], axis=1, inplace=True)

# tratamento da coluna 'Ano' com somente o ano desta data.
df2['Ano'] = df2['ano'].dt.year
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
df2.drop(
    ['População em idade de trabalhar\n(1 000 pessoas)',
     'População na força de trabalho\n(1 000 pessoas)',
     'População ocupada\n(1 000 pessoas)',
     'População ocupada em trabalhos formais (1)\n(1 000 pessoas)',
     'População desocupada\n(1 000 pessoas)',
     'População na força de trabalho potencial\n(1 000 pessoas)',
     'População subutilizada\n(1 000 pessoas)'], axis=1, inplace=True)

# Excluindo coluna 'ano' minusculo e deixando a 'Ano' já tratada
df2.drop('ano', axis=1, inplace=True)

opcoes_ano = list(sexo_tratado['Ano'].unique())
opcoes_ano.append('Todos os anos')

opcoes = list(df2['Ano'].unique())
opcoes.append('Todos os anos')

fig2 = px.bar(df2, y="População ocupada", x="Regiões",
              color='Regiões', barmode="relative")
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)'
                   )
fig3 = px.pie(sexo_tratado,
              values='População em idade de trabalhar',
              names='Sexo',
              color="Sexo",
              color_discrete_sequence=["dodgerblue", "hotpink"],
              title='Separação por sexo')

app.layout = html.Div(className="fundopag", children=[
    html.H1(children='Dados Relacionados à trabalho'),
    html.Div(children='''
        Pessoas em idade para trabalhar, separado por regiões.
    '''),
    dcc.Dropdown(opcoes, value='Todos os anos', id='list_years',
                 className="botao1"
                 ),
    dcc.Graph(
        id='grafico_todos_anos',
        figure=fig2,
        className="graph1",
    ),
    html.Div(children=[
        dcc.Dropdown(opcoes_ano, value='Todos os anos', id='lista_anos',
                     className="botao2"),
        dcc.Graph(
            id='grafico_sexo',
            figure=fig3,
            className="graph2"
        )
    ])
])


@callback(
        Output('grafico_todos_anos', 'figure'),
        Input('list_years', 'value'),
        )
def update_output(value):
    if value == 'Todos os anos':
        fig2 = px.bar(df2, y="População ocupada",
                      x="Regiões",
                      title='População ocupada',
                      color='Regiões',
                      barmode='relative')
        fig2.update_layout(paper_bgcolor='#a9bcce',
                           plot_bgcolor='#a9bcce',
                           font_color='#ffffff',
                           title_text='População Ocupada x Região',
                           title_font_size=22
                           )
        fig2.update_yaxes(title='População Ocupada',
                          title_font_color='#ffffff',
                          title_font_size=15)
    else:
        tabela_filtrada = df2.loc[df2['Ano'] == value, :]
        fig2 = px.bar(tabela_filtrada,
                      y="População ocupada",
                      x="Regiões",
                      title='População ocupada',
                      color='Regiões',
                      barmode='relative')
        fig2.update_layout(paper_bgcolor='#a9bcce',
                           plot_bgcolor='#a9bcce',
                           font_color='#ffffff',
                           title_text='População Ocupada',
                           title_font_size=22
                           )
        fig2.update_yaxes(title='População Ocupada',
                          title_font_color='#ffffff',
                          title_font_size=15)
    return fig2


@callback(
        Output('grafico_sexo', 'figure'),
        Input('lista_anos', 'value'),
)
def sex(value):
    if value == 'Todos os anos':
        fig3 = px.pie(sexo_tratado,
                      values='População em idade de trabalhar',
                      names='Sexo',
                      color="Sexo",
                      color_discrete_sequence=["dodgerblue", "hotpink"],
                      title='Em idade de trabalhar por sexo')
        fig3.update_layout(paper_bgcolor='#a9bcce',
                           plot_bgcolor='#a9bcce',
                           title_font_color='#ffffff'
                           )
    else:
        sexo_filtrado = sexo_tratado.loc[sexo_tratado['Ano'] == value, :]
        fig3 = px.pie(sexo_filtrado,
                      values="População em idade de trabalhar",
                      names='Sexo',
                      color='Sexo',
                      color_discrete_sequence=["dodgerblue", "hotpink"],
                      title='Em idade de trabalhar por sexo')
        fig3.update_layout(paper_bgcolor='#a9bcce',
                           plot_bgcolor='#a9bcce',
                           title_font_color='#ffffff'
                           )
    return fig3


if __name__ == '__main__':
    app.run(debug=True)
