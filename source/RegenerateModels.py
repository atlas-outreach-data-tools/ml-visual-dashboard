# general imports
import random
import numpy as np
import pandas as pd

# ML inventory
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV

seed = 84

def balanced_count_split(df, random_seed, fr=0.7):
    df_train = pd.DataFrame(columns=df.keys())  # frame the training subset
    events = df['Event'].unique()               # list all events
    train_DM = df[df['Event']=='DM_300'].sample(frac=fr, random_state=random_seed)  # training part of DM subset
    train_DM_size = len(train_DM)  # size of training DM subset
    full_DM_size = len(df[df['Event']=='DM_300'])  # full size of training DM subset
    full_size = len(df)
    full_BKG_size = full_size - full_DM_size
    k=1
    for event in events:
        if event!=events[-1]:
            df_event = df[df['Event']==event]            # form the current Event subset

            full_Event_size = len(df[df['Event']==event])
            R = full_Event_size/full_BKG_size
            N = train_DM_size*R*4*k

            train_part = df_event.sample(n=int(N), random_state=random_seed)  # take a random sample
            df_train = pd.concat([df_train,train_part])   # append the training subset
    df_train = pd.concat([df_train,train_DM])

    # now split the rest of data into testing and background (with no DM) subsets
    df_rest = df.drop(df_train.index)              # rest = dataset - training subset
    df_test = pd.DataFrame(columns=df.keys())      # frame the 'testing' subset
    test_DM = df_rest[df_rest['Event']=='DM_300']  # extract all DM data to include in the testing subset
    test_DM_size = full_DM_size-train_DM_size
    for event in events:
        if event!=events[-1]:
            df_event = df_rest[df_rest['Event']==event]    # form the current Event subset
            full_Event_size = len(df[df['Event']==event])
            N = full_Event_size*(1-fr)
            test_part = df_event.sample(n=int(N), random_state=random_seed)  # take random sample
            df_test = pd.concat([df_test,test_part])      # append the background subset
    df_test = pd.concat([df_test,test_DM])

    return df_train, df_test

def shortlist(df_test, x_scaled, random_seed, N=3):
    df_shortlist = pd.DataFrame(columns=df_test.keys())  # frame the subset
    events = df_test['Event'].unique()                   # list all events
    for event in events:
        df_event = df_test[df_test['Event']==event]       # extract the current class data
        short_part = df_event.sample(n=N, random_state=random_seed)  # take a random sample of N size
        df_shortlist = pd.concat([df_shortlist,short_part])   # append the training subset

    df_shortlist_scaled = pd.DataFrame(x_scaled, index=df_test.index)
    df_shortlist_scaled = df_shortlist_scaled.loc[df_shortlist.index]

    return df_shortlist, df_shortlist_scaled

def Run():
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
        del df

    # #save focus data for further easy access
    df_2022.to_csv('build/df_2022.csv', index=False)
    # define features
    Feats = df_2022.drop(columns=['Event','totalWeight']).columns

    # drop N_bjets
    df_app = df_2022.drop('N_bjets', axis=1)
    # cut by ETmiss
    df_app = df_app[df_app['ETmiss']>90.24]

    # split into train and test sets
    df_train, df_test = balanced_count_split(df_app, random_seed=seed)

    # split the train/test datasets into the feature, labels and weights subsets
    X_train = df_train.drop(['Event','totalWeight'], axis=1).values
    W_train = df_train['totalWeight'].values.astype('float64')
    Y_train = df_train['Event'].values
    Y_train = np.array([1 if e=='DM_300' else 0 for e in Y_train])  # binarise classes (1-Signal, 0-Background)

    X_test = df_test.drop(['Event','totalWeight'], axis=1).values
    W_test = df_test['totalWeight'].values.astype('float64')
    Y_test = df_test['Event'].values
    Y_test = np.array([1 if e=='DM_300' else 0 for e in Y_test])  # binarise classes (1-Signal, 0-Background)

    # Initialise the Scaler
    scaler = StandardScaler()

    # Scale the sets
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # extract test set ids
    test_ids = df_test.reset_index()
    test_ids = test_ids['index']

    ### only for App purposes  ##
    # reduce size
    df_test00 = df_test.astype({'totalWeight':'float16'})
    df_test00 = df_test00.round({'lead_lep_pt': 1, 'sublead_lep_pt': 1, 'mll': 1, 'ETmiss': 1,'dRll': 2, 'dphi_pTll_ETmiss': 3,'fractional_pT_difference': 3, 'ETmiss_over_HT': 3,})
    # save Test data for visualising in Scatter plot in WebApp
<<<<<<< Updated upstream
    df_test00.to_csv('share/df_test.csv', index=True, index_label='index')
=======
    df_test00.to_csv('build/df_test.csv', index=True, index_label='index')
>>>>>>> Stashed changes

    # form a shortlist df from the testing data to use with MLP visualisation
    # split into train and test sets
    df_shortlist, df_shortlist_scaled = shortlist(df_test, X_test_scaled, random_seed=0)

    # save Shortlist and Scaled Shortlist for App access
<<<<<<< Updated upstream
    df_shortlist.to_csv('share/df_shortlist.csv', index=True, index_label='index')
    df_shortlist_scaled.to_csv('share/df_shortlist_scaled.csv', index=True, index_label='index')
=======
    df_shortlist.to_csv('build/df_shortlist.csv', index=True, index_label='index')
    df_shortlist_scaled.to_csv('build/df_shortlist_scaled.csv', index=True, index_label='index')
>>>>>>> Stashed changes

    # create list of MLP designs (combinations of hidden layers) from (1,) to (10,10,10)
    Designs = []
    for a in range(2,11,2):
        Designs.append((a,))

    for a in range(2,11,2):
        for b in range(2,11,2):
            Designs.append((a,b))

    for a in range(2,11,2):
        for b in range(2,11,2):
            for c in range(2,11,2):
                Designs.append((a,b,c))

    Probs = pd.DataFrame(Y_test, columns=['Event'], index=test_ids)
    Probs['Weight'] = W_test
    df_metrics = pd.DataFrame(index=['Accuracy','Precision','Recall','f1-score','S'])

    # run  the loop to store results of different MLP configuratrions
    for design in Designs:
        MLP = MLPClassifier(hidden_layer_sizes = design,
                            random_state = seed,
                            shuffle=True,
                            max_iter = 1000,        # def=200
                            alpha=0.0001, #0.05,             # def=0.0001
                            activation='relu',  # def=’relu’
                            )
        MLP.fit(X_train_scaled, Y_train)
        sig_prob = MLP.predict_proba(X_test_scaled)[:, 1]
        pred = MLP.predict(X_test_scaled)

        Probs[str(design)]=sig_prob.round(2)

        tn, fp, fn, tp = confusion_matrix(Y_test, pred, sample_weight=W_test).ravel()
        S = tp/(fp**0.5)

        df_metrics[str(design)]=np.array([accuracy_score(Y_test, pred, sample_weight=W_test),
                                    precision_score(Y_test, pred, sample_weight=W_test),
                                    recall_score(Y_test, pred, sample_weight=W_test),
                                    f1_score(Y_test, pred, sample_weight=W_test),
                                    S/100
                                    ]).round(4)*100

    df_probs = Probs.astype({'Weight':'float16'})

    # # save from Jupyter
<<<<<<< Updated upstream
    df_probs.to_csv('share/df_probs_2022.csv', index=True, index_label='index')
    df_metrics.to_csv('share/df_metrics_2022.csv', index=True, index_label='index')
=======
    df_probs.to_csv('build/df_probs_2022.csv', index=True, index_label='index')
    df_metrics.to_csv('build/df_metrics_2022.csv', index=True, index_label='index')
>>>>>>> Stashed changes

if __name__ == "__main__":
    print("Regenerating files.")
    Run()
else:
    print("Imported tools to Regenerate data files.")
