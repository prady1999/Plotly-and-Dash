

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import pandas as pd
from PriceIndices import MarketHistory, Indices
history = MarketHistory()
external_stylesheets = ['https://fonts.googleapis.com/css?family=Girassol']
tabs=html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Simple Moving Averages', value='tab-1'),
        dcc.Tab(label='Volatality Index', value='tab-2'),
        dcc.Tab(label='Relative Strength Index', value='tab-3'),
        dcc.Tab(label='Moving Average Divergence Convergence', value='tab-4'),
        dcc.Tab(label='Exponential Moving Averages', value='tab-5'),
        dcc.Tab(label='Bollinger Bands', value='tab-6'),
    ], colors={
        "border": "white",
        "primary": "gold",
        'background':'rgb(21,25,53)',
        "border-left":"1px green solid",
        'color':'white'
    })
],style={'color':'white'})



crypto=['bitcoin','ethereum','tether','bitcoin-cash','bitcoin-sv','eos','tezos','stellar','chainlink']
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)
server=app.server


daterange=html.Div([('Date Range :'),dcc.DatePickerRange(id='date-input',
                                                    min_date_allowed=datetime(2013, 4, 28),
                                                    max_date_allowed=datetime.now(),
                                                    initial_visible_month=datetime.now(),
                                                    start_date=datetime(2019, 1, 1),
                                                    end_date=datetime.now(),
                                                    stay_open_on_select=False,
                                                    number_of_months_shown=2,
                                                    month_format='MMMM,YYYY',
                                                    display_format='YYYY-MM-DD',
                                                    style={
                                                          'color': 'white',
                                                          'font-size': '30px',
                                                           'background':'rgb(21,25,53)'
                                                   })],style={'width':'50%','float':'left','font-size': '30px','padding-top':'10px','background':'rgb(21,25,53)','color':'white'})
cureencydropdown=html.Div(['Currencies:',dcc.Dropdown(id='dropdown',
                                options=[{'label': i, 'value': i} for i in crypto],
                                value='bitcoin',
                                optionHeight=30,
                                style={
                                    'height': '45px',
                                    'font-weight': 100,
                                    'font-size': '30px',
                                    'line-height': '20px',
                                    'color': 'black',
                                    'background':'rgb()',
                                    'position': 'middle',
                                    'display': 'inline-block',
                                    'width': '200px',
                                    'vertical-align': 'middle',
                                    'text-align':'center'

                                    }
                                )],style={'width':'50%','float':'right','display':'inline-block','font-size': '30px','padding-top':'10px','text-align':'right','background':'rgb(21,25,53)','color':'white'})

graphout=html.Div(id='graph')
table=html.Div(children=[html.Table(id='table'), html.Div(id='table-output')])
def serve_layout():
    return html.Div([
                html.Div([html.H1(['Dashboard For CryptoCurrencies With Indicator Option'],style={'color':'White','text-align':'center','background':'rgb(21,25,53)'}) ]),
              html.Div([daterange    ,      cureencydropdown

                       ],style={'background':'rgb(21,25,53)','height':'100px'}),
        html.Div(tabs),
       html.Div([ html.Div([graphout],style={'float':'left','width':'70'})   ,
        html.Div([table],style={'float':'right','width':'30'})
                ])



],style={'background':'rgb(21,25,53)'})

app.layout=serve_layout

@app.callback(Output('table','children'),[Input('dropdown','value')])
def draw_table(option):
    df = history.get_price(option, '20130428', '20200510')
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
    return dash_table.DataTable(id='table1',columns=[{"name": i, "id": i} for i in df.columns], data=df.to_dict('records'), style_table={'overflowY': 'scroll'}, fixed_rows={'headers': True, 'data': 5},
        style_cell={'width': '30','text-align':'center'})
@app.callback(Output('graph','children'),[Input('tabs-styled-with-props','value'),Input('date-input', 'start_date'),Input('date-input', 'end_date'),Input('dropdown', 'value')])
def draw_graph(tabs,start_date, end_date, option):
    if tabs=='tab-1':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        sma=Indices.get_simple_moving_average(df)
        data = sma[(sma.date >= start_date) & (sma.date <= end_date)]
        return dcc.Graph(id='graph1',figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['SMA'],'type':'line','name':'SMA','secondary_y':True}],
                                             'layout':{ 'title':f'Price VS Time ({option})','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}

    },style={'height':600,'width':975,'background':'rgb(21,25,53)'})
    elif tabs=='tab-2':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        vol=Indices.get_bvol_index(df)
        data = vol[(vol.date >= start_date) & (vol.date <= end_date)]
        return dcc.Graph(id='graph1',
                         figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['BVOL_Index'],'type':'line','name':'BVOL_Index','secondary_y':True}],

                                 'layout':{ 'title':'Price VS Time','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}})
    elif tabs=='tab-3':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        rsi=Indices.get_rsi(df)
        data =rsi[(rsi.date >= start_date) & (rsi.date <= end_date)]
        return dcc.Graph(id='graph1',
                         figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['RSI_2'],'type':'line','name':'RSI','secondary_y':True}],

                                 'layout':{ 'title':'Price VS Time','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}})
    elif tabs=='tab-4':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        rsi=Indices.get_moving_average_convergence_divergence(df)
        data =rsi[(rsi.date >= start_date) & (rsi.date <= end_date)]
        return dcc.Graph(id='graph1',
                         figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['MACD'],'type':'line','name':'RSI','secondary_y':True}],

                                 'layout':{ 'title':'Price VS Time','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}})
    elif tabs=='tab-5':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        rsi=Indices.get_exponential_moving_average(df)
        data =rsi[(rsi.date >= start_date) & (rsi.date <= end_date)]
        return dcc.Graph(id='graph1',
                         figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['EMA_20'],'type':'line','name':'EMA','secondary_y':True}],

                                 'layout':{ 'title':'Price VS Time','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}})
    elif tabs=='tab-6':
        df = history.get_price(option, '20130428', '20200510')
        df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
        rsi=Indices.get_bollinger_bands(df)
        data =rsi[(rsi.date >= start_date) & (rsi.date <= end_date)]
        return dcc.Graph(id='graph1',
                         figure={'data':[{'x':data['date'],'y':data['price'],'type':'line','name':f'{option}'},{'x':data['date'],'y':data['BB_upper'],'type':'line','name':'BB_upper'},{'x':data['date'],'y':data['BB_lower'],'type':'line','name':'BB_lower'}],

                                 'layout':{ 'title':'Price VS Time','xaxis':{'title':'Time'},'yaxis':{'title':'Price'}}})






app.css.config.serve_locally = True
app.scripts.config.serve_locally = True




if __name__ == '__main__':
    app.run_server()
