from VisualisationTools import *
from Objects import *

NN = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dark_theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


#####################################################################################
#####################################################################################
## Scatter plot components

# defines radioitems group to choose Y-feature
Y_options = Features.copy()
Y_options.remove(featX)
ChooseY = dbc.RadioItems(id='ChooseY',
                         options=Y_options,
                         value = "dRll",
                         style={'font-family':'Coustard Black', 'font-size':12, 'color':'SteelBlue'}, 
                        )


# define slider controls along X
min_value = round(df_scatter[f'{featX}'].min(), 2)
max_value = round(df_scatter[f'{featX}'].max(), 2)
SliderX = dcc.RangeSlider(id='SliderX',
                          min=min_value, 
                          max=max_value,
                          value = [min_value, max_value],
                          #updatemode='drag',
                          persistence = True 
                          )



# define slider controls along Y
SliderY = dcc.RangeSlider(id='SliderY',                          
                          min=0, max=1,
                          vertical=True, verticalHeight=400,
                          #updatemode='drag',
                          persistence=True
                          )


# define tabs
Tabs = dbc.Tabs([dbc.Tab(label="Simulated data", tab_id="tab-0"),
                 dbc.Tab(label="Experimental data", tab_id="tab-1")],
                 id="Tabs",
                 active_tab="tab-0",
                 style={'font-family':'Coustard Black', 'font-size':14},
                )


# define events' checklist
Legend_Scat = dbc.Checklist(
                            id="Legend_Scat", value=Events_sim,
                            #labelStyle={"display": "flex", "align-items": "right"},
                            )  


#####################################################################################
#####################################################################################
## Neural Network model components


# data selector
Shortlist = []  # [{'label':'All Data', 'value':'data'}]
for i in df_shortlist.index:
    single_option = {}
    single_option['label']=f'{i} - '+df_shortlist.Event[i]
    single_option['value']=i
    Shortlist.append(single_option)
Data_Dropdown = dcc.Dropdown(id='Data_Dropdown',
                             options = Shortlist,
                             optionHeight=18,
                             clearable = False,
                             maxHeight = 500,
                             style={'font-family':'Coustard Black', 'font-size':10, 'color':'SlateGrey'}
                            )


# scaler switch
Scaler_Switch = daq.BooleanSwitch(id='Scaler_Switch',
                                  on=False, 
                                  labelPosition="bottom",
                                  #vertical=True, #persistence=True 
                                  )

# power button
Power_Button = daq.PowerButton(id='Power_Button',
                               on=False,
                               color=dark_theme['primary'],                
                               )

# number of hidden layers selector
NN_Depth = dbc.RadioItems(id='NN_Depth', 
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
HL1_Gauge = daq.Gauge(id='HL1_Gauge',
                      color={"gradient":True, "ranges":{'white':[0,1],"palegreen":[1,4],"limegreen":[4,8],"darkgreen":[8,10]}},
                      max=10, min=0, size=130, 
                      label=dict(label='Size of Layer 1', style={'font-size':10, 'marginBottom': 0, 'color':'Navy'}),                      
                      style={'font-family':'ROG Fonts'},
                      scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-size':8}} for i in range(1,11)})
                      )
HL1_Selector = daq.Slider(id='HL1_Selector',
                          min=1, max=10, value=4, step=1, size=130,
                          handleLabel=dict(label="neurons", color='DarkGreen'),  
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          color={"gradient":True, "ranges":{"palegreen":[1,5],"limegreen":[5,9],"darkgreen":[9,10]}},
                          )
# selector for Hidden Layer 2
HL2_Gauge = daq.Gauge(id='HL2_Gauge',                        
                      max=10, min=0, size=130,
                      scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11)}),
                      style={'font-family':'ROG Fonts'}
                      )
HL2_Selector = daq.Slider(id='HL2_Selector',
                          min=1, max=10, value=8, size=130,
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          )
# selector Hidden Layer 3
HL3_Gauge = daq.Gauge(id='HL3_Gauge',                        
                      max=10, min=0, size=130,
                      scale=dict(custom={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11)}),
                      style={'font-family':'ROG Fonts'}
                      )
HL3_Selector = daq.Slider(id='HL3_Selector',
                          min=1, max=10, value=4, size=130,                          
                          marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'ROG Fonts', 'font-size':8}} for i in range(1,11,9)},
                          )

# accuracy indicator
Accuracy_LED = daq.LEDDisplay(id='Accuracy_LED',
                              size=35,
                              color=dark_theme['primary'],
                              backgroundColor='white', #dark_theme['secondary'],
                              label=dict(label='Accuracy:', 
                                  style={'color':'Navy', 'font-size':11, 'font-family':'ROG Fonts', }),
                              )
F1_LED = daq.LEDDisplay(id='F1_LED',
                        size=35,
                        color=dark_theme['primary'],
                        backgroundColor='white', #dark_theme['secondary'],
                        label=dict(label='F1-score:', 
                                  style={'color':'Navy', 'font-size':11, 'font-family':'ROG Fonts', }),
                        )

#####################################################################################
#####################################################################################
## Histogram components


# slider controling histogram cut
Hist_Slider = daq.Slider(id='Hist_Slider',
                          min=0, max=1, value=0., step=0.05,
                          size=497,
                          #marks={f'{i}':{'label':f'{i}', 'style':{'font-family':'Coustard', 'font-size':8}} for i in [0,.5,1.]},
                          updatemode = 'drag',                          
                          labelPosition='bottom',                          
                          )

# Label showing significance value    
Signif_Hist = dbc.Label(id='Signif_Hist', 
                       style={'font-size':26, 'font-family':'Coustard Black'})


####################################################################################################################################################
####################################################################################################################################################
## App layout


NN.layout = dbc.Container([
    
    #####################  Scatter plot section ############################################    
    
    html.Br(),
    dbc.Row(dbc.Col(html.H4('When cut-optimisation is struggling...',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),
    html.Br(),
    dbc.Row(dbc.Col(
                    dcc.Markdown(
                          "In some cases, bold cut-optimisation approach can be challenging. \
                          Suppose we are searching for a *dark matter* particle among results of a proton-proton collision. \
                          We assume that *dark matter* is made of hypothetical particles - WIMPs (weakly interacting massive particles). \
                          They are produced when Z-boson decays into a pair of WIMPs and a dilepton pair. \
                          Such event would leave traces similar to other processes, which we know do happen. \
                          On a graph below, try to play with different combinations of parameters. \
                          As you may find, the dark matter traces can be easily distinguished from **Non-resonant dilepton** and **Z+jets** processes. \
                          However, **WZ** and **ZZ** events have such large variety, that they practically hinder the other processes.",

                          style={'font-size':14, 'font-family':'Coustard'}),
                          
                    width={"size": 8, "offset": 2})),

    dbc.Row([
            dbc.Col([
                      dbc.Label('Select Y-parameter:',
                                style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}), 
                      ChooseY,
                      ], 
                    width={"size": 2, "offset": 0},
                    style={'marginTop':100},
                    align='start'
                    ),
            dbc.Col(SliderY, 
                      width={"size": 1, "offset": 0},
                      style={'width':50,
                            'margin-left':20, 'marginBottom':58},
                      align='end'
                      ),
            dbc.Col([
                    dbc.Col([Tabs,
                            dcc.Graph(id="Scatter",                                      
                                      config={
                                              'displayModeBar':False,
                                              #'modeBarButtonsToRemove': ['zoom2d'],
                                              #'scrollZoom': True,
                                              }                            
                                      ),
                            ]),
                    dbc.Col(SliderX, 
                            style={
                                  'width':630, 
                                  'margin-left':15}),                                
                      ],
                    width={"size": 7, "offset": 0}, #, md=7)
                    ),
            dbc.Col([
                     #dbc.Label('Events:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     Legend_Scat,
                     ], 
                    width={"size": 2, "offset": 0},
                    style={'marginTop':145, 'marginLeft':5},
                    align='start'
                    ) 
            ],
            align="center",
            className="g-0",                   
            ), 

    html.Br(),
    dbc.Row(dbc.Col([
            dcc.Markdown("For convenience, we can approximate our complex 10-dimensional data set to a 2D projection. \
                         Popular algorithms for such visualisation are UMAP, PCA and t-SNE (check the tabs). \
                         Now there is no need to go through multiple combinations of parameters. \
                         However, the setback is that we sacrificied data variance.\
                         And still hardly can isolate the signal (Dark Matter) by optimising the cut(s).",

                         style={'font-size':14, 'font-family':'Coustard'}),
            html.Br(),
            dcc.Markdown("Imagine there are not 10, but 40+ parameters to consider... In such case machine learning inventory can come handy. \
                         Machine learning algorithms are capable of identifying (very) complex patterns and classifying the Signal (dark matter) from the Background (the other events). \
                         Among different algorithms, *neural networks* (NN) often produce the best results in HEP. \
                         Below you can find a model of NN: Multilayer Perceptron (MLP). \
                         It is pre-trained on Monte Carlo simulated data, and you can tinker with its configuration to check the difference in output. \
                         Select the number of hidden layers (NN depth) and vary the amount of neurons. \
                         Then, choose a specific event from the dropdown menu and press the *power button*. \
                         But don't forget to turn on the *scaler switch* - NN work best with normalised data.",

                         style={'font-size':14, 'font-family':'Coustard'}),
                    ],                                        
                     width={"size": 8, "offset": 2})),
    html.Br(),   

    ####################################################################
    #####################  NN model section ############################

    dbc.Row(dbc.Col(html.H4('Play with Neural Network design',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    html.Hr(),
    dbc.Row([
        dbc.Col([dbc.Card([dbc.Label('Select event:',
                                    style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'}),
                        #html.Hr(),
                        daq.DarkThemeProvider(theme=dark_theme, children=Data_Dropdown)], body=True),
                dbc.Row([dbc.Col(dbc.Card([html.Center(dbc.Label('Scale data:',
                                                     style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                                          daq.DarkThemeProvider(theme=dark_theme, children=Scaler_Switch)], body=True)),
                        dbc.Col(dbc.Card([html.Center(dbc.Label('Start NN:',
                                                    style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                                          daq.DarkThemeProvider(theme=dark_theme, children=Power_Button)], body=True))]),
                ],
                width=3),
    
        dbc.Col(dbc.Card([
                dbc.Row(dbc.Col([html.Center(dbc.Label('Number of Hidden Layers:',
                                            style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                #html.Br(),
                                html.Center(NN_Depth)], 
                                width='auto'), 
                        justify='center'),
                html.Br(),
                dbc.Row([
                        dbc.Col([HL1_Gauge, 
                                 html.Center(HL1_Selector)],                                               
                                width='auto'),                                        
                        dbc.Col([HL2_Gauge,
                                 html.Center(HL2_Selector)],
                                width='auto'),
                        dbc.Col([HL3_Gauge, 
                                 html.Center(HL3_Selector)], 
                                width='auto')
                        ], justify='evenly'),
                    ], body=True),
                width={"size": 7, "offset": 0}),                    

        dbc.Col([dbc.Card([Accuracy_LED,
                            html.Br(),
                            F1_LED], 
                            body=True),
                            #daq.DarkThemeProvider(theme=dark_theme, children=Accuracy_LED)], body=True),
                ],
                width=2),
            ], align='center'),
    
    # Sankey diagramm section
    dbc.Row(
            dbc.Col(dcc.Graph(id="MLP", config={'displayModeBar':False}),
                    #width={"size": 10, "offset": 1}
                    )
            ),

    ####################################################################
    #####################  Histogram section ###########################


    dbc.Row([dbc.Col([
                    dbc.Col(dcc.Graph(id="Hist", config={'displayModeBar':False}),
                            ),
                    html.Br(),
                    dbc.Col(Hist_Slider, 
                            style={'margin-left':104}),                             
                    ],
                    width={"size": 6, "offset": 2}),
            dbc.Col([
                     dbc.Label('Events:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     Legend_Hist,
                     html.Br(),
                     dbc.Label('Significance:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     html.Br(),
                     dbc.Col(Signif_Hist, style={'margin-left':50})
                     ],
                    width={"size": 2, "offset": 0},
                    style={'margin-top':60},
                    align='start')
            ],
            align='center'),

    # text after the histogram
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col([
                    dcc.Markdown(
                            'Histogram above shows distribution of the NN outputs of the whole data set. \
                            Move the slider to select the (signal) data to the right cutting out (background) data to the left',

                            style={'font-size':14, 'font-family':'Coustard'}),

                            ], width={"size": 8, "offset": 2}),
                    align='center'),
    html.Br(),
    html.Br(),
    ])

NN.run_server(debug=True, port=7777)