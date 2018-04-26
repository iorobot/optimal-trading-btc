# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:03:03 2018

@author: ciofo
"""
from bittrex import *



api_key = "052190d3574148a9b3404136cef818ce"
api_secret = "b71d9f6528c444cfb9d5e9b16b3c9373"

my_bittrex = Bittrex(api_key, api_secret)

print my_bittrex.get_balance('ETH')