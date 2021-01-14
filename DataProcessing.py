def get_ing(df):
    recipe = df['ingredients'].to_list()
    ing = []
    for r in recipe:
        for el in r.split(','):
            ing.append(el)
    return set(ing)

import numpy as np
import re
import pandas as pd

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


def ingredients_clean(x):
  x = x.split(",")
  l = "" 

  for i in range(len(x)):
    x[i] = x[i].replace("['", "").strip()
    x[i] = x[i].replace("[", "").strip()
    x[i] = x[i].replace("]", "").strip()
    x[i] = x[i].replace('["', "").strip()
    x[i] = x[i].replace('"]', "").strip()
    x[i] = x[i].replace("']", "").strip()
    x[i] = re.sub("\(environ [0-9]* g\)", "", x[i])
    x[i] = re.sub("g[^a-z]", "", x[i]) 
    x[i] = re.sub("[0-9]* g[^a-z]", "", x[i])
    x[i] = re.sub("[0-9]", "", x[i])
    x[i] = x[i].replace("g d", "").strip()
    x[i] = x[i].replace("cl de ", "").strip()
    x[i] = x[i].replace("kg de ", "").strip()
    x[i] = x[i].replace("Kg de ", "").strip()
    x[i] = x[i].replace("kg d ", " ").strip()
    x[i] = x[i].replace("Kg d ", " ").strip()
    x[i] = x[i].replace("cl d", " ").strip()
    x[i] = x[i].replace("ml de ", "").strip()
    x[i] = x[i].replace("l de ", "").strip()
    x[i] = x[i].replace("L de ", "").strip()
    x[i] = x[i].replace('"', " ").strip()
    x[i] = x[i].replace("'", " ").strip()
    x[i] = x[i].replace("cuillères à soupe de", " ").strip()
    x[i] = x[i].replace("cuillères à café de", " ").strip()
    x[i] = x[i].replace("cuillère à café de", " ").strip()
    x[i] = x[i].replace("cuillère à soupe de", " ").strip()
    x[i] = x[i].replace("cuillères à soupe d", " ").strip()
    x[i] = x[i].replace("cuillère à soupe d", " ").strip()
    x[i] = x[i].replace("cuillère à café d", " ").strip()
    x[i] = x[i].replace("(facultatif)", "").strip()
    
    if i != len(x)-1:
      l += x[i]+","
    else:
      l += x[i]
  
  return l.strip()



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
  df["ingredients_st"] = df["ingredients_clean"].apply(lambda x: func_clean(x))

  df['likes'] = df['likes'].apply(lambda x : likes(x))

  df['time_preparation'].fillna(0,inplace=True)

  df['total_time'].fillna(0,inplace=True)

  df['number people'] = df['number people'].apply(lambda x : 0 if x=='no data' else int(x))

  df['cost']=df['cost'].apply(lambda x : {'bon marché':1, 'Coût moyen':2, 'assez cher':3}.get(x,0))
  df['difficulty']=df['difficulty'].apply(lambda x : {'très facile':1, 'facile':2, 'Niveau moyen':3,'difficile':4 }.get(x,0))

  return df


# recommandation algo to choose recipe
def choose_recipe(df,url):


  idx = df[df['links'] == url].index[0]

  tfidf_matrix = tfidf.fit_transform(df['ingredients_st'])

  cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

  sim_scores = list(enumerate(cosine_sim[idx]))

  df_temp=pd.DataFrame(sim_scores)
  df_temp=df_temp.rename({1:'cosine_score'},axis=1)

  df1=pd.concat([df,df_temp],axis=1)
  
  col=['rate','likes','total_time','time_preparation','time_cooking','cost','difficulty','category','gender','number people']

  col_trans= make_column_transformer(     
      (OneHotEncoder(), ['category','gender']),
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

  return df_ind
