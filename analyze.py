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

def base_avg_attr(pizzas, attr):
    '''
    Input: a list of pizza objects
    Output: a dictionary of avg attr for base counts 
    '''
    bases = dict()
    for p in pizzas:
        v = getattr(p, attr)
        if p.base in bases:
            bases[p.base].append(v)
        else:
            bases[p.base] = [v]

    bases = { i: round(float(sum(v))/float(len(v)), 2) for i, v in bases.iteritems() }

    return bases

def base_avg_likes(pizzas):
    return base_avg_attr(pizzas, 'like_count')

def base_avg_comments(pizzas):
    return base_avg_attr(pizzas, 'comment_count')


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

def ingredients_avg_likes(pizzas):
    ingreds = dict()
    for p in pizzas:
        for ingred in p.ingredient_list():
            if ingred in ingreds:
                ingreds[ingred].append(p.like_count)
            else:
                ingreds[ingred] = [p.like_count]

    # average all like counts
    ingreds = { i: round(float(sum(v))/float(len(v)), 2) for i, v in ingreds.iteritems() }
    return ingreds

def ingredients_avg_comments(pizzas):
    ingreds = dict()
    for p in pizzas:
        for ingred in p.ingredient_list():
            if ingred in ingreds:
                ingreds[ingred].append(p.comment_count)
            else:
                ingreds[ingred] = [p.comment_count]

    # average all comment counts
    ingreds = { i: round(float(sum(v))/float(len(v)), 2) for i, v in ingreds.iteritems() }
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

def base_counts_by_format(pizzas, _format):
    '''
    Input: list of pizza objects and a strftime format
    Output: base counts of pizza grouped by the strftime format
    '''

    seperated_pizzas = seperate_by_strftime(pizzas, _format)

    counts = { d: base_counts(v) for d, v in seperated_pizzas.iteritems() }
    counts = { d: sorted(v.items(), key=lambda x: x[1], reverse=True) for d, v in counts.iteritems() }

    return counts 

def base_counts_by_day(pizzas):
    return base_counts_by_format(pizzas, "%A")

def base_counts_by_month(pizzas):
    return base_counts_by_format(pizzas, "%B")

def like_counts_by_format(pizzas, _format):
    '''
    Input: list of pizza objects and a strftime format
    Output: average like counts grouped by the _format
    '''

    seperated_pizzas = seperate_by_strftime(pizzas, _format)

    counts = { d: round(float(sum([p.like_count for p in v]))/float(len(v)), 2)
               for d, v in seperated_pizzas.iteritems() }

    return counts

def like_counts_by_day(pizzas):
    return like_counts_by_format(pizzas, "%A")

def like_counts_by_month(pizzas):
    return like_counts_by_format(pizzas, "%B")

def comment_counts_by_format(pizzas, _format):
    '''
    Input: list of pizza objects and a strftime format
    Output: average comment counts grouped by the _format
    '''

    seperated_pizzas = seperate_by_strftime(pizzas, _format)

    counts = { d: round(float(sum([p.comment_count for p in v]))/float(len(v)), 2)
               for d, v in seperated_pizzas.iteritems() }

    return counts

def comment_counts_by_day(pizzas):
    return comment_counts_by_format(pizzas, "%A")

def comment_counts_by_month(pizzas):
    return comment_counts_by_format(pizzas, "%B")

def combos_pizzas(pizzas, N=2):
    '''
    Input: list of pizza object and an integer N
    Output: dictionary mapping ingredient combinations (length N) to their respective pizza objects
        {
            ["brocollini", "chicken"]: [<Pizza>, <Pizza>]
            ...
        }
    '''

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
    return { c: len(v) for c, v in combos_pizzas(pizzas, N).iteritems() }

def base_pairings_pizzas(pizzas, N=1):
    '''
    Input: list of pizza object and an integer N
    Output: 
    '''
    
    pairings = dict()

    for p in pizzas:
        ingredients = p.ingredient_list()
        if len(ingredients) < N:
            # print "less than " + str(N) + " ingredients: " + p.description
            continue
        for combo in itertools.combinations(ingredients, N):
            pairing = [p.base] + list(combo)
            pairing = tuple(pairing)
            if pairing in pairings:
                pairings[pairing].append(p)
            else:
                pairings[pairing] = [p]

    return pairings

def base_pairings(pizzas, N=1):
    return { c: len(v) for c, v in base_pairings_pizzas(pizzas, N).iteritems() }


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

def chartjs_bar_graph(counts, sorted_labels=None):
    colors = list(constants.COLORS) * len(counts)

    if sorted_labels:
        counts_tups = [(l, counts[l]) for l in sorted_labels]
    else:
        counts_tups = [(c, v) for c, v in counts.iteritems()]
        counts_tups = sorted(counts_tups, key=lambda x: x[1], reverse=True)

    return {
        "labels": [l[0] for l in counts_tups],
        "datasets": [{
            "data": [v[1] for v in counts_tups],
            "fillColor": colors.pop(),
            "label": "idunno"
        }]
    }

def chartjs_multibar_graph(multi_counts, sorted_labels=None):

    colors = list(constants.COLORS) * len(multi_counts)

    keys = [k[0] for k in multi_counts.values()[0]]

    if sorted_labels:
        labels = sorted_labels
    else:
        labels = multi_counts.keys()

    def value_of(key, label):
        for tup in multi_counts[label]:
            if tup[0] == key:
                return tup[1]

    return {
        "labels": labels, 
        "datasets": [{
            "data": [value_of(key, label) for label in labels],
            "fillColor": colors.pop(),
            "label": key 
        } for key in keys]
    }

def chartjs_scatter_graph(datasets):

    ret = []
    colors = list(constants.COLORS) * len(datasets)

    for d, v in datasets.iteritems():
        ret.append({
            "label": d,
            "pointColor": colors.pop(),
            "data": [ { "x": t[0], "y": t[1] } for t in v ]
        })

    return ret

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

    # bases by day/month
    b_by_month = base_counts_by_month(pizzas)
    months = [m for m in constants.MONTHS if m in b_by_month.keys()]
    gen_json('base_by_month', chartjs_multibar_graph(b_by_month, sorted_labels=months))

    b_by_day = base_counts_by_day(pizzas)
    days = [d for d in constants.WEEKDAYS if d in b_by_day.keys()]
    gen_json('base_by_weekday', chartjs_multibar_graph(b_by_day, sorted_labels=days))

    # ingredients by day/month 
    i_by_month = ingredient_counts_by_month(pizzas, threshold=3)
    # months = [m for m in constants.MONTHS if m in i_by_month.keys()]
    # gen_json('ingredients_by_month', chartjs_multibar_graph(i_by_month, sorted_labels=months))

    i_by_day = ingredient_counts_by_day(pizzas, threshold=3)
    # days = [d for d in constants.WEEKDAYS if d in i_by_day.keys()]
    # gen_json('ingredients_by_weekday', chartjs_multibar_graph(i_by_day, sorted_labels=days))

    # ingredient pairings 
    two_combs = combos(pizzas, N=2)
    two_combs_tups = sorted(two_combs.items(), key=lambda x: x[1], reverse=True)
    two_combs = dict(two_combs_tups[:20])
    gen_json('ingredient_pairings', chartjs_bar_graph(two_combs))

    # base ingredient pairings
    pairings = base_pairings(pizzas)
    pairings_tups = sorted(pairings.items(), key=lambda x: x[1], reverse=True)
    pairings = dict(pairings_tups[:20])
    gen_json('base_ingredient_pairings', chartjs_bar_graph(pairings))

    # likes/comments by ingredient
    i_likes = ingredients_avg_likes(pizzas)
    i_comments = ingredients_avg_comments(pizzas)
    i_labels = [i[0] for i in sorted(i_likes.items(), key=lambda x: x[1], reverse=True)]
    lc_by_ingred = { i: [('likes', i_likes[i]), ('comments', i_comments[i])]
                     for i in i_labels }
    gen_json('ingredients_likes', chartjs_multibar_graph(lc_by_ingred, sorted_labels=i_labels))

    # likes/comments by base
    b_likes = base_avg_likes(pizzas)
    b_comments = base_avg_comments(pizzas)
    b_labels = [i[0] for i in sorted(b_likes.items(), key=lambda x: x[1], reverse=True)]
    lc_by_base = { b: [('likes', b_likes[b]), ('comments', b_comments[b])]
                     for b in b_labels }
    gen_json('base_likes', chartjs_multibar_graph(lc_by_base, sorted_labels=b_labels))

    # likes/comments by weekday
    l_by_day = like_counts_by_day(pizzas)
    c_by_day = comment_counts_by_day(pizzas)
    lc_by_day = { d: [('likes', l_by_day[d]), ('comments', c_by_day[d])] for d in days }
    gen_json('likes_by_weekday', chartjs_multibar_graph(lc_by_day, sorted_labels=days))

    # likes by time posted
    def minutes_since_nine(timestamp):
        nine = datetime.datetime.combine(timestamp.date(), datetime.time(9, 0, 0))
        return round((timestamp - nine).total_seconds() / float(60), 2)

    l_by_time = [(minutes_since_nine(p.timestamp), p.like_count) for p in pizzas
                 if minutes_since_nine(p.timestamp) < 200]
    c_by_time = [(minutes_since_nine(p.timestamp), p.comment_count) for p in pizzas
                 if minutes_since_nine(p.timestamp) < 200]
    scatter = chartjs_scatter_graph({"likes": l_by_time, "comments": c_by_time})
    gen_json('likes_by_time', scatter)
