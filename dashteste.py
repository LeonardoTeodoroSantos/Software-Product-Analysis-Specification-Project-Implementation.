from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# aqui eu conecto no arquivo excel
df = pd.read_excel('sexecor.xlsx', engine='openpyxl')
df2 = pd.read_excel('Regiões.xlsx', engine='openpyxl')

# tratamento do data frame sexecor
df['Ano'] = df['ano'].dt.year
df.drop('ano',axis=1,inplace=True)
sexo_tratado = df[df['Sexo'].str.len() > 4]
sexo_tratado.drop(['Sexo e cor ou raça (2)', 'Cor ou raça (2)', 'Total_ao_ano'], axis = 1, inplace=True)
sexo_tratado['População em idade de trabalhar\n(1 000 pessoas)'] = sexo_tratado['População em idade de trabalhar\n(1 000 pessoas)'].astype('int')
sexo_tratado['População na força de trabalho\n(1 000 pessoas)'] = sexo_tratado['População na força de trabalho\n(1 000 pessoas)'].astype('int')
sexo_tratado['População ocupada\n(1 000 pessoas)'] = sexo_tratado['População ocupada\n(1 000 pessoas)'].astype('int')
sexo_tratado['População ocupada em trabalhos formais (1)\n(1 000 pessoas)'] = sexo_tratado['População ocupada em trabalhos formais (1)\n(1 000 pessoas)'].astype('int')
sexo_tratado['População desocupada\n(1 000 pessoas)'] = sexo_tratado['População desocupada\n(1 000 pessoas)'].astype('int')
sexo_tratado['População na força de trabalho potencial\n(1 000 pessoas)'] = sexo_tratado['População na força de trabalho potencial\n(1 000 pessoas)'].astype('int')
sexo_tratado['População subutilizada\n(1 000 pessoas)'] = sexo_tratado['População subutilizada\n(1 000 pessoas)'].astype('int')
sexo_tratado

# tratamento da coluna com data para criar uma coluna 'Ano' com somente o ano desta data.
df2['Ano'] = df2['ano'].dt.year

# tratamento de algumas colunas para numeros inteiros.
df2['População em idade de trabalhar\n(1 000 pessoas)'] = df2['População em idade de trabalhar\n(1 000 pessoas)'].astype(int)
df2['População na força de trabalho\n(1 000 pessoas)'] = df2['População na força de trabalho\n(1 000 pessoas)'].astype(int)
df2['População ocupada\n(1 000 pessoas)'] = df2['População ocupada\n(1 000 pessoas)'].astype(int)
df2['População ocupada em trabalhos formais (1)\n(1 000 pessoas)'] = df2['População ocupada em trabalhos formais (1)\n(1 000 pessoas)'].astype(int)
df2['População desocupada\n(1 000 pessoas)'] = df2['População desocupada\n(1 000 pessoas)'].astype(int)
df2['População na força de trabalho potencial\n(1 000 pessoas)'] = df2['População na força de trabalho potencial\n(1 000 pessoas)'].astype(int)
df2['População subutilizada\n(1 000 pessoas)']= df2['População subutilizada\n(1 000 pessoas)'].astype(int)


#para excluir a coluna 'ano' que ficou com os dias, meses, ano e ainda hora, após ficou somente com ano.
df2.drop('ano',axis=1, inplace=True)



fig = px.bar(df, x="Estados", y="População desocupada\n(1 000 pessoas)", color="Estados", barmode="group")
fig2 = px.line(df2, x="Ano", y="Regiões")
opcoes = list(df2['Regiões'].unique())
opcoes.append('Brasil')

app.layout = html.Div(children=[
    html.H1(children='Dados Relacionados à trabalho'),
    html.H2(children='Gráfico com a população em idade de trabalhar'),
    html.Div(children='''
        Este gráfico mostra as pessoas que estão em idade de trabalhar mas, não especifica a idade delas.
    '''),

    dcc.Dropdown(opcoes, value='Brasil', id='lista_regioes'),
    dcc.Graph(
        id='grafico_todas_regioes',
        figure=fig2
    )
])

@callback(
    Output('grafico_todas_regioes', 'figure'),
    Input('lista_regioes', 'value')
)
def update_output(value):
    if value == 'Brasil':
        fig2 = px.line(df2, y="População ocupada\n(1 000 pessoas)", x="Ano", color='Regiões')
        fig3 = px.bar(df3, y='',x='')
    else:
        tabela_filtrada = df2.loc[df2['Regiões'] == value,:]
        fig2 = px.line(tabela_filtrada, y="População ocupada\n(1 000 pessoas)", x="Ano",color='Regiões')
    return fig2
if __name__ == '__main__':
    app.run(debug=True)