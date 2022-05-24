import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.impute import SimpleImputer
import joblib
# import seaborn as sns
# import graphvizs
# from sklearn.tree.export import export_text
from sklearn import metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score

def train_models():
    df= pd.read_csv('data\carInsurance_train.csv')
    df = raw_data_preprocessing(df)
    x= df.drop(['CarInsurance','Id'],axis=1)
    y=df['CarInsurance']
    x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.3, random_state=2)
    dt= tree.DecisionTreeClassifier(criterion='entropy', max_depth=8,min_samples_split=5, random_state=20)
    dt.fit(x_train,y_train)
    joblib.dump(dt, 'decision_tree_model.joblib')
    return dt

def pre_carinsurance(df1):
    df2 = df1
    dt = joblib.load('decision_tree_model.joblib')
    df1 = raw_data_preprocessing(df1)
    df1 = df1.drop(['CarInsurance','Id'],axis=1)

    pre = dt.predict(df1)
    pre = pd.DataFrame(pre, columns=["CarInsurance"])
    df2 = df2.drop(["CarInsurance"], axis=1)
    results = pd.concat([df2, pre], axis=1)
    return results

def raw_data_preprocessing(df):
    df['Communication'] = df['Communication'].fillna('none')
    df['Outcome'] = df['Outcome'].fillna('NoPrev')

    df['Job'] = df['Job'].fillna('management')
    df['Education'] = df['Education'].fillna('secondary')

    df['CallStart'] = pd.to_datetime(df['CallStart'])
    df['CallEnd'] = pd.to_datetime(df['CallEnd'])
    df['CallTime'] = (df['CallEnd'] - df['CallStart']).dt.total_seconds()
    df.drop(["CallStart", "CallEnd"], axis=1, inplace=True)

    feature = ['Job', 'Marital', 'Education', 'LastContactMonth', 'Outcome', 'Communication']
    df_onehot = pd.get_dummies(df[feature])

    df.drop(['Job', 'Marital', 'Education', 'LastContactMonth', 'Outcome', 'Communication'], axis=1, inplace=True)
    df = pd.concat([df_onehot, df], axis=1)
    return df