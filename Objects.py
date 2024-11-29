import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_daq as daq
import random
from dash import Dash, dcc, html, Input, Output, callback

# define custom legend for the histogram
Legend_Hist = dbc.Checklist(
                            id="Legend_Hist", value=[0, 1],
                            #labelStyle={"display": "flex", "align-items": "right"},
                            )   

# upload the scatter plot data sets
df_scatter = pd.read_csv('df_test.csv',index_col='index')

# upload MLP and histogram data sets
df_shortlist = pd.read_csv('df_shortlist.csv',index_col='index')
df_shortlist_scaled = pd.read_csv('df_shortlist_scaled.csv',index_col='index')

df_probs = pd.read_csv('df_probs_2022.csv',index_col='index')
df_metrics = pd.read_csv('df_metrics_2022.csv',index_col='index')

# define features
Features = df_scatter.drop(columns=['Event','totalWeight']).columns.to_list()
featX = 'ETmiss'
# define events
Events_sim = df_scatter["Event"].unique() 
Events_real = Events_sim.copy()
Events_real[-1] = 'unknown'

Pallete_legend = ['SkyBlue','Salmon','LimeGreen','SandyBrown','RoyalBlue']