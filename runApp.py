import os.path
from pathlib import Path 

FilesExist = True
idir = Path("build/") 
if not os.path.isdir("build"):
    idir.mkdir()

for ifile in ["df_2022", "df_test", "df_shortlist", "df_shortlist_scaled", "df_probs_2022", "df_metrics_2022"]:
    FilesExist = os.path.isfile("build/"+ifile+".csv")

if not FilesExist:
    import source.RegenerateModels as RegMod
    RegMod.Run()

from source.DashComponents import *

NN = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                      UI_objects.ChooseY,
                      ], 
                    width={"size": 2, "offset": 0},
                    style={'marginTop':100},
                    align='start'
                    ),
            dbc.Col(UI_objects.SliderY, 
                      width={"size": 1, "offset": 0},
                      style={'width':50,
                            'margin-left':20, 'marginBottom':58},
                      align='end'
                      ),
            dbc.Col([
                    dbc.Col([UI_objects.Tabs,
                            dcc.Graph(id="Scatter",                                      
                                      config={
                                              'displayModeBar':False,
                                              #'modeBarButtonsToRemove': ['zoom2d'],
                                              #'scrollZoom': True,
                                              }                            
                                      ),
                            ]),
                    dbc.Col(UI_objects.SliderX, 
                            style={
                                  'width':630, 
                                  'margin-left':15}),                                
                      ],
                    width={"size": 7, "offset": 0}, #, md=7)
                    ),
            dbc.Col([
                     #dbc.Label('Events:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     UI_objects.Legend_Scat,
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
                        daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Data_Dropdown)], body=True),
                dbc.Row([dbc.Col(dbc.Card([html.Center(dbc.Label('Scale data:',
                                                     style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                                          daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Scaler_Switch)], body=True)),
                        dbc.Col(dbc.Card([html.Center(dbc.Label('Start NN:',
                                                    style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                                          daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Power_Button)], body=True))]),
                ],
                width=3),
    
        dbc.Col(dbc.Card([
                dbc.Row(dbc.Col([html.Center(dbc.Label('Number of Hidden Layers:',
                                            style={'font-size':11, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                #html.Br(),
                                html.Center(NN_display.NN_Depth)], 
                                width='auto'), 
                        justify='center'),
                html.Br(),
                dbc.Row([
                        dbc.Col([NN_display.HL1_Gauge, 
                                 html.Center(NN_display.HL1_Selector)],                                               
                                width='auto'),                                        
                        dbc.Col([NN_display.HL2_Gauge,
                                 html.Center(NN_display.HL2_Selector)],
                                width='auto'),
                        dbc.Col([NN_display.HL3_Gauge, 
                                 html.Center(NN_display.HL3_Selector)], 
                                width='auto')
                        ], justify='evenly'),
                    ], body=True),
                width={"size": 7, "offset": 0}),                    

        dbc.Col([dbc.Card([NN_display.Accuracy_LED,
                            html.Br(),
                            NN_display.F1_LED], 
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
                    dbc.Col(UI_objects.Hist_Slider, 
                            style={'margin-left':104}),                             
                    ],
                    width={"size": 6, "offset": 2}),
            dbc.Col([
                     dbc.Label('Events:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     UI_objects.Legend_Hist,
                     html.Br(),
                     dbc.Label('Significance:', style={'font-size':16, 'marginBottom':20, 'font-family':'Coustard Black', 'color':'DimGray'}),
                     html.Br(),
                     dbc.Col(UI_objects.Signif_Hist, style={'margin-left':50})
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
