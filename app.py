from datetime import datetime
import pytz
import pandas as pd
import pandas_datareader as pdr
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

external_stylesheet = {
    'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
    'rel': 'stylesheet',
    'integrity': 'sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w',
    'crossorigin': 'anonymous'
}


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheet])

server = app.server

url = 'https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv'
nsdq = pd.read_csv(url)
nsdq = nsdq.set_index('Symbol')
options = []
for tic in nsdq.index:
    options.append({
        'label': f"{tic} - {nsdq.loc[tic]['Company Name']}",
        'value': tic,
    })


app.layout = html.Div([
    dbc.Container([
        html.Div([
            html.H1('Stock Ticker Dashboard'),
        ], className="display-1"),
        dbc.Row(
            [
                dbc.Col(html.Div([
                        html.P('Enter a Stock Symbol: ', className='text-muted'),
                        dbc.FormGroup([
                            dcc.Dropdown(
                                id='stock-picker',
                                options=options,
                                value=['TSLA'],
                                multi=True,
                                className='p-2'
                            ),
                        ])
                        ]), width=6, className='p-2'),

                dbc.Col(html.Div([
                        html.P('Select a Start and End Date: ', className='text-muted'),
                        dbc.FormGroup([
                            dcc.DatePickerRange(
                                id='date-picker',
                                min_date_allowed=datetime(2019, 1, 1),
                                max_date_allowed=datetime.today(),
                                start_date=datetime(2019, 1, 1),
                                end_date=datetime.today(),
                                className='p-2',
                            )
                        ], style={
                            'width': '100%',
                        }
                        )
                        ]), width=6, className='p-2'),

                dbc.Col(html.Div([
                    dbc.FormGroup([
                        dbc.Button(
                            id='submit-button',
                            n_clicks=0,
                            children='Submit',
                            outline=True,
                            color='primary',
                            className='m-1',
                            block=True,
                        )
                    ])
                ]), width=12, className='p-2'),

            ]
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id='graph',
                            figure={
                                'data': [
                                    {'x': [1, 2], 'y': [3, 1]}
                                ],
                                # 'layout': {'title': 'Default Title'},
                            }
                        )
                    )
                )

            ], width=12, className='p-2')
        ]),
    ], className="pb-3"
    ),
    html.Div([
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.A(
                                html.I(className="fas fa-phone p-1"),
                                href="tel:5456021942",
                                style={"text-decoration": 'none', "color": 'white'}
                            ),
                            html.A(
                                html.I(className="fas fa-at p-1"),
                                href="mailto:m.jubeni@protonmail.com",
                                style={"text-decoration": 'none', "color": 'white'}
                            ),
                            html.A(
                                html.I(className="fab fa-linkedin p-1"),
                                href="https://www.linkedin.com/in/m-jubeni/",
                                style={"text-decoration": 'none', "color": 'white'}
                            ),
                            html.A(
                                html.I(className="fab fa-github p-1"),
                                href="https://github.com/r7asmu7s",
                                style={"text-decoration": 'none', "color": 'white'}
                            ),
                            html.A(
                                html.I(className="fab fa-kaggle p-1"),
                                href="https://www.kaggle.com/r7asmu7s",
                                style={"text-decoration": 'none', "color": 'white'}
                            )

                        ], style={"text-decoration": 'none', "color": 'white'}),
                        html.P([
                            f"2020 - {datetime.today().year} ",
                            html.A(
                                "Mehrzad M. Jubeni",
                                href="https://www.mjubeni.com",
                                style={"text-decoration": 'none', "color": 'white'}

                            )
                        ])
                    ])
                ])

            ])
        ], className="text-center text-white p-4", style={
            'background-color': '#008000', 'color': 'white', 'text-decoration': 'none'
        })
    ])

], className="mt-5"
)


@app.callback(
    Output('graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [
        State('stock-picker', 'value'),
        State('date-picker', 'start_date'),
        State('date-picker', 'end_date')
    ]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[: 10], '%Y-%m-%d')
    end = datetime.strptime(end_date[: 10], '%Y-%m-%d')
    # to make tz aware
    start = pytz.utc.localize(start)
    end = pytz.utc.localize(end)

    traces = []
    for tic in stock_ticker:
        df = pdr.get_data_tiingo(
            tic, api_key='3e46e9afa3a7716e0bdefb6a7369b1ff902f583e').reset_index().set_index(['date'])

        df_date_range = df.loc[start: end]
        traces.append({
            'x': df_date_range.index,
            'y': df_date_range['close'],
            'name': tic,
        })
    figure = {
        'data': traces,
        'layout': {'title': ', '.join(stock_ticker) + ' Closing Prices'}
    }

    return figure


if __name__ == "__main__":
    app.run_server()
