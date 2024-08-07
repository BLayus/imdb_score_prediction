# -*- coding: utf-8 -*-
"""Modelo Final Regressão IMDB.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ld1Ovw2RPEXzktZlFfYO93QnUafKWPds

##Bibliotecas e Dataset
"""

!pip install --upgrade scikit-learn

! pip install scikit-optimize

# Import libraries
import pandas as pd
import numpy as np
import re
from datetime import datetime
import datetime as dt

# Data viz libraries
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px

# Satistical Libraries
from scipy import stats
import scipy.stats
from scipy.stats import chi2_contingency
from scipy.stats import norm

# Machine Learning Libraries
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler
from sklearn.preprocessing import FunctionTransformer

from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mean_absolute_percentage_error

from xgboost import XGBRegressor

from sklearn.inspection import permutation_importance

from skopt import BayesSearchCV

import warnings
warnings.filterwarnings("ignore")

# Import dataset from github

df = pd.read_csv('https://raw.githubusercontent.com/BLayus/imdb_score_prediction/main/dataset/Dataset_imdb.csv', index_col= 'Unnamed: 0', encoding= 'utf_8')

# Dataset sample

df.sample(5)

# Applying a plot style to the charts

#plt.style.use('seaborn-v0_8')

sns.set_style('darkgrid', {'grid.color': '.8',
                           'grid.linestyle': '-',
                           'text.color': '.2',
                           'xtick.color': 'dimgray',
                           'ytick.color': 'dimgray',
                           'axes.labelcolor': 'dimgray'})

# Defining a color pallete

colors = ['#4c94de', 'grey', 'cornflowerblue', 'silver', 'lightsteelblue', 'whitesmoke']
sns.set_palette(sns.color_palette(colors))

# Import scrapped data from scrapping notebook

from google.colab import drive
drive.mount('/content/drive')

df_scrapping= pd.read_csv('/content/drive/MyDrive/Data Science/Case Lighthouse Indicium/scrapping.csv')

# Merge scrapped data into df
# Use '.loc' to align data properly based on matching 'Series_Title' values

for index, row in df_scrapping.iterrows():
    df.loc[df['Series_Title'] == row['Series_Title'], 'Gross'] = row['Gross']

df.info()

# The 'Apollo 13' movie has no date, in official website, I found that release year was 1995
# Using Loc to find and replace the value

df.loc[df['Released_Year'] == 'PG', 'Released_Year'] = 1995

df_pred = pd.DataFrame({'Series_Title': ['The Shawshank Redemption'],
                    'Released_Year': ['1994'],
                    'Certificate': ['A'],
                    'Runtime': ['142 min'],
                    'Genre': ['Drama'],
                    'Overview': ['Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'],
                    'Meta_score': [80.0],
                    'Director': ['Frank Darabont'],
                    'Star1': ['Tim Robbins'],
                    'Star2': ['Morgan Freeman'],
                    'Star3': ['Bob Gunton'],
                    'Star4': ['William Sadler'],
                    'No_of_Votes': [2343110],
                    'Gross': ['28,341,469']}
                  )

"""##Pre Processing"""

# Convert Released_Year to datetime year only

def convert_datetime(df):
  df['Released_Year']= pd.to_datetime(df['Released_Year'], format= '%Y', errors= 'coerce').dt.year
  return df

# Converting strings in column "Runtime" to int 64 and removing substring 'min'

def convert_runtime(df):
  if df['Runtime'].dtype == 'object':
    df['Runtime']= df['Runtime'].str.extract('(\d+)', expand=False).astype('int64')
  return df

# Replace commas in Gross strings

def convert_gross(df):
  df['Gross'] = df['Gross'].astype(str)
  df['Gross']= df['Gross'].str.replace(r'[^\w\s]', '', regex= True)

  # Converting gross type to numerical and fill NaN

  df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce').fillna(0).astype('int64')
  return df

# Certificate column, imput missing with mode

def simple_imputer(df):
  imputer= SimpleImputer(missing_values= np.nan, strategy= 'most_frequent')
  data= df[['Certificate']]
  imputer= imputer.fit(data)
  df['Certificate']= imputer.transform(data).flatten()

  # Meta Score column, imput with median

  imputer= SimpleImputer(missing_values= np.nan, strategy= 'median')
  data= df[['Meta_score']]
  imputer= imputer.fit(data)
  df['Meta_score']= imputer.transform(data).flatten()
  return df

# Certificate grouping and converting to numerical info
# As this grouping has low cardinality, we can use One Hot Encoder

def certificate_groups(df):
  df['Certificate']= df['Certificate'].apply(lambda x: 'all_age_group' if x == ['U', 'G', 'Passed', 'Approved']
                                             else 'accompanied_age_group' if x == ['PG', 'TV-PG', 'U/A', 'GP']
                                             else '14_years_group' if x == ['PG-13', 'TV-14']
                                             else '16_years_group' if x == ['16', 'R']
                                             else 'adult_group')
  return df

# Convert column dtypes

def convert_dtypes(df):
  df['Released_Year'] = df['Released_Year'].astype(int)
  df['Gross'] = df['Gross'].astype(int)
  return df

# Drop Unnecessary columns

def drop_cols(df):
  drop_cols= ['Series_Title', 'Overview']
  df.drop(columns= drop_cols, inplace= True)
  return df

# Convert column dtypes

def convert_dtypes(df):
  df['Released_Year'] = df['Released_Year'].astype(int)
  df['Gross'] = df['Gross'].astype(int)
  return df

# Drop Unnecessary columns

def drop_cols(df):
  drop_cols= ['Series_Title', 'Overview']
  df.drop(columns= drop_cols, inplace= True)
  return df

# Create a function with with steps before encoding

def pre_encoder(df):
  convert_datetime(df)
  convert_runtime(df)
  convert_gross(df)
  simple_imputer(df)
  certificate_groups(df)
  drop_cols(df)
  convert_dtypes(df)

  return(df)

# Defining functions to evaluate results

# Define a function to plot distplot
def distplot(y_test, y_predict):
  plt.figure(figsize=(8, 6))
  ax = sns.distplot(y_test, hist=False, color='r', label='Valor Real')
  sns.distplot(y_predict, hist=False, ax=ax, color='b', label='Valor Previsão')
  plt.legend()
  plt.title('Distribuição dos Valores')
  plt.show()

  if isinstance(model, DecisionTreeRegressor):
    plt.figure(figsize=(25, 12))
    plot_tree(model, filled=True)
    plt.show()

# Create a function to plot residual chart
def residplot(y_test, y_predict):
  plt.figure(figsize=(8, 6))
  sns.residplot(x=y_test, y=y_predict, color='r')
  plt.title('Resíduos')
  plt.xlabel('Valor Real')
  plt.ylabel('Erro')
  plt.show()

# Define function to evaluate
def evaluate(y_test, y_predict, model):
  distplot(y_test, y_predict)
  residplot(y_test, y_predict)
  print('R2: ', r2_score(y_test, y_predict))
  print('MAE: ', mean_absolute_error(y_test, y_predict))
  print('MAPE: ', mean_absolute_percentage_error(y_test, y_predict))
  print('MSE: ', mean_squared_error(y_test, y_predict))
  print('RMSE: ', np.sqrt(mean_squared_error(y_test, y_predict)))


# Define a function to plot feature importances
def feature_importance (model):
  if hasattr(model, 'feature_importances_'):
    feat_imp = pd.Series(model.feature_importances_, index= x_train.columns).sort_values(ascending=False)

    top_feat = feat_imp[:6]
    all_feat = feat_imp[::]

    fig, axes = plt.subplots(1,2, figsize=(12,8))
    top_feat.plot(kind='bar', ax=axes[0])
    all_feat.plot(kind='bar', ax=axes[1])
    axes[0].set_title(f"{model} - Top 6 Most Important Features")
    axes[1].set_title(f"{model} - All Feature Importances")

  else:
    print(f"Feature importance is not available for {model.steps[-1][0]}")
  return print('')


# Define a function to store each model results
def append_results (model, y_test, y_predict):
  model_name.append(model.__class__.__name__)
  R2.append(round(r2_score(y_test, y_predict), 3))
  MAE.append(round(mean_absolute_error(y_test, y_predict), 3))
  MAPE.append(round(mean_absolute_percentage_error(y_test, y_predict), 3)*100)
  MSE.append(round(mean_squared_error(y_test, y_predict), 3))
  RMSE.append(round(np.sqrt(mean_squared_error(y_test, y_predict)), 3))

  return print('Resultados adicionados')

# Define lists to store model results
model_name = []
R2 = []
MAE = []
MSE= []
MAPE = []
RMSE = []

# Define a evaluation function putting all functions together

def evaluation(model, x_train_transformed, x_test_transformed, y_train, y_test):
  y_pred_train = model.predict(x_train_transformed)
  y_predict = model.predict(x_test_transformed)
  evaluate(y_test, y_predict, model)
  feature_importance(model)
  append_results(model, y_test, y_predict)

  print(f"Score Treino: {model.score(x_train, y_train)}\n")
  print(f"Score Teste: {model.score(x_test, y_test)}\n")

  return print('Função completa aplicada \n')

# Apply pre process function

pre_encoder(df)

df.sample(3)

# Defining columns to encode

ohe_cols= ['Certificate']

te_cols= ['Released_Year', 'Genre', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']

# Instatiate the encoders

target_enc = TargetEncoder(smooth='auto', target_type='continuous')

ohe_enc = OneHotEncoder(handle_unknown='ignore')

# Making column transformer

col_trans= make_column_transformer(
    (ohe_enc, ohe_cols),
    (target_enc, te_cols),
    remainder= 'passthrough')

# Creating a pipeline to encode

def passthrough_func(X):
    print("Data after ColumnTransformer:", type(X), X.shape)
    df= pd.DataFrame(X)
    for col in df.columns:
      df[col] = df[col].astype(float)
    return df

enc_pipeline= make_pipeline(col_trans,
                        FunctionTransformer(passthrough_func, validate=False)
                        )

"""##Modelo"""

#  Train test split

x = df.drop(columns= ['IMDB_Rating'], axis= 1)
y = df['IMDB_Rating']

x_train, x_test, y_train, y_test = train_test_split( x, y, test_size= 0.3, random_state= 71)

# Show train test dataset shapes

display(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
# display(x_train.info())

x_train.sample()

model= XGBRegressor(eval_metric= ['mae', 'mape'],
                    objective= 'reg:linear',
                    learning_rate= 0.01,
                    max_depth= 5,
                    n_estimators= 500,
                    gama= 0.1,
                    reg_alpha= 0,
                    reg_lambda= 0,
                    subsample= 0.5,
                    random_state= 71)

# Fit and predict

x_train= enc_pipeline.fit_transform(x_train, y_train)
x_test= enc_pipeline.transform(x_test)

model.fit(x_train, y_train, eval_set= [(x_train, y_train), (x_test, y_test)])

y_predict = model.predict(x_test)
evaluation(model, x_train, x_test, y_train, y_test)

# Comparing y_true and y_predict

# Calculate absolute error
abs_error = (y_test - y_predict).abs() # Calculate the absolute difference directly

# Calculate percentage error
percent_error = (y_predict - y_test) / y_test * 100  # Use y_test as the denominator


# Create a comparison dataframe
df_comparison = pd.DataFrame({
    'Rating Real': y_test,
    'Rating Previsto': round(y_predict, 2),
    'Erro Absoluto': round(abs_error, 2),
    'Erro Percentual': round(percent_error, 2)
})

# Print the comparison dataframe
print(df_comparison)
print('---------------------------------------------------------------------\n')

print(f'A média do erro absoluto foi de {abs_error.mean()}\n')
print(f'A média do erro percentual foi de {percent_error.mean()}')

"""##Realizando Previsão do Dataset df_pred (input)"""

df_pred

# Loop for all columns and include them on dataset

for col in df:
  if col not in df_pred:
    df_pred[col] = 1
  else:
    pass

# Apply pre process function

pre_encoder(df_pred)

df_pred

#  Define X and Target

x_p= df_pred.drop(columns= ['IMDB_Rating'], axis= 1)
y_p= df_pred['IMDB_Rating']

display(x_p, y_p)

# Applying model

x_p = enc_pipeline.transform(x_p)

y_pred = model.predict(x_p)

# Make Prediction

display(np.round((y_pred) ,2))
display(len(y_pred))

display(f'O Rating Previsto Para Este Filme é {np.round((y_pred), 1)}')

"""###Salvando modelo treinado em formato pkl"""

import pickle

# Saving to pickle

with open ('model_pickle', 'wb') as d:
  pickle.dump(model, d)

#Saving pickle file

with open ('model_pickle', 'rb') as d:
  mp = pickle.load(d)

# Opening saved pickle file to test it

mp.predict(x_p)

display(f'O Rating Previsto Para Este Filme é {np.round(mp.predict(x_p), 1)}')

# Gives the same answer as modelling

"""De acordo com o site do IMDB, o Rating deste filme é 9.1

O Modelo classificou como 8.7

Erro de 0.3 pontos, ou aproximadamente 3.5 %
"""