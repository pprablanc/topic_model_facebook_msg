#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

def extract_fb_msg(url):

    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # tag
    tag_date = "_3-94 _2lem".split()
    tag_name = "_3-96 _2pio _2lek _2lel".split()
    tag_message = "_2let".split()
    tag_full = tag_date + tag_name + tag_message
    
    # extraction
    full_html = soup.find_all("div", class_= tag_full)
    full = [elt.get_text() for elt in full_html]

    # dataframe shape
    table = [{'name': full[i], 'message': full[i+1], 'date': full[i+2]} for i in range(0, len(full) - 2, 3)]
    df = pd.DataFrame(table)
    return df
