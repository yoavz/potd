import random
import math
import json

import numpy
import sklearn
from sklearn import svm
from sklearn import linear_model
from sklearn import tree 
from sklearn import ensemble
from pprint import pprint

import constants

def load():
    with open('data/pizzas.json') as f:
        return json.load(f, encoding="utf-8")

def base_class(pizza):
    return constants.BASES.index(pizza.base)

def train_bases(p, prev=7):
    # make a copy
    pizzas = list(p)

    # sort by date
    pizzas = sorted(pizzas, key=lambda x: x.timestamp)

    X = list()

    for i, p in enumerate(pizzas):
        # time features
        x = p.to_feature_vector()

        # previous bases
        prev_bases = list()
        for j in range(1,1+prev):
            if i-j>=0:
                prev_bases.append(float(base_class(pizzas[i-j])))
                x += pizzas[i-j].ingred_feature_vector()
            else:
                prev_bases.append(0.0)
                x += [0.0]
        x += prev_bases

        print x
        X.append(x)

    # numpy and normalize
    X = numpy.array(X)
    X = sklearn.preprocessing.normalize(X)

    # grab all bases
    Y = numpy.array([base_class(p) for p in pizzas])

    assert len(Y) == len(X)

    split = int(math.floor(len(X) * 0.6))

    # randomly shuffle, split, and train 10 times
    scores = list()

    numpy.random.shuffle(X)
    train_X = X[:split]
    train_Y = Y[:split]
    test_X = X[split:]
    test_Y = Y[split:]
    model = ensemble.RandomForestClassifier(n_estimators=1000, verbose=True) 
    model.fit(train_X, train_Y)

    print "Prev bases: " + str(prev)
    print "Score: " + str(model.score(test_X, test_Y)) 

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
    
    # for i in range(10):
    #     train_bases(pizzas, prev=i)
    train_bases(pizzas, prev=100)
