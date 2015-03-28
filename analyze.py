import json
import datetime
import itertools
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

def seperate_by_strftime(pizzas, _format):
    '''
    Input: a list of pizza objects
    Output: a dictionary of _format to lists of pizza objects
            use python docs to determine strftime behavior.
    Example with a _format of "%A":
            { "Monday": [ <Pizza>,
                        ...
                        ]
              ...
            }
    '''
    seperated = dict()
    
    for p in pizzas:
        key = p.timestamp.strftime(_format)
        if key in seperated:
            seperated[key].append(p)
        else:
            seperated[key] = [p] 

    return seperated

def seperate_by_day(pizzas):
    ''' %A - Weekday as locale's full name, "Tuesday" '''
    return seperate_by_strftime(pizzas, "%A")

def seperate_by_month(pizzas):
    ''' %B - Month as locale's full name, "January" '''
    return seperate_by_strftime(pizzas, "%B")

def ingredient_counts_by_format(pizzas, _format, threshold=3):
    '''
    Input: list of pizza objects and a strftime format
    Output: ingredient counts of pizza grouped by the strftime format
    '''
    pizzas_by_day = seperate_by_strftime(pizzas, _format)

    ingred_counts = { d: ingredient_counts(v) for d, v in pizzas_by_day.iteritems() }
    ingred_counts = { d: sorted(v.items(), key=lambda x: x[1], reverse=True) for d, v in ingred_counts.iteritems() }
    ingred_counts = { d: v[:threshold] for d, v in ingred_counts.iteritems() }

    return ingred_counts

def ingredient_counts_by_day(pizzas, threshold=3):
    return ingredient_counts_by_format(pizzas, "%A", threshold)

def ingredient_counts_by_month(pizzas, threshold=3):
    return ingredient_counts_by_format(pizzas, "%B", threshold)

def combos_to_pizzas(pizzas, N=2):

    combos = dict()

    for p in pizzas:
        ingredients = p.ingredient_list()
        if len(ingredients) < N:
            # print "less than " + str(N) + " ingredients: " + p.description
            continue
        for combo in itertools.combinations(ingredients, N):
            if combo in combos:
                combos[combo].append(p)
            else:
                combos[combo] = [p]

    return combos

def combos(pizzas, N=2):
    return { c: len(v) for c, v in combos_to_pizzas(pizzas, N).iteritems() }

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

    # overall charts
    gen_json('base_overall', chartjs_pie_graph(base_counts(pizzas)))
    gen_json('ingredients_overall', chartjs_bar_graph(ingredient_counts(pizzas)))

    # seperate ingreds by day
    by_day = ingredient_counts_by_day(pizzas, threshold=3)
    by_month = ingredient_counts_by_month(pizzas, threshold=3)
    pprint(by_day)
    pprint(by_month)

    # combos
    two_combs = combos(pizzas, N=2)
    two_combs_tups = sorted(two_combs.items(), key=lambda x: x[1], reverse=True)
    two_combs = dict(two_combs_tups[:20])
    gen_json('ingredient_pairings', chartjs_bar_graph(two_combs))

    # three_combs = combos_to_pizzas(pizzas, N=3)
    # three_combs = { i: [p.raw_timestamp for p in ps] for i, ps in three_combs.iteritems() }
    # pprint(three_combs)
