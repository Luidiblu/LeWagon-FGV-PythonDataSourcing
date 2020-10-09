#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 18:34:32 2020

@author: Diego Pisani
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib
import re

page_number = 1

movies_dict = {
        "Title": [],
        "Year": [],
        "Duration": []
        }

while page_number != 201:

    url = f'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start={page_number}'

    response = requests.get(url)

    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    movies = soup.find_all("div", class_="lister-item-content")

    for movie in movies:
      title = movie.find("h3").find("a").string

      year = movie.find("span", class_="lister-item-year")
      
      year = re.search(r"\d{4}", str(year)).group(0)
      
      duration = int(movie.find("span", class_="runtime").string.strip(' min'))
      
      movies_dict['Title'].append(title)
      
      movies_dict['Year'].append(int(year))
      
      movies_dict['Duration'].append(duration)

    page_number += 50


dataframe = pd.DataFrame.from_dict(movies_dict)

dataframe["Duration"].hist()

print(dataframe[dataframe["Duration"] >= 60 * 3])
