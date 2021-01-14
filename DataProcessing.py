def get_ing(df):
    recipe = df['ingredients'].to_list()
    ing = []
    for r in recipe:
        for el in r.split(','):
            ing.append(el)
    return set(ing)

