'''
Created on Jan 7, 2017

@author: weyu
'''

from collections import namedtuple

from docplex.mp.model import Model
from docplex.util.environment import get_environment

FOODS = [
    ("Roasted Chicken", 0.84, 0, 10),
    ("Spaghetti W/ Sauce", 0.78, 0, 10),
    ("Tomato,Red,Ripe,Raw", 0.27, 0, 10),
    ("Apple,Raw,W/Skin", .24, 0, 10),
    ("Grapes", 0.32, 0, 10),
    ("Chocolate Chip Cookies", 0.03, 0, 10),
    ("Lowfat Milk", 0.23, 0, 10),
    ("Raisin Brn", 0.34, 0, 10),
    ("Hotdog", 0.31, 0, 10)
]

NUTRIENTS = [
    ("Calories", 2000, 2500),
    ("Calcium", 800, 1600),
    ("Iron", 10, 30),
    ("Vit_A", 5000, 50000),
    ("Dietary_Fiber", 25, 100),
    ("Carbohydrates", 0, 300),
    ("Protein", 50, 100)
]

FOOD_NUTRIENTS = [
    ("Roasted Chicken", 277.4, 21.9, 1.8, 77.4, 0, 0, 42.2),
    ("Spaghetti W/ Sauce", 358.2, 80.2, 2.3, 3055.2, 11.6, 58.3, 8.2),
    ("Tomato,Red,Ripe,Raw", 25.8, 6.2, 0.6, 766.3, 1.4, 5.7, 1),
    ("Apple,Raw,W/Skin", 81.4, 9.7, 0.2, 73.1, 3.7, 21, 0.3),
    ("Grapes", 15.1, 3.4, 0.1, 24, 0.2, 4.1, 0.2),
    ("Chocolate Chip Cookies", 78.1, 6.2, 0.4, 101.8, 0, 9.3, 0.9),
    ("Lowfat Milk", 121.2, 296.7, 0.1, 500.2, 0, 11.7, 8.1),
    ("Raisin Brn", 115.1, 12.9, 16.8, 1250.2, 4, 27.9, 4),
    ("Hotdog", 242.1, 23.5, 2.3, 0, 0, 18, 10.4)
]

Food = namedtuple("Food", ["name", "unit_cost", "qmin", "qmax"])
Nutrient = namedtuple("Nutrient", ["name", "qmin", "qmax"])


def build_diet_model(**kwargs):
    # Create tuples with named fields for foods and nutrients

    food = [Food(*f) for f in FOODS]
    nutrients = [Nutrient(*row) for row in NUTRIENTS]

    food_nutrients = {(fn[0], nutrients[n].name):
                      fn[1 + n] for fn in FOOD_NUTRIENTS for n in range(len(NUTRIENTS))}

    # Model
    mdl = Model(name='diet', **kwargs)

    # Decision variables, limited to be >= Food.qmin and <= Food.qmax
    qty = {f: mdl.continuous_var(lb=f.qmin, ub=f.qmax, name=f.name) for f in food}

    # Limit range of nutrients, and mark them as KPIs
    for n in nutrients:
        amount = mdl.sum(qty[f] * food_nutrients[f.name, n.name] for f in food)
        mdl.add_range(n.qmin, amount, n.qmax)
        mdl.add_kpi(amount, publish_name="Total %s" % n.name)

    # Minimize cost
    #mdl.minimize(mdl.sum(qty[f] * f.unit_cost for f in food))
    mdl.maximize(mdl.sum(qty[f] * f.unit_cost for f in food))

    mdl.print_information()
    return mdl


if __name__ == '__main__':
    """DOcplexcloud credentials can be specified with url and api_key in the code block below.

    Alternatively, Context.make_default_context() searches the PYTHONPATH for
    the following files:

        * cplex_config.py
        * cplex_config_<hostname>.py
        * docloud_config.py (must only contain context.solver.docloud configuration)

    These files contain the credentials and other properties. For example,
    something similar to::

       context.solver.docloud.url = "https://docloud.service.com/job_manager/rest/v1"
       context.solver.docloud.key = "example api_key"
    """
    url = None
    key = None

    mdl = build_diet_model()

    # Solve the model. If a key has been specified above, the solve
    # will use IBM Decision Optimization on cloud.
    if not mdl.solve(url=url, key=key):
        print("*** Problem has no solution")
    else:
        mdl.float_precision = 3
        print("* model solved as function:")
        mdl.print_solution()
        mdl.report_kpis()
        # Save the CPLEX solution as "solution.json" program output
        with get_environment().get_output_stream("solution.json") as fp:
            mdl.solution.export(fp, "json")
            
    result = mdl.solution.export_as_string()
    import json
    jsonresult = json.loads(result)