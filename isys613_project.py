###################
# THIS MODULE CONTAINS THE GENDER AND ETHNICITY FUNCTIONS TO BE
# USED IN ISYS613 COURSE PROJECTS
###################
import random 
import pandas as pd
import nltk; from nltk.corpus import names 
import os; import os.path

# Shut Tensoflow the hell up about debugging warnings
import tensorflow as tf; import logging
tf.get_logger().setLevel(logging.ERROR)

import ethnicolr as ec

gender_classifier = None

def gender_features_2(word):
    return {'two_last': word[-2:], 'two_first': word[:2]}

def _predict_gender_init():
    try:
        male_pth = os.path.abspath('male_nms.txt')
        female_pth = os.path.abspath('female_nms.txt')
    except OSError:
        male_pth = os.path.abspath('male.txt')
        female_pth = os.path.abspath('female.txt')

    labeled_names = ([(name.lower(), 'male') for name in names.words(male_pth)]+
                [(name.lower(), 'female') for name in names.words(female_pth)]) 

    random.shuffle(labeled_names) 

    # we use the feature extractor to process the names data. 
    train_set = [(gender_features_2(n), gender) for (n, gender)in labeled_names] 

    # The training set is used to train a new "naive Bayes" classifier. 
    return nltk.NaiveBayesClassifier.train(train_set) 

def predict_gender(df: pd.DataFrame, name_attr: str) -> pd.Series:

    global gender_classifier

    if( gender_classifier == None):
        gender_classifier = _predict_gender_init()

    def gen_fx(nm):
        return gender_classifier.classify(gender_features_2(nm.lower()))

    return df[name_attr].apply(gen_fx)

def predict_ethnicity_1(df: pd.DataFrame, name_attr: str) -> pd.DataFrame:
    df1 =  ec.pred_census_ln(df, name_attr, year=2010).iloc[:,-4:]
    df1.columns = ['asian', 'black', 'hispanic', 'white']
    df1.index = df.index
    df.drop(columns='race', inplace=True)
    return df1

def predict_ethnicity_2(df: pd.DataFrame, name_attr: str) -> pd.DataFrame:
    df1= ec.pred_fl_reg_ln(df, name_attr).iloc[:,-4:]
    df1.columns = ['asian', 'black', 'hispanic', 'white']
    df1.index = df.index
    df.drop(columns='race', inplace=True)
    return df1