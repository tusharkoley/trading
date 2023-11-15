#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import yfinance as yf
import datapackage
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from itertools import product
import time


# Load S&P 500 Companies data
data_url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'
package = datapackage.Package(data_url)
resources = package.resources

for resource in resources:
    if resource.tabular:
        stocks_df = pd.read_csv(resource.descriptor['path'])

stocks_df.set_index('Symbol', inplace=True)

# Load Nifty 200 Companies data
snp_df = pd.read_csv('nifty200list.csv')
snp_df = snp_df.rename(columns={'Company Name':'Name'}).drop(['Series','ISIN Code'], axis=1)
snp_df['Symbol'] = snp_df['Symbol'] + '.NS'
snp_df = snp_df.set_index('Symbol')
stocks_df = pd.concat([snp_df, stocks_df])
all_tickers = ['^BSESN'] + list(stocks_df.index)

# Global Variables
INITIAL_CASH = 100000
CASH_AVAILABLE = 100000
PORTFOLIO_VALUE = 0
NET_PROFIT = CASH_AVAILABLE + PORTFOLIO_VALUE - INITIAL_CASH
columns = ['ticker','avg_price', 'current_price', 'no_of_shares', 'pos_value', 'stop_loss',
           'target_pr', 'transaction_cost', 'position_status', 'position_type']
position_df = pd.DataFrame(columns=columns)
closed_df = pd.DataFrame(columns=columns)
columns.append('limit_pr')
limit_df = pd.DataFrame(columns=columns)
TOTAL_TRANSACTIONS = 0

def get_latest_price(ticker):
    """
    Get the latest stock price for a given ticker.

    Parameters:
    - ticker (str): The stock ticker symbol.

    Returns:
    - float: The latest stock price.
    """
    data = yf.download(tickers=ticker, period='1d', interval='1m')
    return np.round(data.iloc[-1].Close, 2)

def open_position(ticker, quantity=1, amount=-1, position_type='B', stop_loss=-1, target_pr=-1, 
                  transaction_cost=3, order_type='M', limit_pr=-1):
    """
    Open a new position for a given stock.

    Parameters:
    - ticker (str): The stock ticker symbol.
    - quantity (int): The quantity of stocks to buy/sell.
    - amount (float): The amount to invest (-1 if quantity is provided).
    - position_type (str): 'B' for Buy, 'S' for Sell.
    - stop_loss (float): Stop-loss price.
    - target_pr (float): Target price.
    - transaction_cost (float): Transaction cost.
    - order_type (str): 'M' for Market Order, 'L' for Limit Order.
    - limit_pr (float): Limit price for Limit Order.
    """
    global position_df, limit_df, CASH_AVAILABLE, PORTFOLIO_VALUE, NET_PROFIT, TOTAL_TRANSACTIONS

    if order_type == 'L' and limit_pr == -1:
        print('Please provide Limit Price')
        return

    price = get_latest_price(ticker)
    data_dict = {}

    if amount != -1:
        quantity = amount / price

    if position_type == 'S':
        quantity = -quantity

    data_dict['ticker'] = [ticker]
    data_dict['avg_price'] = [price]
    data_dict['current_price'] = [price]
    data_dict['no_of_shares'] = [quantity]
    data_dict['pos_value'] = [price * quantity]
    data_dict['stop_loss'] = [stop_loss]
    data_dict['target_pr'] = [target_pr]
    data_dict['transaction_cost'] = [transaction_cost]
    data_dict['position_status'] = ['Open']
    data_dict['position_type'] = ['B']

    if order_type == 'M':
        position_df = pd.concat([position_df, pd.DataFrame.from_dict(data_dict)])
        position_df = position_df.groupby('ticker').agg({'pos_value':'sum', 'current_price':'last',
                                       'no_of_shares':'sum', 'target_pr':'last',
                                       'transaction_cost':'sum', 'stop_loss':'first', 'position_status':'last',
                                       'position_type':'last'}).reset_index()
        try:
            position_df['avg_price'] = position_df['pos_value'] / position_df['no_of_shares']
        except:
            position_df['avg_price'] = price

        PORTFOLIO_VALUE = PORTFOLIO_VALUE + price * quantity
        CASH_AVAILABLE = CASH_AVAILABLE - price * quantity - transaction_cost
        NET_PROFIT = CASH_AVAILABLE + PORTFOLIO_VALUE - INITIAL_CASH
        TOTAL_TRANSACTIONS = TOTAL_TRANSACTIONS + 1
    else:
        data_dict['limit_pr'] = limit_pr
        limit_df = pd.concat([limit_df, pd.DataFrame.from_dict(data_dict)])
        limit_df = limit_df.groupby('ticker').agg({'avg_price':'mean', 'pos_value':'sum', 'current_price':'last',
                                       'no_of_shares':'sum', 'target_pr':'last',
                                       'transaction_cost':'sum', 'stop_loss':'first', 'position_status':'last',
                                       'position_type':'last', 'limit_pr':'last'}).reset_index()

    position_df = position_df.drop((position_df[position_df['no_of_shares'] == 0]).index)

def rebalance_portfolio():
    """
    Rebalance the portfolio by checking stop-loss conditions and executing limit orders.
    """
    global position_df, limit_df, CASH_AVAILABLE, PORTFOLIO_VALUE, NET_PROFIT
    curr_prices = []
    stop_dict = position_df.set_index('ticker')['stop_loss'].to_dict()

    for ticker in position_df['ticker']:
        curr_price = get_latest_price(ticker)
        curr_prices.append(curr_price)
        stop_loss = stop_dict[ticker]

        if stop_loss != -1:
            if position_df[position_df['ticker'] == ticker]['stop_loss'].values[0] <= curr_price:
                print('stop loss ', ticker)
                close_position(ticker)

    position_df['current_price'] = curr_prices

    try:
        position_df['curr_profit'] = (position_df['current_price'] - position_df['avg_price']) * position_df['no_of_shares']
    except:
        pass

    PORTFOLIO_VALUE = (position_df['current_price'] * position_df['no_of_shares']).sum()
    NET_PROFIT = CASH_AVAILABLE + PORTFOLIO_VALUE - INITIAL_CASH

    if limit_df.shape[0] > 0:
        print('**Inside Limit Order')
        for ticker in limit_df['ticker']:
            limit_pr = limit_df[limit_df['ticker'] == ticker]['limit_pr'].values[0]
            limit_qty = limit_df[limit_df['ticker'] == ticker]['no_of_shares'].values[0]
            position_type = limit_df[limit_df['ticker'] == ticker]['position_type'].values[0]

            print('limit price', limit_pr, limit_qty)

            if get_latest_price(ticker) >= limit_pr and position_type == 'B':
                print('inside limit ', limit_pr, limit_qty)
                open_position(ticker=ticker, quantity=limit_qty, order_type='M')
                limit_df = limit_df.drop((limit_df[limit_df['ticker'] == ticker]).index)

def close_position(ticker):
    """
    Close an open position for a given stock.

    Parameters:
    - ticker (str): The stock ticker symbol.
    """
    global position_df, closed_df, limit_df, CASH_AVAILABLE, PORTFOLIO_VALUE, NET_PROFIT, TOTAL_TRANSACTIONS

    if (position_df[position_df['ticker'] == ticker].shape[0]) == 0:
        print(f'No position available for {ticker}')
        return

    quantity = position_df[position_df['ticker'] == ticker]['no_of_shares'].values[0]
    open_position(ticker=ticker, quantity=-quantity)

def print_status():
    """
    Print the current status of the portfolio.
    """
    colors = ['blue', 'green', 'black', 'purple', 'red', 'brown']
    fig = go.Figure(data=[go.Pie(labels=position_df['ticker'].values,
                                values=(position_df['current_price'] * position_df['no_of_shares']).values)])

    fig.update_traces(hoverinfo='label+percent', textfont_size=20,
                      textinfo='label+percent',
                      marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))

    fig.update_layout(
        title=f"Portfolio Allocation PCT, Cash Available = ${int(CASH_AVAILABLE)},Net Profit/Loss:{int(NET_PROFIT)}, P/L={np.round(NET_PROFIT * 100 / INITIAL_CASH, 2)}%")
    fig.show()

def thread_rebalance():
    """
    Thread function to periodically rebalance the portfolio.
    """
    print("Thread Start")
    for i in range(1000):
        print('Counter', i)
        rebalance_portfolio()
        time.sleep(60)

    print("Thread End")

# Example usage
open_position('AAPL', quantity=100)
open_position('META', quantity=70)
open_position('MSFT', quantity=40)
open_position('BAC', quantity=100)
open_position('MRNA', 100)
open_position('GOOG', 120)
open_position('REGN', 15)
open_position('KO', 100)
open_position('MNST', 100)

# Rebalance and print portfolio status
rebalance_portfolio()

close_position('META')
print_status()
