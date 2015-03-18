import json
import datetime
from pprint import pprint

from nltk.tokenize import word_tokenize

import constants

def load():
    with open('data/pizzas.json') as f:
        return json.load(f, encoding="utf-8")

def gen_json(filename, data):
    if not filename.endswith('.json'):
        filename += '.json'

    with open('charts/' + filename, 'w') as f:
        json.dump(data, f)

# Input: Raw data [ { pizza }, { pizza }, ... ]
# Output: Data seperated by month:
#   {
#       "January": [ { pizza }, { pizza }, ... ] 
#       "February": [ { pizza }, { pizza }, ... ] ,
#       ...
#   } 
def seperate_months(data):

    def to_month(timestamp):
        if not timestamp:
            print "Warning, no timestamp"
            return "unknown"
        return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%B")

    months = dict()
    for d in data:
        month = to_month(d.get("created_time"))
        if months.get(month):
            months[month].append(d)
        else:
            months[month] = [d]

    counts = { k: len(months.get(k)) for k in months }

    return months

# Input: a pizza object
# Output: tokens of all the text
def extract_tokens(pizza):
    if not pizza.get("caption"):
        print "Warning: no caption found"
        return ""
    text = pizza["caption"].get("text")
    if not text:
        print "Warning: no text found"
        return ""

    # to lowercase
    text = text.lower()

    return word_tokenize(text)

# passed in a list of pizza objects,
# returns a dictionary of token counts
def count_tokens(data):

    counts = dict()
    for d in data:
        tokens = extract_tokens(d)
        for t in tokens:
            if counts.has_key(t):
                counts[t] += 1
            else:
                counts[t] = 0
    return counts 

# Input: List of pizza objects: [ { pizza }, { pizza }, ... ]
#        ingredient which may have multiple words, e.g. "roasted red peppers"
# counts the number of pizzas with each ingredient. A pizza can have more
# than one ingredient, but can only have one each of ingredient at most

# Output: Dict of ingredient counts
#         {
#           "roasted red peppers": 59,
#           "pineapple": 34
#         }
def ingredient_counts(data, ingredients):
    counts = { v: 0 for v in ingredients }

    # a - the actual ingredient
    # b - the text we're matching against
    def token_match(a, b):
        for w1, w2 in zip(a, b):
            if not w2.startswith(w1):
                return False
        return True

    for pizza in data:
        tokens = extract_tokens(pizza)
        # "sun-dried" vs "sundried"
        tokens = [t.replace("-", "").encode('utf-8') for t in tokens]
        
        for ingredient in ingredients:
            ingredient_tokens = ingredient.split(" ")
            ingredient_len = len(ingredient_tokens)
            for i in range(len(tokens)-ingredient_len+1):
                # if tokens[i].startswith("broccolini"):
                #     print tokens[i]
                if token_match(ingredient_tokens, tokens[i:i+ingredient_len]):
                    counts[ingredient] += 1
                    break

    return counts

#########
# BASES #
#########

def base_counts(counts):
    return { c: counts.get(c) for c in constants.BASES }

def base_overall(data):

    colors = list(constants.COLORS)
    counts = count_tokens(data)
    bases = base_counts(counts)

    ret = []

    for c, v in bases.iteritems():
        color = colors.pop()
        ret.append({
            "value": v,
            "label": c,
            "color": color, 
        })

    return ret 

def base_by_month(data):
    
    colors = list(constants.COLORS)
    by_month = seperate_months(data)
    by_month_counts = {m: count_tokens(v) for m, v in by_month.iteritems()}

    months = by_month.keys() 
    datasets = []

    for base in constants.BASES:  
        color = colors.pop()
        datasets.append({
            "label": base,
            "fillColor": color,
            "data": [ by_month_counts[m].get(base) or 0 for m in months ] 
        })

    return {
        "labels": months,
        "datasets": datasets
    }



##############
# VEGETABLES #
##############

# Input: List of pizza objects: [ { pizza }, { pizza }, ... ]
# Output: Dict of ingredient counts
# {
#   "broccolini": 4
#   "peppadews": 42
# }
# ...

def count_vegetables(data):

    counts = ingredient_counts(data, constants.VEGETABLES)

    # don't double count tomato
    if counts.get("tomato") and counts.get("sundried tomato"):
        counts["tomato"] -= counts["sundried tomato"]

    return counts

############
# PROTEINS #
############

def count_proteins(data):

    counts = ingredient_counts(data, constants.PROTEINS)

    # don't double count bacon or chicken sausage
    if counts.get("bacon") and counts.get("bacon marmalad"):
        counts["bacon"] -= counts["bacon marmalad"]
    if counts.get("chicken sausage") and counts.get("sausage"):
        counts["sausage"] -= counts["chicken sausage"]

    return counts

############
# CHEESES #
############

def count_cheeses(data):
    return ingredient_counts(data, constants.CHEESES)


# Given arbitrary label: count dict, 
# generate chartjs data for it

def chartjs_pie_graph(counts):
    colors = list(constants.COLORS) * len(counts)

    ret = list()
    for c, v in counts.iteritems():
        color = colors.pop()
        ret.append({
            "value": v,
            "label": c,
            "color": color, 
        })
    return ret 

########
# MAIN #
########

if __name__ == '__main__':

    data = load()
    
    # bases
    gen_json('base_overall', base_overall(data))
    gen_json('base_by_month', base_by_month(data))

    # ingredients
    veggies = count_vegetables(data)
    proteins = count_proteins(data)
    cheeses = count_cheeses(data)

    ingredients = {}
    for d in [veggies, proteins, cheeses]:
        ingredients.update(d)
    gen_json('ingredients_overall', chartjs_pie_graph(ingredients))

    pprint(ingredients)
