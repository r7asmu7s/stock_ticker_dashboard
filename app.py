import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas_datareader.data as web
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import os
import pytz



app = dash.Dash()

server = app.server

# os.environ["ALPHAVANTAGE_API_KEY"] = "WDA2CIFZBVIN045Z"
url = 'https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv'
nsdq = pd.read_csv(url)
nsdq = nsdq.set_index('Symbol')
options = []
for tic in nsdq.index:
    # 'Label': 'user sees','value': 'script sees'
    # the_dict = {}
    # the_dict['label'] = nsdq.loc[tic]['Company Name'] + ' - ' + tic
    # the_dict['value'] = tic
    # options.append(the_dict)
    options.append({
        'label': f"{tic} - {nsdq.loc[tic]['Company Name']}",
        'value': tic,
    })

app.layout = html.Div([
    html.Div([
        html.H1('Stock Ticker Dashboard'),
    ]),
    html.Div([
        html.H3(
            'Enter a Stock Symbol: ',
            style = {
                'paddingRight': '30px',
            },
        ),
        dcc.Dropdown(
            id = 'stock-picker',
            options = options,
            value = ['TSLA'],
            multi = True,
            # style = {
            #     'fontSize': 24,
            #     'width': 75,
            # }
        ),
    ],
    style = {
        'display': 'inline-block',
        'verticalAlign': 'top',
        'width': '30%'
    },
    ),
    html.Div([
        html.H3(
            'Select a Start and End Date: '
        ),
        dcc.DatePickerRange(
            id = 'date-picker',
            min_date_allowed = datetime(2019, 1, 1),
            max_date_allowed = datetime.today(),
            start_date = datetime(2019, 1, 1),
            end_date = datetime.today(),
        ),
    ],
    style = {
        'display': 'inline-block',
    }
    ),
    html.Div([
        html.Button(
            id = 'submit-button',
            n_clicks = 0,
            children = 'Submit',
            style = {
                'fontSize': 24,
                'marginLeft': '30px'
            }
        )
    ],
    style = {
        'display': 'inline-block',
    }
    ),
    html.Div([
        dcc.Graph(
            id = 'graph',
            figure = {
                'data': [
                    {'x': [1, 2], 'y': [3, 1]}
                ],
                # 'layout': {'title': 'Default Title'},
            }
        ),
    ])
])

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
        df = pdr.get_data_tiingo(tic, api_key = '3e46e9afa3a7716e0bdefb6a7369b1ff902f583e').reset_index().set_index(['date'])

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

if __name__ == '__main__':
    app.run_server()