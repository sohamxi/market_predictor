#!/usr/bin/env python

import sys
import subprocess as sp
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import time
import datetime
import os
import csv

coin_sym = ["BTC","ETH","XRP"]
coin_status_colnames = ["highest_bid","lowest_ask","last_traded_price","min_24hrs","max_24hrs","vol_24hrs","currency_full_form","per_change","trade_volume"]
df_colnames = ['NAME','INDICATOR','BID_HIGHEST','ASK_LOWEST','TRADED_PRICE','MAX(24H)','MIN(24H)','% CHANGE','VOLUME','VOL(24H)','TIMESTAMP']

class PriceTracker:

    def __init__(self):
        self.price = {}
        self.koinex_details = {}

    def get_current_price(self):
        reply = requests.get('https://koinex.in/api/ticker')
        if reply.status_code != 200:
            raise Exception("Cannot connect to Koinex Ticker API - Check internet connection")
        else:
            self.koinex_details = reply.json()['stats']["inr"]
            self.price = reply.json()['prices']["inr"]
        now = datetime.datetime.now()
        self.now = now - datetime.timedelta(minutes=now.minute % 1,
                               seconds=now.second,
                               microseconds=now.microsecond)

class CoinTracker(PriceTracker):
    def __init__(self,coinName):
        super().__init__()
        self.coinName=coinName
        self.file_name=f'CoinData_{coinName}.csv'

    def create_df(self):
        self.df_str=json_normalize(data=self.koinex_details[self.coinName],meta=coin_status_colnames)
        self.df_str["TIME"]=self.now
        print(self.df_str)

    def update_file(self):
        prel_list=self.df_str.values.tolist()
        with open(self.file_name,mode='a',newline='') as file:
            ### Enable the below only when writing headers for the first time
            # dictwriter=csv.DictWriter(file,fieldnames=df_colnames)
            # dictwriter.writeheader()
            writer=csv.writer(file, delimiter=',')
            writer.writerows([i for i in prel_list])

    def show_details(self):
        print(self.df_str)

if __name__ == "__main__":
    coinlist=["XRP","BTC"]
    for coin in coinlist:
        new_track = CoinTracker(coin)
        new_track.get_current_price()
        new_track.create_df()
        new_track.update_file()
        #new_track.show_details()