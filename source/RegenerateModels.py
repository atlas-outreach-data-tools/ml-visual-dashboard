# general imports
import random
import numpy as np
import pandas as pd
import os.path

# ML inventory
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV, train_test_split

seed = 84

def get_data():

    if os.path.isfile("build/df_2022.csv"):
        df_2022 = pd.read_csv('build/df_2022.csv')
        return df_2022

    # make a list of all background processes
    processes = ['nonresll', 'Zjets', 'WZ', 'ZZ'] # for 2022 data

    # pick up respective DM data set (2022)
    DM = 'DM_300'
    df_2022 = pd.read_csv(f'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/csv/DM_ML_workbook/{DM}.csv')
    df_2022.insert(loc=0, column='Event', value=DM)

    # import all bacjground in a data set
    for process in processes:
        df = pd.read_csv(f'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/csv/DM_ML_workbook/{process}.csv')
        if process=='nonresll':
            name='Non-resonant_ll'
        elif process=='Zjets':
            name='Z+jets'
        else:
            name=process
        df.insert(loc=0, column='Event', value=name)
        df_2022 = pd.concat([df_2022,df], ignore_index=True)

    # drop N_bjets
    df_app = df_2022.drop('N_bjets', axis=1)
    # cut by ETmiss
    df_app = df_app[df_app['ETmiss']>90.24]

    # #save focus data for further easy access
    df_app.to_csv('build/df_2022.csv', index=False)
        

    return df_app

def balanced_count_split(df, random_seed, fr=0.7):
    
    df_train = df_test = pd.DataFrame(columns=df.keys())  # frame the training subset
    events = df['Event'].unique()               # list all events
    
    df_DM = df[df['Event']=='DM_300']
    df_bkg = df[df['Event']!='DM_300']

    train_DM, test_DM = train_test_split(df_DM, train_size=fr, random_state=random_seed)
    #Oversampling:
    R = len(df_DM)/len(df_bkg)
    train_bkg, test_bkg = train_test_split(df_bkg, train_size=4*fr*R, random_state=random_seed, stratify=df_bkg['Event'])

    df_train = pd.concat([train_bkg,train_DM])
    df_test = pd.concat([test_bkg,test_DM])

    return df_train, df_test

def InWeightOutSplit(df):

    # split the train/test datasets into the feature, labels and weights subsets and add indexing
    X_train = df.drop(['Event','totalWeight'], axis=1).values
    W_train = df['totalWeight'].values.astype('float64')
    Y_train = df['Event'].values
    Y_train = np.array([1 if e=='DM_300' else 0 for e in Y_train])  # binarise classes (1-Signal, 0-Background)

    return X_train, W_train, Y_train

def shortlist(df_test, random_seed, N=3):
    #df_shortlist = pd.DataFrame(columns=df_test.keys())  # frame the subset
    events = df_test['Event'].unique()                   # list all events
    tmp_shortlist = []
    for event in events:
        df_event = df_test[df_test['Event']==event]       # extract the current class data
        short_part = df_event.sample(n=N, random_state=random_seed)  # take a random sample of N size
        tmp_shortlist.append(short_part) 

    df_shortlist = pd.concat(tmp_shortlist)

    return df_shortlist


def save_app_test_data(df_test):

    ### only for App purposes  ##
    # reduce size
    df_test00 = df_test.astype({'totalWeight':'float16'})
    df_test00 = df_test00.round({'lead_lep_pt': 1, 'sublead_lep_pt': 1, 'mll': 1, 'ETmiss': 1,'dRll': 2, 'dphi_pTll_ETmiss': 3,'fractional_pT_difference': 3, 'ETmiss_over_HT': 3,})
    # save Test data for visualising in Scatter plot in WebApp
    df_test00.to_csv('build/scatter_data.csv', index=False)#, index_label='index')    


def GetMLPDesigns():
    Designs = []
    for a in range(2,11,1):
        Designs.append((a,))

    for a in range(2,11,1):
        for b in range(2,11,1):
            Designs.append((a,b))

    for a in range(2,11,1):
        for b in range(2,11,1):
            for c in range(2,11,1):
                Designs.append((a,b,c))

    return Designs


def TestMLPDesign(design, seed, X_train_scaled, W_train, Y_train, 
                            X_test_scaled, W_test, Y_test,
                            shortlist_scaled):

    df_metrics = pd.DataFrame(index=['Accuracy','Precision','Recall','f1-score','S'])
    df_pred = pd.DataFrame(columns=[str(design)])
    shortlist_pred = pd.DataFrame(columns=[str(design)])

    #Define model
    MLP = MLPClassifier(hidden_layer_sizes = design,
                        random_state = seed,
                        shuffle=True,
                        max_iter = 1000,        # def=200
                        alpha=0.0001, #0.05,             # def=0.0001
                        activation='relu',  # def=’relu’
                        )
    #Train model
    MLP.fit(X_train_scaled, Y_train) #, sample_weight=W_train)

    #Assess model
    sig_prob = MLP.predict_proba(X_test_scaled)[:, 1]
    pred = MLP.predict(X_test_scaled)
    tn, fp, fn, tp = confusion_matrix(Y_test, pred, sample_weight=W_test).ravel()
    S = tp/(fp**0.5)


    df_metrics[str(design)]=np.array([accuracy_score(Y_test, pred, sample_weight=W_test),
                                    precision_score(Y_test, pred, sample_weight=W_test),
                                    recall_score(Y_test, pred, sample_weight=W_test),
                                    f1_score(Y_test, pred, sample_weight=W_test),
                                    S/100
                                    ]).round(4)*100

    df_pred[str(design)] = sig_prob
    
    #handle the shortlist with careful matching event-by-event of properties
    tmp_shortlist = shortlist_scaled
    tmp_shortlist.columns = tmp_shortlist.columns.astype(str)
    tmp_shortlist = tmp_shortlist.drop(columns=["index"]).to_numpy()
    shortlist_pred[str(design)] = MLP.predict_proba(tmp_shortlist)[:, 1]
    #shortlist_pred["index"] = shortlist_scaled["index"]
    return df_pred, df_metrics, shortlist_pred


def Run():
    
    #Get data
    df_app = get_data()
 
    # split into train and test sets
    df_train, df_test = balanced_count_split(df_app, random_seed=seed)

    X_train, W_train, Y_train = InWeightOutSplit(df_train)
    X_test, W_test, Y_test = InWeightOutSplit(df_test)
    
    # Initialise the Scaler
    scaler = StandardScaler()
    # Scale the sets
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #Save useful data for app
    df_test = df_test.reset_index()
    X_test_scaled_tmp = pd.DataFrame(X_test_scaled).reset_index()
    save_app_test_data(df_test)

    # create list of MLP designs (combinations of hidden layers) from (1,) to (10,10,10)
    Designs = GetMLPDesigns()
    Result_probs = []
    Result_metrics = []
    Shortlist_probs = []


    #For memory-safe event-by-event information:
    joined = pd.merge(df_test, X_test_scaled_tmp, on="index")
    df_shortlist = shortlist(joined, random_seed=seed)
    shortlist_scaled = df_shortlist.drop(columns=["Event","totalWeight","sum_lep_charge","lead_lep_pt",
                                            "sublead_lep_pt","mll","ETmiss","dRll","dphi_pTll_ETmiss",
                                            "fractional_pT_difference","ETmiss_over_HT"])

    # run  the loop to store results of different MLP configuratrions
    for design in Designs:

        tmp_probs, tmp_metrics, shortlist_pred = TestMLPDesign(design, seed, X_train_scaled, W_train, Y_train, 
                                                        X_test_scaled, W_test, Y_test, shortlist_scaled)

        Result_probs.append(tmp_probs)
        Result_metrics.append(tmp_metrics)
        Shortlist_probs.append(shortlist_pred)

    df_probs = pd.concat(Result_probs, axis=1)#, join='inner')
    df_metrics = pd.concat(Result_metrics, axis=1)
    df_probs['Event'] = df_test['Event']
    df_probs['weight'] = W_test
    df_probs = df_probs.reset_index()
    df_probs.to_csv('build/scatter_probs.csv', index=False)#, index_label='index')
    df_metrics.to_csv('build/MLP_metrics.csv', index=True, index_label='index')

    df_probs_shortlist = pd.concat(Shortlist_probs, axis=1)
    df_probs_shortlist = df_probs_shortlist.set_index(df_shortlist.index)
    df_shortlist_tosave = pd.concat([df_shortlist, df_probs_shortlist], axis=1)
    print(df_shortlist, df_probs_shortlist)
    df_shortlist_tosave.to_csv('build/events_shortlist_MLP.csv', index=False)#, index_label='index')

if __name__ == "__main__":

    FilesExist = True	
    if not os.path.isdir("build"):
        idir.mkdir()

    for ifile in ["scatter_probs", "events_shortlist_MLP", "MLP_metrics", "scatter_data", "df_2022"]:
        FilesExist = os.path.isfile("build/"+ifile+".csv")
        if not FilesExist:
            print("Regenerating files.")
            Run()
            break

    print("HOT TO GO!")

else:
    print("Imported tools to Regenerate data files.")
