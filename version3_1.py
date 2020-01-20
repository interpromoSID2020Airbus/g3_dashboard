#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import json
import re
from collections import Counter
import os
import cx_Oracle
from wordcloud import WordCloud, STOPWORDS
import base64
import Find_Areas as fa

##########################################################
##########################################################
# CONNECTION BASE DE DONNEE ##############################


os.chdir("C:\\Oracle\\instantclient_19_5")
ORACLE_CONNECT = "rll2373a/Alice1234@(DESCRIPTION=(SOURCE_ROUTE=OFF)(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=telline.univ-tlse3.fr)(PORT=1521)))(CONNECT_DATA=(SID=etupre)))"
mydb = cx_Oracle.connect(ORACLE_CONNECT)

mycursor = mydb.cursor()
###REQUETE TABLE PAR DEFAULT###

mycursor.execute('''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger''')



###############################

myresult = mycursor.fetchall()
myresult
defaultDF=pd.DataFrame(myresult, columns=['Airline', 'Manufacturer', 'Aircraft', 'Category',
                                    'Flight_Type','Seat_Type', 'Power_Available',
                                    'Seat_Position',
                                    'Overall_Customer_Rating','Cleanliness', 'Catering',
                                    'Inflight_Entertainment', 'Cabin_Staff_Service',
                                    'Seat_Comfort', 'Origin', 'Date',
                                    'Type_of_Traveller', 'Recommended'])


# 2-Création tableau / Graph pour nombre de vol ########
fig_nb_vol = go.Figure()
features_nb_vol = ['Airline', 'Manufacturer', 'Aircraft','Origin']

opts = [{'label': i_opts,
         'value': i_opts} for i_opts in features_nb_vol]


# 3-Création Tableau / Pie Chart type vol
fig_type_f = go.Figure()


# 4-Création Tableau / Pie Chart satisfaction generale
fig_type_la = go.Figure()


# 5-Création tableau / Satisfaction globale critères qualitatifs
fig_bar_sat = go.Figure()
features_bar_sat =['Airline', 'Manufacturer', 'Aircraft','Seat_Type', 'Power_Available']


opt_bar_sat = [{'label': i_opt_bar_sat,
                'value': i_opt_bar_sat} for i_opt_bar_sat in features_bar_sat]


# 6-Création tableau / Satisfaction globale critères quantitatifs
fig_scatter_sat = go.Figure()
features_scatter_sat=['Cleanliness', 'Catering','Inflight_Entertainment', 'Cabin_Staff_Service']
opt2 = [{'label': i_opt2,
         'value': i_opt2} for i_opt2 in features_scatter_sat]


#########################################################
#TAB 2
#########################################################

# 8-Création Tableau / Pie Chart type siege
fig_type_s = go.Figure()

# 9-Création Tableau / BoxPlot note selon la position du siege
fig_note_box = go.Figure()


#########################################################
#TAB 3
#########################################################


# 10-Création Tableau / BoxPlot note selon la class/seat_category
fig_note_class = go.Figure()

# 11-Création tableau / seat_comfort X class
fig_scatter_comfort_class = go.Figure()

# 12-Création tableau / type_of_traveller X recommended (empile)
fig_type_reco = go.Figure()

#################
# TAB 4
#################

path_data = 'LAYOUT SEATGURU/'

# Import json
file = 'data_aircraft.json'
with open(file) as json_file:
    data = json.load(json_file)

# List of Aircraft Type
list_aircraft = [key for key in data.keys()]
list_aircraft_clean = []
list_option_aircraft = []
for aircraft in list_aircraft:
    aircraft = aircraft.replace('.svg', '')
    aircraft = aircraft.replace('.png', '')
    aircraft = aircraft.replace('.jpg', '')
    aircraft = aircraft.replace('_', ' ')
    aircraft = re.sub("(plane\w+)", "", aircraft)
    list_aircraft_clean.append(aircraft)
    list_option_aircraft.append({'label': aircraft, 'value': aircraft})

# Image plane
image_filename = path_data + list_aircraft[0]
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Initialize tag area
def initialize_tag():
    list_tag_area = []
    for i in range(0, 400):
        list_tag_area.append(html.Area(id=str(i)))
    return list_tag_area


# Create Scatter
fig_scatter = go.Figure()

##################################################
##############VALEUR DES FILTERS
###################################################

mycursor = mydb.cursor()
mycursor.execute('''SELECT S1.airline_name
                    FROM ( SELECT S2.airline_name
                           FROM SEAT S2
                           GROUP BY S2.airline_name
                           ORDER BY Count(S2.airline_name) DESC ) S1
                    WHERE ROWNUM <= 150''')
myresult2 = mycursor.fetchall()


mycursor = mydb.cursor()
mycursor.execute('''SELECT R.manufacturer_name
                    FROM ( SELECT S.manufacturer_name
                           FROM SEAT S
                           GROUP BY S.manufacturer_name
                           ORDER BY Count(S.manufacturer_name) DESC ) R
                    WHERE ROWNUM <= 10''')
myresult3 = mycursor.fetchall()


mycursor = mydb.cursor()
mycursor.execute('''SELECT R.aircraft_type
                    FROM ( SELECT S.aircraft_type
                           FROM SEAT S
                           GROUP BY S.aircraft_type
                           ORDER BY Count(S.aircraft_type) DESC ) R
                    WHERE ROWNUM <= 150''')
myresult4 = mycursor.fetchall()

###############################


defaultDF1=pd.DataFrame(myresult2, columns=['Airline'])
defaultDF2=pd.DataFrame(myresult3, columns=['Manufacturer'])
defaultDF3=pd.DataFrame(myresult4, columns=['Aircraft'])

filt_comp = defaultDF1['Airline']
opt_comp = [{'label': i, 'value': i} for i in filt_comp]

filt_manu = defaultDF2['Manufacturer']
opt_manu = [{'label': i, 'value': i} for i in filt_manu]

filt_type = defaultDF3['Aircraft']
opt_type = [{'label': i, 'value': i} for i in filt_type]

########################################################


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {'background': '#111111',
          'text': '#7FDBFF',
          'filtre':'#071e4a',
          'blanc': '#ffffff'}

app = dash.Dash(__name__, external_stylesheets=[
                'https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap-grid.min.css'])
app.layout = html.Div([
    html.Div(
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Airbus_Logo_2017.svg/1280px-Airbus_Logo_2017.svg.png',
             style={'height': '15%','width': '15%'}),
    style={'textAlign': 'right'}),
    dcc.Tabs([
        dcc.Tab(label='General', id='tab1', children=[
            html.Br(),
            html.Div([
                dbc.Row([
                        # -------DROPDOWNS + DATE PICKER ---------
            dbc.Col(html.Div([html.Label('Filters'),
                              html.Button('Refresh Filters',
                                          id='reset_button')]),
                    width=1),
            dbc.Col(html.Div([html.Label('Airline'),
                              dcc.Dropdown(id='comp_filt',
                    options=opt_comp,
                    multi=False
                    )]), width=2),
            dbc.Col(html.Div([html.Label('Manufacturer'),
                              dcc.Dropdown(id='manu_filt',
                    options=opt_manu,
                    multi=False
                    )]), width=2),
            dbc.Col(html.Div([html.Label('Aircraft Type'),
                              dcc.Dropdown(id='type_filt',
                    options=opt_type,
                    multi=False
                    )]), width=2),
                        
                        ])
            ]),


            ##############################################################
            # ############################ NOUVELLE ROW ##################
            dbc.Row([
                # ####### METTRE AFFICHAGE DES PASSAGERS DANS RONDS #########
                dbc.Col(html.Div([html.Br(),
                                  html.Br(),
                                  html.Br(),
                                  html.I("Number of Evaluations"),
                                  html.Br(),
                                  html.H1(id='nb_passengers')],
                                 style={'text-align': 'center'}), width=6),
                # #### "" GRAPH 1 NUMBER OF FLIGHT + dropdown en abscisse #####
                dbc.Col(html.Div([
                    dcc.Graph(id='plot', figure=fig_nb_vol),

                    html.P([html.Label("Choose a feature"),
                            dcc.Dropdown(
                        id='opt', options=opts, value='Airline')
                    ], style={'width': '400px',
                              'fontSize': '20px',
                              'padding-left': '100px',
                              'display': 'inline-block'})
                ]), width=6),
            ]),

            ##############################################################
            # ############################ NOUVELLE ROW ##################
            dbc.Row([
                # ################# PIE CHART -- TYPE OF FLIGHT PROPORTION ###
                dbc.Col(html.Div([
                    dcc.Graph(id='graph_type_f', figure=fig_type_f),
                ]), width=6),
                # ##############PIE CHART  LABEL_GENERAL PROPORTION ########
                dbc.Col(html.Div([
                    dcc.Graph(id='graph_type_la', figure=fig_type_la),
                ]), width=6),

                # ###FIN ROW ###
            ]),
            ##############################################################
            # ############################ NOUVELLE ROW ##################
            dbc.Row([
                # ## Histogramme qualitatif -- satisfaction
                dbc.Col(html.Div([
                    dcc.Graph(id='bar_sat', figure=fig_bar_sat),
                    html.P([html.Label("Choose a feature"),
                            dcc.Dropdown(id='opt_bar_sat', options=opt_bar_sat,
                                         value='Airline')
                            ], style={'width': '400px',
                                      'fontSize': '20px',
                                      'padding-left': '100px',
                                      'display': 'inline-block'})
                ]), width=6),

                # # Histogramme quantitatif -- satisfaction
                dbc.Col(html.Div([
                    dcc.Graph(id='scatter_Sat', figure=fig_scatter_sat),
                    html.P([html.Label("Choose a feature"),
                            dcc.Dropdown(id='opt2', options=opt2,
                                         value='Cleanliness')
                            ], style={'width': '400px',
                                      'fontSize': '20px',
                                      'padding-left': '100px',
                                      'display': 'inline-block'})
                ]), width=6),

                # ###FIN ROW ###
            ]),
            
            # FIN TOUTES LES DIV
            html.Div(id='intermediate-value', style={'display': 'none'})
            #######
        ]),


        # #######################################################################
        # #############################     TAB 2     ###########################
        # ######################################################################


        dcc.Tab(label='Seat', id='tab2', children=[
                html.Div([
                    html.Br(),
                    dbc.Row([
                            # -------DROPDOWNS + DATE PICKER ---------
                            # gerer fonction du boutton voir components dash (tuto)
                            dbc.Col(html.Div([html.Label('Filters'),
                              html.Button('Refresh Filters',
                                          id='reset_button_t2')]),
                                    width=1),
                            dbc.Col(html.Div([html.Label('Airline'),
                                              dcc.Dropdown(id='comp_filt_t2',
                                    options=opt_comp,
                                    multi=False
                                    )]), width=2),
                            dbc.Col(html.Div([html.Label('Manufacturer'),
                                              dcc.Dropdown(id='manu_filt_t2',
                                    options=opt_manu,
                                    multi=False
                                    )]), width=2),
                            dbc.Col(html.Div([html.Label('Aircraft Type'),
                                              dcc.Dropdown(id='type_filt_t2',
                                    options=opt_type,
                                    multi=False
                                    )]), width=2)
                                            ]),

                    dbc.Row([
                        # ################# PIE CHART -- TYPE OF SEAT ###
                        dbc.Col(html.Div([
                            dcc.Graph(id='graph_type_s',
                                      figure=fig_type_s),
                        ]), width=6),

                        # ################# BOX PLOT -- note selon la position
                        dbc.Col(html.Div([
                            dcc.Graph(id='graph_note_box',
                                      figure=fig_note_box),
                        ]), width=6),
                    ])

                ]),
                html.Div(id='intermediate-value2', style={'display': 'none'})
                ]),


        # ####################################################################
        # #############################     TAB 3     ########################
        # ####################################################################


        dcc.Tab(label='Flight Caracteristics', id='tab3', children=[html.Div([
            html.Br(),
            dbc.Row(
                [
                    # -------DROPDOWNS + DATE PICKER ---------
                    dbc.Col(html.Div([html.Label('Filters'),
                              html.Button('Refresh Filters',
                                          id='reset_button_t3')]),
                                    width=1),
                            dbc.Col(html.Div([html.Label('Airline'),
                                              dcc.Dropdown(id='comp_filt_t3',
                                    options=opt_comp,
                                    multi=False
                                    )]), width=2),
                            dbc.Col(html.Div([html.Label('Manufacturer'),
                                              dcc.Dropdown(id='manu_filt_t3',
                                    options=opt_manu,
                                    multi=False
                                    )]), width=2),
                            dbc.Col(html.Div([html.Label('Aircraft Type'),
                                              dcc.Dropdown(id='type_filt_t3',
                                    options=opt_type,
                                    multi=False
                                    )]), width=2)
                                            ]),
            dbc.Row([
                # ################# BoxPlot -- note selon category/class
                dbc.Col(html.Div([
                    dcc.Graph(id='graph_note_class',
                              figure=fig_note_class),
                ]), width=6),
                # #################  seat_comfort/ seat_category
                dbc.Col(html.Div([
                    dcc.Graph(id='scatter_comfort_class',
                              figure=fig_scatter_comfort_class),
                ]), width=6),


            ]),
            dbc.Row([
                # ################# empile -- type_of_traveller X recommended
                dbc.Col(html.Div([
                    dcc.Graph(id='plot_type_reco',
                              figure=fig_type_reco),

                ]), width=6),

            ]),


        ]),
        html.Div(id='intermediate-value3', style={'display': 'none'})
        ]),


        # ######################################################################
        # #############################     TAB 4     #########################
        # ######################################################################

        dcc.Tab(label='Aircraft Plans', id='tab4', children=[html.Div([
            html.Br(),
            dbc.Row([
                   # Dropdowns
                dbc.Col(html.Div([html.Label('Aircraft'),
                          dcc.Dropdown(
                            options=list_option_aircraft,
                            multi=False,
                            id='dd_aircraft',
                            value=list_aircraft_clean[0]
                            )]), style={"maxWidth": "500px"}),
                dbc.Col(html.Div([html.Label('Seat'),
                          dcc.Dropdown(
                            multi=False,
                            id='dd_seat'
                            )]), style={"maxWidth": "500px"})]),
            dbc.Row([
                # Image plane
                dbc.Col([html.Img(id='img_plane', useMap="#siege", style={"margin-top": "50px"}, src='data:image/png;base64,{}'.format(encoded_image.decode())),
                     html.MapEl(children=initialize_tag(), id='mapelement', name="siege")]),
                dbc.Col([html.Div([dcc.Graph(id='scatter_seat',style={
                        "width": "400px", "height": "1000px"}, figure=fig_scatter)])])
            ])
    ], style={"text-align": "center"})
        ]),


        # #######################################################################
        # #############################     TAB 5     #########################
        # ######################################################################

        dcc.Tab(label='Comments', id='tab5', children=[
                    html.Br(),
                    dbc.Col(html.Div([html.Label('Label'),
                                      dcc.Dropdown(id='lab_filt_t5',
                                               options=[
                                                   {'label': 'Atmosphere',
                                                    'value': 'ATMOSPHERE'},
                                                   {'label': 'Baggage',
                                                    'value': 'BAGGAGE'},
                                                   {'label': 'Cabin_Crew',
                                                    'value': 'CABIN_CREW'},
                                                   {'label': 'Comfort',
                                                    'value': 'COMFORT'},
                                                   {'label': 'Empty',
                                                    'value': 'EMPTY'},
                                                   {'label': 'Food',
                                                    'value': 'FOOD'},
                                                   {'label': 'Not_Flight',
                                                    'value': 'NOT_FLIGHT'},
                                                   {'label': 'Price',
                                                    'value': 'PRICE'},
                                                   {'label': 'Punctuality',
                                                    'value': 'PUNCTUALITY'},
                                               ],
                                               multi=False,
                                               value='BAGGAGE'
                                               )]), width=2),
                    dbc.Col([html.Img(id='word_cloud', style={"margin-top":"50px"}, src='data:image/png;base64,{}'.format(encoded_image.decode()))]),
                ])

    ]),
])

# DEBUT DES CALLBACK

    
####################################
# TAB 1    
####################################    
  
    
@app.callback(
    Output('nb_passengers', 'children'),
    [Input('intermediate-value', 'children')])
def update_kpi(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    nb_passengers = len(nouv_data.index)
    return nb_passengers    
    

@app.callback(
    Output('plot', 'figure'),
    [Input('opt', 'value'),
     Input('intermediate-value', 'children')])
    
def update_graph_3(input1,jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    resultDF = pd.read_json(datasets['defaultDF'], orient='split')
    resultDF = resultDF.dropna(axis=0, subset=[input1])
    trace_3 = go.Bar(x=list(Counter(resultDF[input1]).keys()),
                     y=list(Counter(resultDF[input1]).values()),
                     name=input1)
    layout_nb_vol = go.Layout(title='Number of flight')
    fig_nb_vol = go.Figure(data=[trace_3], layout=layout_nb_vol)
    return fig_nb_vol


@app.callback(
    Output('graph_type_f', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph_2(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    nouv_data = nouv_data.dropna(axis=0, subset=['Flight_Type'])
    trace_3 = go.Pie(go.Pie(labels=nouv_data['Flight_Type'].unique(),
                        values=nouv_data['Flight_Type'].value_counts(),
                        name='Proportion Flight Type'))
    layout_type_f = go.Layout(title='Flight Type Proportion')
    fig_type_f = go.Figure(data=[trace_3], layout=layout_type_f)
    
    return fig_type_f


@app.callback(
    Output('graph_type_la', 'figure'),
    [Input('intermediate-value', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    data_la = pd.read_json(datasets['defaultDF'], orient='split')
    data_la = data_la.dropna(axis=0, subset=['Overall_Customer_Rating'])
    trace_satisfaction = go.Pie(go.Pie(labels=data_la['Overall_Customer_Rating'].unique(),
                            values=data_la['Overall_Customer_Rating'].value_counts()),
                     name='Proportion General Satisfaction')
    layout_type_la = go.Layout(title='Proportion General Satisfaction')
    fig_type_la = go.Figure(data=[trace_satisfaction], layout=layout_type_la)
    
    return fig_type_la


@app.callback(
    dash.dependencies.Output('bar_sat', 'figure'),
    [Input('opt_bar_sat', 'value'),
     Input('intermediate-value', 'children')])
    
def update_graph_5(input1,jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    datasets = json.loads(jsonified_cleaned_data)
    resultDF = pd.read_json(datasets['defaultDF'], orient='split')
    resultDF = resultDF.dropna(axis=0, subset=[input1])
    fig_empile_sat = go.Figure()
    fig_empile_sat.add_trace(go.Bar(name='unsatisfied',
                                    x=resultDF[input1].unique(),
                                    y=resultDF[input1][resultDF['Overall_Customer_Rating'] <= 3].value_counts()))
    fig_empile_sat.add_trace(go.Bar(name='satisfied',
                                    x=resultDF[input1].unique(),
                                    y=(resultDF[input1][resultDF['Overall_Customer_Rating'].between(3.1,7)].value_counts())))
    fig_empile_sat.add_trace(go.Bar(name='very satisfied',
                                    x=resultDF[input1].unique(),
                                    y=(resultDF[input1][resultDF['Overall_Customer_Rating'] > 7].value_counts())))
                                       
    fig_empile_sat.update_layout(barmode='relative',
                                 title_text='Customers Rating by '
                                 + input1)

    return fig_empile_sat


@app.callback(
    dash.dependencies.Output('scatter_Sat', 'figure'),
    [Input('opt2', 'value'),
     Input('intermediate-value', 'children')])
def update_graph_6(input1,jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    nouv_data = defaultDF.dropna(axis=0, subset=['Overall_Customer_Rating'])
    nouv_data = defaultDF.dropna(axis=0, subset=[input1])
    zzz = nouv_data[['Overall_Customer_Rating', input1]]
    x = []
    y = []
    size = []
    for i in range(0,11):
        for j in range(0,6):
            x.append(i)
            y.append(j)
            new_zzz = zzz[zzz['Overall_Customer_Rating'] == i]
            new_zzz = new_zzz[new_zzz[input1] == j]
            size.append(len(new_zzz.index)/10)
    trace_1 = go.Scatter(x=x,
                         y=y,
                         name=input1,
                         mode='markers',
                         marker=dict(size=size))
    layout_scatter_sat = go.Layout(title='Global Satisfaction')
    fig_scatter_sat = go.Figure(data=[trace_1], layout=layout_scatter_sat)
    return fig_scatter_sat


####################################
# TAB 2    
####################################

# Type Seat Proportion
@app.callback(
    Output('graph_type_s', 'figure'),
    [Input('intermediate-value2', 'children')])
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    nouv_data = nouv_data.dropna(axis=0, subset=['Seat_Type'])
    trace_seat_type = go.Pie(go.Pie(labels=nouv_data['Seat_Type'].unique(),
                        values=nouv_data['Seat_Type'].value_counts(),
                        name='Proportion Seat Type'))
    layout_type_st = go.Layout(title='Type Seat Proportion')
    fig_type_s = go.Figure(data=[trace_seat_type], layout=layout_type_st)
    
    return fig_type_s

# Box Type Seat and Notes
@app.callback(
    Output('graph_note_box', 'figure'),
    [Input('intermediate-value2', 'children')])
def update_graph_3(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    fig_note_box = go.Figure()
    fig_note_box.add_trace(go.Box(name='standard',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'standard']))
    fig_note_box.add_trace(go.Box(name='recliner',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'recliner']))
    fig_note_box.add_trace(go.Box(name='flat_bed',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'flat_bed']))
    fig_note_box.add_trace(go.Box(name='angle_flat',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'angle_flat']))
    fig_note_box.add_trace(go.Box(name='open_suite',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'open_suite']))
    fig_note_box.add_trace(go.Box(name='closed_suite',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Seat_Type'] == 'closed_suite']))
    
    fig_note_box.update_layout(title='Notes Dispersion by Seat Type')
    
    return fig_note_box


####################################
# TAB 3
####################################

# Box Class and Notes
@app.callback(
    Output('graph_note_class', 'figure'),
    [Input('intermediate-value3', 'children')])
def update_graph_4(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    fig_note_class = go.Figure()
    fig_note_class.add_trace(go.Box(name='economy',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Category'] == 'economy']))
    fig_note_class.add_trace(go.Box(name='business',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Category'] == 'business']))
    fig_note_class.add_trace(go.Box(name='first',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Category'] == 'first']))
    fig_note_class.add_trace(go.Box(name='premium',
                              y=nouv_data['Overall_Customer_Rating'][nouv_data['Category'] == 'premium']))
    
    fig_note_class.update_layout(title='Global Notes by Class')
    
    return fig_note_class


# Scatter Comfort and Class
@app.callback(
    Output('scatter_comfort_class', 'figure'),
    [Input('intermediate-value3', 'children')])
def update_graph_5(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    nouv_data = defaultDF.dropna(axis=0, subset=['Category'])
    nouv_data = defaultDF.dropna(axis=0, subset=['Seat_Comfort'])
    zzz = nouv_data[['Category', 'Seat_Comfort']]
    x = ['economy','business','first','premium']
    y = []
    size = []
    for i in range(0,len(x)):
        for j in range(0,6):
            x.append(x[i])
            y.append(j)
            new_zzz = zzz[zzz['Category'] == x[i]]
            new_zzz = new_zzz[new_zzz['Seat_Comfort'] == j]
            size.append(len(new_zzz.index)/40)
    trace_comfort_class = go.Scatter(x=x,
                                     y=y,
                                     name='Category',
                                     mode='markers',
                                     marker=dict(size=size))
    layout_scatter_comfort_class = go.Layout(title='Seat Comfort and Class')
    fig_scatter_comfort_class = go.Figure(
        data=[trace_comfort_class], layout=layout_scatter_comfort_class)
    
    return fig_scatter_comfort_class


# Type of Traveller and Recommended
@app.callback(
    Output('plot_type_reco', 'figure'),
    [Input('intermediate-value3', 'children')])
def update_graph_6(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    nouv_data = pd.read_json(datasets['defaultDF'], orient='split')
    fig_type_reco = go.Figure()
    fig_type_reco.add_trace(go.Bar(name='yes',
                                        x=nouv_data['Type_of_Traveller'].unique(),
                                        y=nouv_data['Type_of_Traveller'][nouv_data['Recommended'] == 'yes'].value_counts()))
    fig_type_reco.add_trace(go.Bar(name='no',
                                        x=nouv_data['Type_of_Traveller'].unique(),
                                        y=nouv_data['Type_of_Traveller'][nouv_data['Recommended'] == 'no'].value_counts()))
    fig_type_reco.update_layout(barmode='relative',
                                title_text='Type of Traveller and Recommended Fly')
    
    return fig_type_reco


####################################
# TAB 4
####################################
    

@app.callback(
    [dash.dependencies.Output('dd_seat', 'options'),
     dash.dependencies.Output('dd_seat', 'value')],
    [dash.dependencies.Input('dd_aircraft', 'value')])
def update_list_seat(value):
    aircraft = list_aircraft[list_aircraft_clean.index(value)]
    seats = fa.find_seats(data, aircraft)
    list_seat = [{'label':seat, 'value':seat} for seat in seats]
    return list_seat, list_seat[0]['value']

@app.callback(
    dash.dependencies.Output('img_plane', 'src'),
    [dash.dependencies.Input('dd_aircraft', 'value')])
def update_image(value):
    aircraft_image = path_data + list_aircraft[list_aircraft_clean.index(value)]
    encoded_image = base64.b64encode(open(aircraft_image, 'rb').read())
    source = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return source

@app.callback(
    dash.dependencies.Output('mapelement', 'children'),
    [dash.dependencies.Input('dd_aircraft', 'value')])
def update_area_seat(value):
    list_tag = []
    all_coord_seat = fa.find_coordinates(data, list_aircraft[list_aircraft_clean.index(value)])
    index_id = 0
    for coord in all_coord_seat.keys():
        coord_all = str(all_coord_seat[coord])[1:-1]
        list_tag.append(html.Area(shape="rect", title="Seat N°"+str(index_id), coords=coord_all, id=str(index_id)))
        index_id += 1    
    return list_tag

@app.callback(
    dash.dependencies.Output('scatter_seat', 'figure'),
    [dash.dependencies.Input('dd_aircraft', 'value'),
     dash.dependencies.Input('dd_seat', 'value')])
def update_fig_seat(input_aircraft, input_seat):
    aircraft_image = list_aircraft[list_aircraft_clean.index(input_aircraft)]
    dict_element = fa.find_elements(data, aircraft_image, input_seat)
    list_el = []
    list_x = []
    list_y = []
    list_d = []

    for el in dict_element.keys():
        for coord_dist in dict_element[el]:
            list_el.append(el)
            list_x.append(coord_dist[0][0])
            list_y.append(coord_dist[0][1])
            list_d.append(coord_dist[1]/15)
            
    list_col = []
    for el in range(len(list_el)):
        if list_el[el] == "bar": list_col.append("red")
        elif list_el[el] == "toilettes": list_col.append("blue")
        elif list_el[el] == "sortie_gauche": list_col.append("yellow")
        elif list_el[el] == "sortie_droit": list_col.append("yellow")
        
    max_y = np.max(list_y)+100 if len(list_y)>0 else 0
        
    scatter_seat = go.Scatter(
        x=list_x,
        y=list_y,
        mode='markers',
        marker=dict(size=list_d, color=list_col)
        )
    layout_seat = go.Layout(title="Distance between the seat and the elements")
    fig_seat = go.Figure(data=[scatter_seat], layout=layout_seat)
    fig_seat.update_xaxes(showticklabels=False)
    fig_seat.update_yaxes(showticklabels=False, range=[max_y, 0])
    return fig_seat

# ################################################
# ####### Refresh filters ###################


@app.callback(
    dash.dependencies.Output('comp_filt', 'value'),
    [dash.dependencies.Input('reset_button', 'n_clicks')])
def on_click1(n_clicks):
    if (n_clicks):
        return None


@app.callback(
    dash.dependencies.Output('manu_filt', 'value'),
    [dash.dependencies.Input('reset_button', 'n_clicks')])
def on_click2(n_clicks):
    if (n_clicks):
        return None


@app.callback(
    dash.dependencies.Output('type_filt', 'value'),
    [dash.dependencies.Input('reset_button', 'n_clicks')])
def on_click3(n_clicks):
    if (n_clicks):
        return None


# RESET BUTTON TAB 3


@app.callback(
    dash.dependencies.Output('comp_filt_t3', 'value'),
    [dash.dependencies.Input('reset_button_t3', 'n_clicks')])
def on_click1_t3(n_clicks):
    if (n_clicks):
        return None


@app.callback(
    dash.dependencies.Output('manu_filt_t3', 'value'),
    [dash.dependencies.Input('reset_button_t3', 'n_clicks')])
def on_click2_t3(n_clicks):
    if (n_clicks):
        return None


@app.callback(
    dash.dependencies.Output('type_filt_t3', 'value'),
    [dash.dependencies.Input('reset_button_t3', 'n_clicks')])
def on_click4_t3(n_clicks):
    if (n_clicks):
        return None
    
    
    
###############################################################
    #TEST SHARED DATA
###############################################################

@app.callback(
    Output('intermediate-value', 'children'),
              [dash.dependencies.Input('comp_filt', 'value'),
               dash.dependencies.Input('manu_filt', 'value'),
               dash.dependencies.Input('type_filt', 'value')])

def clean_data(in_comp_1, in_manu_1, in_type_1):
    os.chdir("C:\\Oracle\\instantclient_19_5")
    ORACLE_CONNECT = "rll2373a/Alice1234@(DESCRIPTION=(SOURCE_ROUTE=OFF)(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=telline.univ-tlse3.fr)(PORT=1521)))(CONNECT_DATA=(SID=etupre)))"
    mydb = cx_Oracle.connect(ORACLE_CONNECT)
    mycursor = mydb.cursor()
###REQUETE TABLE PAR DEFAULT###

    if in_comp_1==None and in_manu_1==None and in_type_1==None:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
    else:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
        data_filters=(in_comp_1, in_manu_1, in_type_1)
        
        for list2 in range(len(data_filters)):
            if not data_filters[list2] is None:
                for x in data_filters[list2]:
                    if list2==0:
                        req_fin = req_fin + " AND S.airline_name='"+x+"'"
                    if list2==1:
                        req_fin = req_fin + " AND S.manufacturer_name='"+x+"'"
                    if list2==2:
                        req_fin = req_fin + " AND S.aircraft_type='"+x+"'"
    mycursor.execute(req_fin)

    myresult = mycursor.fetchall()
    myresult
    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    defaultDF=pd.DataFrame(myresult, columns=['Airline', 'Manufacturer', 'Aircraft', 'Category',
                                    'Flight_Type','Seat_Type', 'Power_Available',
                                    'Seat_Position',
                                    'Overall_Customer_Rating','Cleanliness', 'Catering',
                                    'Inflight_Entertainment', 'Cabin_Staff_Service',
                                    'Seat_Comfort', 'Origin', 'Date',
                                    'Type_of_Traveller', 'Recommended'])

    datasets = {
         'defaultDF': defaultDF.to_json(orient='split', date_format='iso'),
     }

    return json.dumps(datasets)

@app.callback(
    Output('intermediate-value2', 'children'),
              [dash.dependencies.Input('comp_filt_t2', 'value'),
               dash.dependencies.Input('manu_filt_t2', 'value'),
               dash.dependencies.Input('type_filt_t2', 'value')])

def clean_data(in_comp_2, in_manu_2, in_type_2):
    os.chdir("C:\\Oracle\\instantclient_19_5")
    ORACLE_CONNECT = "rll2373a/Alice1234@(DESCRIPTION=(SOURCE_ROUTE=OFF)(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=telline.univ-tlse3.fr)(PORT=1521)))(CONNECT_DATA=(SID=etupre)))"
    mydb = cx_Oracle.connect(ORACLE_CONNECT)
    mycursor = mydb.cursor()
###REQUETE TABLE PAR DEFAULT###

    if in_comp_2==None and in_manu_2==None and in_type_2==None:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
    else:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
        data_filters=(in_comp_2, in_manu_2, in_type_2)
        
        for list2 in range(len(data_filters)):
            if not data_filters[list2] is None:
                for x in data_filters[list2]:
                    if list2==0:
                        req_fin = req_fin + " AND S.airline_name='"+x+"'"
                    if list2==1:
                        req_fin = req_fin + " AND S.manufacturer_name='"+x+"'"
                    if list2==2:
                        req_fin = req_fin + " AND S.aircraft_type='"+x+"'"
    mycursor.execute(req_fin)

    myresult = mycursor.fetchall()
    myresult
    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    defaultDF=pd.DataFrame(myresult, columns=['Airline', 'Manufacturer', 'Aircraft', 'Category',
                                    'Flight_Type','Seat_Type', 'Power_Available',
                                    'Seat_Position',
                                    'Overall_Customer_Rating','Cleanliness', 'Catering',
                                    'Inflight_Entertainment', 'Cabin_Staff_Service',
                                    'Seat_Comfort', 'Origin', 'Date',
                                    'Type_of_Traveller', 'Recommended'])

    datasets = {
         'defaultDF': defaultDF.to_json(orient='split', date_format='iso'),
     }

    return json.dumps(datasets)


@app.callback(
    Output('intermediate-value3', 'children'),
              [dash.dependencies.Input('comp_filt_t3', 'value'),
               dash.dependencies.Input('manu_filt_t3', 'value'),
               dash.dependencies.Input('type_filt_t3', 'value')])

def clean_data(in_comp_3, in_manu_3, in_type_3):
    os.chdir("C:\\Oracle\\instantclient_19_5")
    ORACLE_CONNECT = "rll2373a/Alice1234@(DESCRIPTION=(SOURCE_ROUTE=OFF)(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=telline.univ-tlse3.fr)(PORT=1521)))(CONNECT_DATA=(SID=etupre)))"
    mydb = cx_Oracle.connect(ORACLE_CONNECT)
    mycursor = mydb.cursor()
###REQUETE TABLE PAR DEFAULT###

    if in_comp_3==None and in_manu_3==None and in_type_3==None:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
    else:
        req_fin='''Select S.airline_name , S.manufacturer_name , 
                 S.aircraft_type, S.CATEGORY, S.flight_type , S.seat_type , 
                S.power_available , S.seat_position, N.overall_customer_rating, 
                N.cleanliness ,N.catering ,N.inflight_entertainment, 
                N.cabin_staff_service, N.seat_comfort, R.origine ,N.date_flown,
                P.type_of_traveller, N.recommended
                FROM  ROUTE R, NOTES N, SEAT S ,DATES D, PASSENGER P
                WHERE N.id_seat = S.id_seat AND 
                N.id_route = R.id_route AND N.date_flown = D.id_date
                AND P.id_passenger = N.id_passenger'''
        data_filters=(in_comp_3, in_manu_3, in_type_3)
        
        for list2 in range(len(data_filters)):
            if not data_filters[list2] is None:
                for x in data_filters[list2]:
                    if list2==0:
                        req_fin = req_fin + " AND S.airline_name='"+x+"'"
                    if list2==1:
                        req_fin = req_fin + " AND S.manufacturer_name='"+x+"'"
                    if list2==2:
                        req_fin = req_fin + " AND S.aircraft_type='"+x+"'"
    mycursor.execute(req_fin)

    myresult = mycursor.fetchall()
    myresult
    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    defaultDF=pd.DataFrame(myresult, columns=['Airline', 'Manufacturer', 'Aircraft', 'Category',
                                    'Flight_Type','Seat_Type', 'Power_Available',
                                    'Seat_Position',
                                    'Overall_Customer_Rating','Cleanliness', 'Catering',
                                    'Inflight_Entertainment', 'Cabin_Staff_Service',
                                    'Seat_Comfort', 'Origin', 'Date',
                                    'Type_of_Traveller', 'Recommended'])

    datasets = {
         'defaultDF': defaultDF.to_json(orient='split', date_format='iso'),
     }

    return json.dumps(datasets)



##############################
# TAB 5
##############################
@app.callback(
    dash.dependencies.Output('word_cloud', 'src'),
    [Input('lab_filt_t5', 'value')])
#     dash.dependencies.Input('date-picker-range', 'start_date'),
#     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_tab5(input1):
    mycursor = mydb.cursor()
    frequencies = {}
    for row in mycursor.execute('''SELECT W.word, AVG(A.tfidf)
                                FROM WORD W, APPEAR A
                                WHERE A.id_word = W.id_word
                                AND W.id_word IN(
                                    SELECT A1.id_word
                                    FROM APPEAR A1
                                    WHERE A1.id_doc IN (
                                        SELECT D2.id_doc
                                        FROM DOCUMENT D2
                                        WHERE '''+input1+''' != 0))
                                GROUP BY w.word
                                ORDER BY AVG(A.tfidf)
                                FETCH FIRST 20 ROWS ONLY'''):
        frequencies[str(row[0])] = round(row[1],2)
    if len(frequencies) != 0:
        word_cloud = WordCloud(width = 400, height = 400, background_color='white', stopwords=STOPWORDS).generate_from_frequencies(frequencies)
        word_cloud.to_file("resultat.png")
        image = "resultat.png"
        encoded_image = base64.b64encode(open(image, 'rb').read())
        source = 'data:image/png;base64,{}'.format(encoded_image.decode())
        return source
    else:
        frequencies['No data found'] = 5
        word_cloud = WordCloud(width = 400, height = 400, background_color='white', stopwords=STOPWORDS).generate_from_frequencies(frequencies)
        word_cloud.to_file("resultat.png")
        image = "resultat.png"
        encoded_image = base64.b64encode(open(image, 'rb').read())
        source = 'data:image/png;base64,{}'.format(encoded_image.decode())
        return source
    


if __name__ == '__main__':
    app.run_server(debug=True)
    app.config['suppress_callback_exceptions'] = True
