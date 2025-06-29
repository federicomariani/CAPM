import pandas as pd
import seaborn as sns
import plotly.express as px
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
from jupyterthemes import jtplot # Jupyter theme

jtplot.style(theme = 'monokai', context= 'notebook', ticks= True, grid= False)

stocks_df = pd.read_csv("stocks_dataset.csv")

def normalize(df):
    x = df.copy()
    for i in x.columns[1:]:
        x[i] = x[i]/x[i][0]
    return x

def interactive_plot(df, title):
    pio.renderers.default = "browser"
    fig = px.line(title = title)
    for i in df.columns[1:]:
        fig.add_scatter(x = df["Date"], y = df[i], name = i)
    fig.show()

interactive_plot(normalize(stocks_df), "Normalized Prices")

def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j] - df[i][j-1])/df[i][j-1])*100
        df_daily_return[i][0] = 0
    return df_daily_return

stocks_daily_return = daily_return(stocks_df)

for i in stocks_daily_return.columns:
  pio.renderers.default = "browser"
  if i != 'Date' and i != 'sp500':
    fig = px.scatter(
        stocks_daily_return, 
        x = 'sp500', 
        y = i, 
        title = f"{i} vs S&P500",
        template = "plotly_dark"
        ) #Chart
    fig.update_traces(marker = dict(color = "white")) #Dots color
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[i], 1)
    fig.add_scatter(
        x = stocks_daily_return['sp500'], 
        y = b*stocks_daily_return['sp500'] + a,
        mode = "lines",
        line = dict(color = "blue", width = 3),
        name = "Regression Line"
        ) #Regression Line 
    fig.update_layout(
        plot_bgcolor = "black",
        paper_bgcolor = "black",
        xaxis = dict(showgrid = False),
        yaxis = dict(showgrid = False)
        ) #Grid disabled 
    fig.show()
