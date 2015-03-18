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

def base_counts(pizzas):
    '''
    Input: a list of pizza objects
    Output: a dictionary of counts of all bases
    '''

    bases = dict()
    for p in pizzas:
        if p.base in bases:
            bases[p.base] += 1
        else:
            bases[p.base] = 0
    return bases

def ingredient_counts(pizzas):
    '''
    Input: a list of pizza objects
    Output: a dictionary of counts of all ingredients
    '''

    ingreds = dict()
    for p in pizzas:
        for ingred in p.ingredient_list():
            if ingred in ingreds:
                ingreds[ingred] += 1
            else:
                ingreds[ingred] = 1 
    return ingreds


# def base_by_month(data):
#     
#     colors = list(constants.COLORS)
#     by_month = seperate_months(data)
#     by_month_counts = {m: count_tokens(v) for m, v in by_month.iteritems()}
#
#     months = by_month.keys() 
#     datasets = []
#
#     for base in constants.BASES:  
#         color = colors.pop()
#         datasets.append({
#             "label": base,
#             "fillColor": color,
#             "data": [ by_month_counts[m].get(base) or 0 for m in months ] 
#         })
#
#     return {
#         "labels": months,
#         "datasets": datasets
#     }

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

def chartjs_bar_graph(counts):
    colors = list(constants.COLORS) * len(counts)

    counts_tups = [(c, v) for c, v in counts.iteritems()]
    counts_tups = sorted(counts_tups, key=lambda x: x[1], reverse=True)

    return {
        "labels": [l[0] for l in counts_tups],
        "datasets": [{
            "data": [v[1] for v in counts_tups],
            "color": colors.pop(),
            "label": "idunno"
        }]
    }

########
# MAIN #
########

from pizza import Pizza, PizzaException

if __name__ == '__main__':

    data = load()
    pizzas = list()
    
    problems = {} 
    for d in data:
        try:
            pizzas.append(Pizza(d))
        except PizzaException as e:
            problem = str(e)
            if problem in problems: 
                problems[problem] += 1
            else: 
                problems[problem] = 0 

    print str(len(pizzas)) + " pizzas parsed. "
    print str(sum([p for p in problems.values()])) + " pizzas tossed. "

    gen_json('base_overall', chartjs_pie_graph(base_counts(pizzas)))
    gen_json('ingredients_overall', chartjs_bar_graph(ingredient_counts(pizzas)))
