import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_daq as daq
import os

from dash import Dash, dcc, html, Input, Output, callback


class UIObjects:
    def __init__(self):
        self.dark_theme = {
            'dark': True,
            'detail': '#007439',
            'primary': '#00EA64',
            'secondary': '#6E6E6E',
        }


        # define custom legend for the histogram
        self.Legend_Hist = dbc.Checklist(
                               id="Legend_Hist", value=[0, 1],
                             #labelStyle={"display": "flex", "align-items": "right"},
                                )   

        self.Pallete_legend = ['SkyBlue','Salmon','LimeGreen','SandyBrown','RoyalBlue']

        DB = DataBackend()
        self.Features = DB.df_scatter.drop(columns=['Event','totalWeight']).columns.to_list()
        self.featX = 'ETmiss'

        self.Events_sim = DB.df_scatter["Event"].unique()
        self.Events_real = self.Events_sim.copy()

        self.Events_real[-1] = "unknown"

    ########## Scatter plot components ##########
        # defines radioitems group to choose Y-feature
        self.Y_options = self.Features.copy()
        self.Y_options.remove(self.featX)
        self.ChooseY = dbc.RadioItems(id='ChooseY',
                         options=self.Y_options,
                         value = "dRll",
                         style={'font-family':'Coustard Black', 'font-size':12, 'color':'SteelBlue'}, 
                        )

        min_value = round(DB.df_scatter[f'{self.featX}'].min(), 2)
        max_value = round(DB.df_scatter[f'{self.featX}'].max(), 2)
        self.SliderX = dcc.RangeSlider(id='SliderX',
                          min=min_value, 
                          max=max_value,
                          value = [min_value, max_value],
                          #updatemode='drag',
                          persistence = True 
                          )

        self.SliderY = dcc.RangeSlider(id='SliderY',                          
                          min=0, max=1,
                          vertical=True, verticalHeight=400,
                          #updatemode='drag',
                          persistence=True
                          )
    ##### Def tabs ####
        self.Tabs = dbc.Tabs([dbc.Tab(label="Simulated data", tab_id="tab-0"),
                    dbc.Tab(label="Experimental data", tab_id="tab-1")],
                    id="Tabs",
                    active_tab="tab-0",
                    style={'font-family':'Coustard Black', 'font-size':14},
                            )
    #### Def events' checklist ######
        self.Legend_Scat = dbc.Checklist(
                            id="Legend_Scat", value=self.Events_sim,
                            #labelStyle={"display": "flex", "align-items": "right"},
                            ) 

    ### Histogram components ##
        self.Hist_Slider = daq.Slider(id='Hist_Slider',
                        min=0, max=1, value=0., step=0.05,
                        size=497,
                        #marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'Coustard', 'font-size':8}} for i in [0,.5,1.]},
                        updatemode = 'drag',                          
                        labelPosition='bottom',                          
                        )

    # Label showing significance value    
        self.Signif_Hist = dbc.Label(id='Signif_Hist', 
                       style={'font-size':26, 'font-family':'Coustard Black'})


class NNDisplay:
    def __init__(self):
        DB = DataBackend()
        UIO = UIObjects ()

        Shortlist = []  # [{'label':'All Data', 'value':'data'}]
        for i in DB.df_shortlist.index:
            single_option = {}
            single_option['label']=f'{i} - '+DB.df_shortlist.Event[i]
            single_option['value']=i
            Shortlist.append(single_option)
        self.Data_Dropdown = dcc.Dropdown(id='Data_Dropdown',
                                options = Shortlist,
                                optionHeight=18,
                                clearable = False,
                                maxHeight = 500,
                                style={'font-family':'Coustard Black', 'font-size':10, 'color':'SlateGrey'}
                                )

        # self.Scaler_Switch = daq.BooleanSwitch(id='Scaler_Switch',
        #                           on=False, 
        #                           labelPosition="bottom",
        #                           #vertical=True, #persistence=True 
        #                           )

        self.Power_Button = daq.PowerButton(id='Power_Button',
                                    on=False,
                                    color=UIO.dark_theme['primary'],                
                                    )

        # number of hidden layers selector
        self.NN_Depth = dbc.RadioItems(id='NN_Depth', 
                                options=[1,2,3], 
                                value=1,
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                #style={'size':'md'},
                                inline=True,                
                                )

        # selector for Hidden Layer 1
        self.HL1_Gauge = daq.Gauge(id='HL1_Gauge',
                          color={"gradient":True, "ranges":{'white':[0,1],"palegreen":[1,4],"limegreen":[4,8],"darkgreen":[8,10]}},
                          max=10, min=0, size=130, 
                          label=dict(label='Size of Layer 1', style={'font-size':10, 'marginBottom': 0, 'color':'Navy'}),                      
                          style={'font-family':'ROG Fonts'},
                          scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-size':8}} for i in range(1,11)})
                          )

        self.HL1_Selector = daq.Slider(id='HL1_Selector',
                          min=1, max=10, value=4, step=1, size=130,
                          handleLabel=dict(label="neurons", color='DarkGreen'),  
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          color={"gradient":True, "ranges":{"palegreen":[1,5],"limegreen":[5,9],"darkgreen":[9,10]}},
                          )

        # selector for Hidden Layer 2
        self.HL2_Gauge = daq.Gauge(id='HL2_Gauge',                        
                          max=10, min=0, size=130,
                          scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11)}),
                          style={'font-family':'ROG Fonts'}
                          )

        self.HL2_Selector = daq.Slider(id='HL2_Selector',
                          min=1, max=10, value=8, size=130,
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          )

        # selector Hidden Layer 3
        self.HL3_Gauge = daq.Gauge(id='HL3_Gauge',                        
                          max=10, min=0, size=130,
                          scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11)}),
                          style={'font-family':'ROG Fonts'}
                          )

        self.HL3_Selector = daq.Slider(id='HL3_Selector',
                          min=1, max=10, value=4, size=130,                          
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          )

        # accuracy indicator
        self.Accuracy_LED = daq.LEDDisplay(id='Accuracy_LED',
                            size=35,
                            color=UIO.dark_theme['primary'],
                            backgroundColor='white', #dark_theme['secondary'],
                            label=dict(label='Accuracy:', 
                            style={'color':'Navy', 'font-size':11, 'font-family':'ROG Fonts', }),
                            )

        self.F1_LED = daq.LEDDisplay(id='F1_LED',
                            size=35,
                            color=UIO.dark_theme['primary'],
                            backgroundColor='white', #dark_theme['secondary'],
                            label=dict(label='F1-score:', 
                            style={'color':'Navy', 'font-size':11, 'font-family':'ROG Fonts', }),
                            )

class DataBackend:
    def __init__(self):
        self.df_scatter = pd.read_csv('build/scatter_data.csv',index_col='index').drop_duplicates()
        self.df_shortlist = pd.read_csv('build/events_shortlist_MLP.csv',index_col='index').drop_duplicates()
        self.df_metrics = pd.read_csv('build/MLP_metrics.csv',index_col='index').drop_duplicates()
        self.df_probs = pd.read_csv('build/scatter_probs.csv',index_col='index')
