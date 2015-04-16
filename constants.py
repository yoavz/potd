# -*- coding: utf-8 -*-

########
# MENU #
########

BASES = [ "marinara", "bianca", "margherita", "verde" ]

PROTEINS = [
    "bacon",
    "bacon marmalad",
    "anchovies",
    "pepperoni",
    "shrimp",
    "chicken",
    "chicken sausage",
    "soppressata",
    # official menu name is "prosciutto di parma", but
    # this word is sufficiently unique
    "prosciutto", 
    "rosemary ham",
    "salami",
    "sausage",
    "meatballs",
    "egg",
]

CHEESES = [
    "ricotta",
    # "scamorza" maybe used. TODO: check insta 
    "provolone",
    "gorgonzola",
    "feta",
    # menu name: "boschetto di tartufo"
    "boschetto",
    "fontina",
    "goat cheese",
    # menu name: "mozarella di bufala"
    "mozarella",
    # left out: vegan mozzarella
]

VEGETABLES = [
    "broccolini",
    "peppadew",
    "tomato",
    "kalamata olive",
    "artichoke",
    "arugula",
    "pine nut",
    "mushroom",
    "roasted garlic",
    "caramelized onion",
    "red onion",
    "capers",
    "pesto",
    "corn",
    "jalapeño",
    "spinach",

    "sundried tomato",
    "pineapple",
    "green pepper",
    "red pepper",
    "squash"
]

INGREDIENTS = PROTEINS + CHEESES + VEGETABLES

# http://www.colourlovers.com/palette/176295/Pizza
COLORS = [
    "#6D6D04",
    "#EBE4C4",
    "#F1B42F",
    "#B44418",
    "#D1A674",
]

MONTHS = [
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
]

WEEKDAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]
