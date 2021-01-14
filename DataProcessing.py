<<<<<<< HEAD
def get_ing(df):
    recipe = df['ingredients'].to_list()
    ing = []
    for r in recipe:
        for el in r.split(','):
            ing.append(el)
    return set(ing)

=======
import numpy as np

def time_format(x):
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
>>>>>>> 5a1b2ac530bde43c092c1a59b5d162525e374ebd
