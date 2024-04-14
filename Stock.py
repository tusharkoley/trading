import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

class Time:    
    @staticmethod
    def validate_datetime(p_time):

        if p_time!=None and type(p_time)!=datetime:
            return False
        return True

    @staticmethod
    def extract_period_details(period):

        if period[-1].lower()=='y':           
            return relativedelta(years=int(period[:-1]))                

        if period[-1].lower()=='m':
            return relativedelta(months=int(period[:-1]))

        elif period[-1].lower()=='d':        
            return relativedelta(days==int(period[:-1]))

        else:               
            print('Please enter correct period values')
            return None

    @staticmethod
    def generate_start_end_period(period='1Y', start_time=None, end_time=None):

        if not Time.validate_datetime(start_time):
            print('Please enter the corrcet start time format')
            return None
        if not Time.validate_datetime(end_time):
            print('Please enter the corrcet end time format')
            return None    

        if start_time!=None and end_time!=None:
            return (start_time, end_time)    

        if Time.extract_period_details(period)==None:
            print("Please enter the corrcet end time")
            return None

        if start_time!=None:                       
            return start_time,(start_time + Time.extract_period_details(period))

        return (datetime.today() - Time.extract_period_details(period),datetime.today())


class PriceData(object):
       
    def __init__(self) -> None:         
          self.price = pd.DataFrame()

    def __get__(self, obj, objtype):
          self.ticker = getattr(obj, 'ticker')
          self.start_time = getattr(obj, 'start_time')
          self.end_time = getattr(obj, 'end_time')
          print(f'getting the latest price infomation for {self.ticker} from strting time {self.start_time} to {self.end_time}')
          self.price = self.get_latest_price(self.ticker, self.start_time, self.end_time)
          
          return self.price
    
    def __set__(self,obj, value):
          print('Setting the new price')
          self.price = value

    def get_latest_price(self, ticker, start_time, end_time):
          data = yf.download(tickers=ticker, start=start_time, end=end_time) 
          return data


class EPS:
     def __init__(self) -> None:         
          self.eps = pd.DataFrame()

    def __get__(self, obj, objtype):
          self.ticker = getattr(obj, 'ticker')
          self.start_time = getattr(obj, 'start_time')
          self.end_time = getattr(obj, 'end_time')
         
          
          return self.eps
    
    def __set__(self,obj, value):
          print('Setting the new price')
          self.price = value

    def get_latest_eps_info(self, ticker, start_time, end_time):
          data = yf.download(tickers=ticker, start=start_time, end=end_time) 
          return data
     


class Stock(object):

    def __init__(self, ticker, period='1Y', start_time=None, end_time=None) -> None:
            self.ticker = ticker 
            
            (self.start_time,
             self.end_time) = Time.generate_start_end_period(period, start_time,end_time)
   

    price = PriceData()

    
##### Script Strating prosition ######

stock = Stock('AAPL', end_time=datetime.today())

price = stock.price
print('*****', price.shape)
print(stock.ticker)


