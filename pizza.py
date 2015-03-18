import datetime

from nltk.tokenize import word_tokenize

import constants

def log(m):
    print '(Pizza): ' + str(m)

class PizzaException(Exception):
    pass

class Pizza(object):
    '''
    A POTD for a given day
    '''

    def __init__(self, pizza):
        self.from_instagram(pizza)
        pass

    def __repr__(self):
        return self.base + " with " + ", ".join(self.ingredient_list())

    def _count_ingredients(self, ingredients):
        '''
        Given a list of ingredients, of which each may be multiple words,
        this function searches this pizzas description for the ingredient
        and specifies it in the ingredient table
        '''

        def token_match(a, b):
            for w1, w2 in zip(a, b):
                if not w2.startswith(w1):
                    return False
            return True

        for ingredient in ingredients:
            ingredient_tokens = ingredient.lower().split(" ")
            ingredient_len = len(ingredient_tokens)
            for i in range(len(self.tokens)-ingredient_len+1):
                if token_match(ingredient_tokens, self.tokens[i:i+ingredient_len]):
                    self.ingredients[ingredient] = True
                    break

    def _parse_base(self):
        intersection = [b for b in constants.BASES if b in self.tokens]
        if len(intersection) == 0:
            raise PizzaException("No base found")
        elif len(intersection) > 1:
            raise PizzaException("Multiple bases found")
        else:
            self.base = intersection[0]

    def _parse_ingredients(self):
        self.ingredients = {i: False for i in constants.INGREDIENTS}
        self._count_ingredients(constants.INGREDIENTS)

        if len(self.ingredient_list()) == 0:
            raise PizzaException("No ingredients found")

        # specific cases w/ ambiguous ingredients
        if self.ingredients.get("bacon marmalad"):
            self.ingredients["bacon"] = False
        if self.ingredients.get("chicken sausage"):
            self.ingredients["chicken"] = False
        if self.ingredients.get("sundried tomato"):
            self.ingredients["tomato"] = False

    def ingredient_list(self):
        return [i for i, v in self.ingredients.iteritems() if v == True]

    def from_instagram(self, instagram_obj):
        '''
        Populate a pizza object from 
        downloaded instagram data
        '''

        self.raw_data = instagram_obj

        def attr(name):
            if not name in instagram_obj:
                log("Missing attr: " + name)
                return None
            else:
                return instagram_obj.get(name)
                
        self.raw_timestamp = attr("created_time") 
        self.timestamp = datetime.datetime.fromtimestamp(int(self.raw_timestamp)) 
        
        if not instagram_obj.get("caption"):
            raise PizzaException("Missing caption")

        self.description = attr("caption").get("text")
        self.tokens = word_tokenize(self.description) 
        self.tokens = [t.replace("-", "").lower().encode('utf-8') for t in self.tokens] 

        self._parse_base()
        self._parse_ingredients()
