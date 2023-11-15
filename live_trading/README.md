# Automated Stock Portfolio Management

## Overview

This Python script provides automated stock portfolio management capabilities. It leverages the Yahoo Finance API (`yfinance`) for real-time stock data, allowing users to open and close positions, set stop-loss and target prices, and execute limit orders.

## Features

- **Real-Time Stock Data:** Utilizes the `yfinance` library to fetch real-time stock prices.
- **Portfolio Management:** Opens and closes positions, executes limit orders, and implements stop-loss and target prices.
- **Rebalancing:** Periodically rebalances the portfolio based on predefined conditions.

## Dependencies

- `numpy`
- `pandas`
- `yfinance`
- `datapackage`
- `plotly`

## Usage

1. **Installation:**
   - Install the required dependencies using `pip install -r requirements.txt`.

2. **Initialization:**
   - Create an instance of the `StockPortfolioManager` class.
   - Initialize the portfolio with an initial cash amount.

3. **Opening Positions:**
   - Use the `open_position` method to open a new position.
   - Provide the stock ticker, quantity/amount, position type, and other optional parameters.

4. **Rebalancing:**
   - Call the `rebalance_portfolio` method to rebalance the portfolio periodically.
   - This function checks stop-loss conditions, executes limit orders, and updates the portfolio.

5. **Closing Positions:**
   - Use the `close_position` method to close an open position.
   - Provide the stock ticker to close the corresponding position.

6. **Printing Status:**
   - Call the `print_status` method to print the current status of the portfolio.
   - This includes allocation percentage, cash available, net profit/loss, and profit/loss percentage.

## Example Usage

```python
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
