import json
import datetime
from pprint import pprint

import plotly.plotly as py
from plotly.graph_objs import *

import constants

def load():
    with open('data/pizzas.json') as f:
        return json.load(f)

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


# passed in a list of pizza objects,
# returns a dictionary of token counts
def count_tokens(data):
    from nltk.tokenize import word_tokenize

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


    counts = dict()
    for d in data:
        tokens = extract_tokens(d)
        for t in tokens:
            if counts.has_key(t):
                counts[t] += 1
            else:
                counts[t] = 0
    return counts 

def cheese_counts(counts):
    return { c: counts.get(c) for c in constants.CHEESES }

def cheese_overall(data):

    colors = list(constants.COLORS)
    counts = count_tokens(data)
    cheeses = cheese_counts(counts)

    ret = []

    for c, v in cheeses.iteritems():
        color = colors.pop()
        ret.append({
            "value": v,
            "label": c,
            "color": color, 
        })

    return ret 

def cheese_by_month(data):
    
    colors = list(constants.COLORS)
    by_month = seperate_months(data)
    by_month_counts = {m: count_tokens(v) for m, v in by_month.iteritems()}

    months = by_month.keys() 
    datasets = []

    for cheese in constants.CHEESES:  
        color = colors.pop()
        datasets.append({
            "label": cheese,
            "fillColor": color,
            "data": [ by_month_counts[m].get(cheese) or 0 for m in months ] 
        })

    return {
        "labels": months,
        "datasets": datasets
    }

if __name__ == '__main__':

    data = load()
    
    gen_json('cheese_overall', cheese_overall(data))
    gen_json('cheese_by_month', cheese_by_month(data))
