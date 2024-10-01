import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import base64

# Definindo o caminho absoluto para os arquivos CSV
demonstrativo_financeiro_path = r'demonstrativo_financeiro.csv'
financial_data_path = r'financial_data.csv'

# Carregar a imagem
image_path = r'logo.png'
encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},
                           {"rel": "icon", "href": "/assets/4.png", "type": "image/png"}],
                suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div(
        className="main-header",
        children=[
            html.H1(
                children=[
                    "Dashboard Interativo de Dados Financeiros",
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'height': '60px', 'float': 'right', 'padding-left': '20px'})
                ],
                style={"color": "white", "text-align": "center"}
            )
        ],
        style={"background": "linear-gradient(to right, #903361, #313162)", "padding": "10px", "border-radius": "10px"}
    ),
    html.Div([
        dcc.Dropdown(
            id='language-dropdown',
            options=[
                {'label': 'Português', 'value': 'pt'},
                {'label': 'English', 'value': 'en'}
            ],
            value='pt',  # Default language
            clearable=False,
            style={'width': '200px', 'margin': '10px auto'}
        ),
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Análise de Resultados', value='tab-1', style={'backgroundColor': '#313162', 'color': 'white'}),
            dcc.Tab(label='Demonstrativo de Resultados', value='tab-2', style={'backgroundColor': '#313162', 'color': 'white'}),
            dcc.Tab(label='Dados em Planilha', value='tab-3', style={'backgroundColor': '#313162', 'color': 'white'}),
        ]),
        html.Div(id='tabs-content-example')
    ], style={'width': '80%', 'margin': 'auto', 'backgroundColor': '#f2f2f2'})
])

@app.callback(
    Output('tabs-example', 'children'),
    Output('tabs-content-example', 'children'),
    Input('tabs-example', 'value'),
    Input('language-dropdown', 'value')
)
def render_content(tab, lang):
    # Lendo os dados
    df = pd.read_csv(financial_data_path)
    df_demonstrativo = pd.read_csv(demonstrativo_financeiro_path)

    tabs_labels = {
        'pt': ['Análise de Resultados', 'Demonstrativo de Resultados', 'Dados em Planilha'],
        'en': ['Results Analysis', 'Financial Statement', 'Spreadsheet Data']
    }

    analysis_title = {'pt': 'Análise de Resultados Financeiros Mensais', 'en': 'Monthly Financial Results Analysis'}
    evolution_title = {'pt': 'Evolução da Receita', 'en': 'Revenue Evolution'}
    indebtedness_title = {'pt': 'Endividamento Geral', 'en': 'Overall Indebtedness'}
    final_result_title = {'pt': 'Demonstrativo de Resultados', 'en': 'Financial Statement'}
    final_comp_title = {'pt': 'Resultado Final do Comp.', 'en': 'Final Result of the Comp.'}
    accumulated_result_title = {'pt': 'Resultado Acumulado Ano', 'en': 'Accumulated Year Result'}
    average_result_title = {'pt': 'Resultado Médio Mensal', 'en': 'Average Monthly Result'}
    average_variation_title = {'pt': 'Variação Média Ano', 'en': 'Average Year Variation'}
    net_operating_revenue_title = {'pt': 'Receita Operacional Líquida', 'en': 'Net Operating Revenue'}
    final_result_chart_title = {'pt': 'Resultado Final', 'en': 'Final Result'}
    filter_label = {'pt': 'Filtro:', 'en': 'Filter:'}
    month_label = {'pt': 'Mês:', 'en': 'Month:'}

    tab1 = dcc.Tab(label=tabs_labels[lang][0], value='tab-1', style={'backgroundColor': '#313162', 'color': 'white'})
    tab2 = dcc.Tab(label=tabs_labels[lang][1], value='tab-2', style={'backgroundColor': '#313162', 'color': 'white'})
    tab3 = dcc.Tab(label=tabs_labels[lang][2], value='tab-3', style={'backgroundColor': '#313162', 'color': 'white'})

    if tab == 'tab-1':
        content = html.Div([
            html.H1(analysis_title[lang]),
            dcc.Graph(
                id='analise-resultados',
                figure={
                    'data': [
                        go.Bar(
                            x=df['Mes'],
                            y=df['Receitas'],
                            name='Receitas',
                            marker=dict(color='#383939')
                        ),
                        go.Bar(
                            x=df['Mes'],
                            y=df['Custos'],
                            name='Custos',
                            marker=dict(color='#903361')
                        ),
                        go.Scatter(
                            x=df['Mes'],
                            y=df['Lucros'],
                            mode='lines+markers',
                            name='Lucros',
                            marker=dict(color='#313162')
                        )
                    ],
                    'layout': go.Layout(
                        title=analysis_title[lang],
                        barmode='group'
                    )
                }
            ),
            dcc.Graph(
                id='evolucao-receita',
                figure={
                    'data': [
                        go.Scatter(
                            x=df['Mes'],
                            y=df['Receitas'].cumsum(),
                            mode='lines+markers',
                            fill='tozeroy',
                            name='Evolução da Receita',
                            marker=dict(color='purple')
                        )
                    ],
                    'layout': go.Layout(
                        title=evolution_title[lang]
                    )
                }
            ),
            dcc.Graph(
                id='endividamento-geral',
                figure={
                    'data': [
                        go.Pie(
                            labels=df['Mes'],
                            values=df['Endividamento'],
                            name='Endividamento',
                            marker=dict(colors=['#313162', '#383939', '#903361', '#555555', '#444444'])
                        )
                    ],
                    'layout': go.Layout(
                        title=indebtedness_title[lang]
                    )
                }
            )
        ], style={'backgroundColor': '#f2f2f2'})
    elif tab == 'tab-2':
        content = html.Div([
            html.H1(final_result_title[lang]),

            html.Div([
                html.Div([
                    html.H3(final_comp_title[lang]),
                    html.P(f"R$ {abs(df_demonstrativo['Resultado_Final'].sum()):,.2f}")
                ], className="result-box four columns"),

                html.Div([
                    html.H3(accumulated_result_title[lang]),
                    html.P(f"R$ {abs(df_demonstrativo['Resultado_Final'].sum()):,.2f}")
                ], className="result-box four columns"),

                html.Div([
                    html.H3(average_result_title[lang]),
                    html.P(f"R$ {abs(df_demonstrativo['Resultado_Final'].mean()):,.2f}")
                ], className="result-box four columns"),

                html.Div([
                    html.H3(average_variation_title[lang]),
                    html.P(f"{abs(((df_demonstrativo['Resultado_Final'].sum() / len(df_demonstrativo)) / df_demonstrativo['Resultado_Final'].mean() - 1) * 100):.2f}%")
                ], className="result-box four columns")
            ], className="row", style={'display': 'flex', 'justify-content': 'space-around', 'flex-wrap': 'wrap', 'backgroundColor': '#f2f2f2'}),

            dcc.Graph(
                id='receita-operacional-liquida',
                figure={
                    'data': [
                        go.Bar(
                            x=df_demonstrativo['Mes'],
                            y=df_demonstrativo['Receita_Operacional_Liquida'],
                            name='Receita Operacional Líquida',
                            marker=dict(color='#313162')
                        )
                    ],
                    'layout': go.Layout(
                        title=net_operating_revenue_title[lang]
                    )
                }
            ),

            dcc.Graph(
                id='resultado-final',
                figure={
                    'data': [
                        go.Scatter(
                            x=df_demonstrativo['Mes'],
                            y=df_demonstrativo['Resultado_Final'],
                            mode='lines+markers',
                            name='Resultado Final',
                            marker=dict(color='#313162')
                        )
                    ],
                    'layout': go.Layout(
                        title=final_result_chart_title[lang]
                    )
                }
            )
        ], style={'text-align': 'center', 'backgroundColor': '#f2f2f2'})
    elif tab == 'tab-3':
        content = html.Div([
            html.H1(tabs_labels[lang][2]),
            html.Div([
                html.Label(filter_label[lang]),
                dcc.Dropdown(
                    id='data-filter',
                    options=[
                        {'label': 'Receita', 'value': 'Receitas'},
                        {'label': 'Custo', 'value': 'Custos'},
                        {'label': 'Lucro', 'value': 'Lucros'}
                    ],
                    value='Receitas',
                    clearable=False,
                    style={'width': '200px'}
                ),
                html.Label(month_label[lang]),
                dcc.Dropdown(
                    id='month-filter',
                    options=[{'label': month, 'value': month} for month in df['Mes'].unique()],
                    value=df['Mes'].iloc[0],
                    clearable=False,
                    style={'width': '200px'}
                )
            ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'}),

            dcc.Graph(id='table-graph')
        ], style={'backgroundColor': '#f2f2f2'})

    return [tab1, tab2, tab3], content

@app.callback(
    Output('table-graph', 'figure'),
    Input('data-filter', 'value'),
    Input('month-filter', 'value')
)
def update_table(selected_data, selected_month):
    df = pd.read_csv(financial_data_path)
    filtered_df = df[df['Mes'] == selected_month]

    table_figure = go.Figure(data=[go.Table(
        header=dict(values=list(filtered_df[['Mes', selected_data]].columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[filtered_df['Mes'], filtered_df[selected_data]],
                   fill_color='lavender',
                   align='left'))
    ])

    return table_figure

if __name__ == '__main__':
    app.run_server(debug=True)
