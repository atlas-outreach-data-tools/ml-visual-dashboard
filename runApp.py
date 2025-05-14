import os.path
from pathlib import Path 

FilesExist = True
idir = Path("build/") 
if not os.path.isdir("build"):
    idir.mkdir()

for ifile in ["scatter_probs", "events_shortlist_MLP", "MLP_metrics", "scatter_data", "df_2022"]:
    FilesExist = os.path.isfile("build/"+ifile+".csv")

if not FilesExist:
    import source.RegenerateModels as RegMod
    RegMod.Run()

from source.DashComponents import *
from assets.text import PageHeaders, PageText

NN = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

ATLASLogo = dbc.Card(
    [
        dbc.CardImg(src="assets/atlas_logo.png"),
        #dbc.CardBody(
            #[
                #html.H4("Card title", className="card-title"),
                #html.P(
                    #"Some quick example text to build on the card title and "
                    #"make up the bulk of the card's content.",
                    #className="card-text",
                #),
                #dbc.Button("Go somewhere", color="primary"),
            #]
        #),
    ],
    style={"width": "18rem"},
)
#ATLASLogo = html.Img(src="assets/atlas_logo.png", width=200)

####################################################################################################################################################
####################################################################################################################################################
## App layout


NN.layout = dbc.Container([

   ### Title header and preamble ###
    
    dbc.Row([ 
        dbc.Col(ATLASLogo, width="auto"),
        dbc.Col(html.H1('Visualising machine learning in a search for dark matter',
                        style={'font-family':'Coustard Black', 'color':'DarkSlateGrey', 'marginTop':100}),
                width={"size": 8})
        ]),

    html.Br(),
    dbc.Row(dbc.Col(html.H2('Searching for dark matter',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    dbc.Row(dbc.Col(
                    dcc.Markdown(
                          PageText["DMSearches"],
                          style={'font-size':16, 'font-family':'Coustard'}),
                          
                    width={"size": 8, "offset": 2})),

    #####################  Scatter plot section ############################################    
    
    html.Br(),
    dbc.Row(dbc.Col(html.H3('Why not use cut optimisation?',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),
    dbc.Row(dbc.Col(
                    dcc.Markdown(
                          PageText["CutOptimisation1"],
                          style={'font-size':16, 'font-family':'Coustard'}),
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
    dbc.Row(dbc.Col(
                    dcc.Markdown(PageText["CutOptimisation2"],
                          style={'font-size':16, 'font-family':'Coustard'}),
                          
                    width={"size": 8, "offset": 2})),

    ### Using machine learning ###

    html.Br(),
    dbc.Row(dbc.Col(html.H2('Using machine learning',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    dbc.Row(dbc.Col([
            dcc.Markdown(PageText["MLInfo1"],
                         style={'font-size':16, 'font-family':'Coustard'}),

            dcc.Markdown(PageText["MLInfo2"],
                         style={'font-size':16, 'font-family':'Coustard'}),
                    ],                                        
                     width={"size": 8, "offset": 2})),
    html.Br(),   

    ####################################################################
    #####################  NN model section ############################

    dbc.Row(dbc.Col(html.H3('Play with Neural Network design',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    html.Hr(),
    dbc.Row([
        dbc.Col([dbc.Card([dbc.Label('Select event:',
                                    style={'font-size':16, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'}),
                        #html.Hr(),
                        daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Data_Dropdown)], body=True),
                dbc.Row([dbc.Col(dbc.Card([html.Center(dbc.Label('Power on:',
                                                     style={'font-size':16, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                        #                   daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Scaler_Switch)], body=True)),
                        # dbc.Col(dbc.Card([html.Center(dbc.Label('Start NN:',
                        #                             style={'font-size':16, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
                                          #html.Hr(),
                                          daq.DarkThemeProvider(theme=UI_objects.dark_theme, children=NN_display.Power_Button)], body=True))]),
                ],
                width=3),
    
        dbc.Col(dbc.Card([
                dbc.Row(dbc.Col([html.Center(dbc.Label('Number of Hidden Layers:',
                                            style={'font-size':16, 'marginBottom':20, 'font-family':'ROG fonts', 'color':'Navy'})),
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
    html.Br(),
    dbc.Row(dbc.Col(html.H3('Which design is best?',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    dbc.Row(dbc.Col(dcc.Markdown(PageText["DesignOptimise"],
                          style={'font-size':16, 'font-family':'Coustard'}),     
                    width={"size": 8, "offset": 2})),

    html.Br(),
    dbc.Row(dbc.Col(html.H2('How do we use our machine learning output? ',
                            style={'font-family':'Coustard Black', 'color':'DarkSlateGrey'}),
                    width={"size": 8, "offset": 2})),

    ## Insert description on how to use ML outputs 
    dbc.Row([dbc.Col([
                    dbc.Col(dcc.Graph(id="Hist", config={'displayModeBar':False, 
                                                        'edits':{'shapePosition':True}
                                                        }),
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
    dbc.Row(dbc.Col([
                    dcc.Markdown(
                            PageText["UsingMLOut"],
                            style={'font-size':16, 'font-family':'Coustard'}),

                            ], width={"size": 8, "offset": 2}),
                    align='center'),
    html.Br(),
    html.Br(),
    ])

NN.run_server(host="0.0.0.0", debug=True, port=8080)
