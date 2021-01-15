import numpy as np
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder, MinMaxScaler,StandardScaler
from sklearn.pipeline import make_pipeline
from random import *
import string

import nltk
nltk.download('popular')

def ing_list(df):
  total_ingredients_= []
  for i in df["ingredients"]:
    total_ingredients_.append(i)

  return total_ingredients_



def time_format(x):
  x=re.sub(' \d+ sec','',x)
  if "h" in x:
    x = x.split("h")
    min = int(x[0])*60
    b = x[-1]
    if b.isdigit():
      total_min = min + int(b)
    else:
      total_min = min

  elif "min" in x:
    x = x.replace(" min", "")
    total_min = int(x)
  else:
    total_min = np.nan

  return total_min


def max_len(l):
  compteur = 0
  result = ""
  for item in l:
    if len(item) > compteur:
      compteur = len(item)
      result = item
  return result


def ingredients_clean(x,total_ingredients_ ):
  ing_to_delete = ["poivre", "sel", "oeuf", "beurre", "huile", "sucre", 
                 "farine", "persil", "ciboulette", "échalotte", "oignon"
                 ]
  x = x.split(",")
  l = "" 
  for i in range(len(x)):
    total = []
    for ing in total_ingredients_:     
      if ing in x[i]: 
          total.append(ing)  
    x[i] = max_len(total)
    for value in ing_to_delete:
      if value in x[i]:
        x[i] =""
    if x[i] != "":
      if i != len(x)-1:
        l += (x[i]+",").strip()
      else:
        l += x[i].strip()
  if len(l) != 0:      
    if l[-1] == ",":
      return l[:-1]
  return l.strip()


def freq_ingredients(sentence):
  ingre_frequencies = nltk.FreqDist(sentence.split(","))
  return ingre_frequencies

def total_ingredients(df):
  total_ingre = ""
  for value in df["ingredients_clean"]:
    total_ingre += value.strip() +","
  return total_ingre.strip()


def DataProcesing(df):
  df["time_preparation"] = df["time_preparation"].apply(lambda x: time_format(x))
  df["time_cooking"] = df["time_cooking"].apply(lambda x: time_format(x))
  df["total_time"] = df["total_time"].apply(lambda x: time_format(x))
  f["likes"] = df["likes"].apply(lambda x: likes(x))
  df['time_cooking'].fillna(0, inplace = True)
  df["ingredients"] = df["ingredients"].apply(lambda x: "".join(x))
  df["ingredients"] = df["ingredients"].apply(lambda x: x[2:-2])
  df["ingredients"] = df["ingredients"].apply(lambda x: x.replace("',", " "))
  df["ingredients"] = df["ingredients"].apply(lambda x: x.replace(" '", " "))

  l_ingre = []
  for item in range(len(df["ingredients"])):
    ingredients = df.loc[item,"ingredients"]
    l_ = ingredients_clean(ingredients)
    l_ingre.append(l_)

  columns_ = list(df.columns)
  columns_.append("ingredients_clean")  
  df = pd.concat([df, pd.DataFrame(l_ingre)], axis=1)
  df.columns = columns_
 
  return df



def func_clean(x):
  stops_fr = nltk.corpus.stopwords.words("french") 
  res = ''
  for word in nltk.word_tokenize(re.sub("[^a-z-éèîàûô\, ']", "", x.lower())): 
      if word not in stops_fr: 
          res += word + " "
  return res.strip()


def likes(x):
  if 'k' in x:
    x=x.replace('k','')
  return int(float(x)*1000)


def DataProcessing(df):
  df["time_preparation"] = df["time_preparation"].apply(lambda x: time_format(x))
  df["time_cooking"] = df["time_cooking"].apply(lambda x: time_format(x))
  df["total_time"] = df["total_time"].apply(lambda x: time_format(x))
  df['time_cooking'].fillna(0, inplace = True)
  df["ingredients"] = df["ingredients"].apply(lambda x: "".join(x))
  df["ingredients"] = df["ingredients"].apply(lambda x: x[2:-2])
  df["ingredients"] = df["ingredients"].apply(lambda x: x.replace("',", " "))
  df["ingredients"] = df["ingredients"].apply(lambda x: x.replace(" '", " "))

  l_ingre = []
  for item in range(len(df["ingredients"])):
    ingredients = df.loc[item,"ingredients"]
    l_ = ingredients_clean(ingredients)
    l_ingre.append(l_)

  columns_ = list(df.columns)
  columns_.append("ingredients_clean")  
  df = pd.concat([df, pd.DataFrame(l_ingre)], axis=1)
  df.columns = columns_
 

  df['likes'] = df['likes'].apply(lambda x : likes(x))

  df['time_preparation'].fillna(0,inplace=True)

  df['total_time'].fillna(0,inplace=True)

  df['number people'] = df['number people'].apply(lambda x : 0 if x=='no data' else int(x))

  df['cost']=df['cost'].apply(lambda x : {'bon marché':1, 'Coût moyen':2, 'assez cher':3}.get(x,0))
  df['difficulty']=df['difficulty'].apply(lambda x : {'très facile':1, 'facile':2, 'Niveau moyen':3,'difficile':4 }.get(x,0))

  return df


# recommandation algo to choose recipe
def choose_recipe(df,url):

  tfidf = TfidfVectorizer(ngram_range = (1, 2))

  idx = df[df['links'] == url].index[0]

  tfidf_matrix = tfidf.fit_transform(df['ingredients_st'])

  cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

  sim_scores = list(enumerate(cosine_sim[idx]))

  df_temp=pd.DataFrame(sim_scores)
  df_temp=df_temp.rename({1:'cosine_score'},axis=1)

  df1=pd.concat([df,df_temp],axis=1)
  
  col=['rate','likes','total_time','time_preparation','time_cooking','cost','difficulty','category','Xmas recipe','number people']

  col_trans= make_column_transformer(     
      (OneHotEncoder(), ['category','Xmas recipe']),
      (OrdinalEncoder(), ['cost','difficulty']),
      (StandardScaler(), ['rate','likes','total_time','time_preparation','time_cooking','number people']),
      remainder='passthrough')
  
  X = col_trans.fit_transform(df1[col])
  y = df1['links']
  
  modelKNN = KNeighborsClassifier(n_neighbors=16,weights='distance')

  
  modelKNN.fit(X,y)
  
  
  l_distances = list(modelKNN.kneighbors(col_trans.transform(df1[df1['links']==url][col]))[0][0])  
  l_indexs= list(modelKNN.kneighbors(col_trans.transform(df1[df1['links']==url][col]))[1][0]) 
  
  result=list(zip(l_distances,l_indexs))
  liste_index=[]

  for i in result[1:]:
    liste_index.append(i[1])   
  df2=df1.iloc[liste_index,:]

  df2=df2.reset_index(drop=True)

  liste_ind = sample(list(df2.index), 8)
  df_ind = df2.loc[liste_ind,:]           
  df_ind = df_ind.sort_values(by='rate', ascending=False) 
  df_ind =df_ind.head(3) 

  return df_ind.reset_index(drop=True)

def moy(df):
  return round(df['sum']/df['total'],2)

def get_df_to_figcomp(df):
  df["Xmas recipe"]  = "Noël"
  df['diff_num'] = df['difficulty'].apply(lambda x : {'très facile':1.25, 'facile':2.5, 'Niveau moyen':3.75, 'difficile':5}.get(x,0))
  df['cost_num'] = df['cost'].apply(lambda x : {'bon marché':1.66, 'Coût moyen':3.3, 'assez cher':5}.get(x,0))
  df_moy_diff=df.groupby(['Xmas recipe','category'], as_index=False).diff_num.sum()
  df_tot_diff=df.groupby(['Xmas recipe','category'], as_index=False).rate.count()
  dff_diff=pd.concat([df_moy_diff, df_tot_diff['rate']], axis=1).rename(columns={'category':'categ','Xmas recipe':'gend','diff_num':'sum','rate':'total'})

  df_moy_cost=df.groupby(['Xmas recipe','category'], as_index=False).cost_num.sum()
  df_tot_cost=df.groupby(['Xmas recipe','category'], as_index=False).rate.count()
  dff_cost=pd.concat([df_moy_cost, df_tot_cost['rate']], axis=1).rename(columns={'category':'categ','Xmas recipe':'gend','cost_num':'sum','rate':'total'})

  df_moy_rate=df.groupby(['Xmas recipe','category'], as_index=False).rate.sum()
  df_tot_rate=df.groupby(['Xmas recipe','category'], as_index=False).diff_num.count()
  dff_rate=pd.concat([df_moy_rate, df_tot_rate['diff_num']], axis=1).rename(columns={'category':'categ','Xmas recipe':'gend','rate':'sum','diff_num':'total'})

  dff_diff['moy']=dff_diff.apply(moy,axis=1)
  dff_diff['theme']='Difficulty'

  dff_cost['moy']=dff_cost.apply(moy,axis=1)
  dff_cost['theme']='Coût'

  dff_rate['moy']=dff_rate.apply(moy,axis=1)
  dff_rate['theme']='Note'

  dff = pd.concat([dff_diff,dff_cost,dff_rate])

  return dff
