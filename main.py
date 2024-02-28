from matplotlib import pyplot as plt
from math import sin, cos, tan
import numpy as np
import sympy
import json

cot = lambda x: 1 / tan(x)
STEPS = 10000
IMG = r"tmp.jpg"

config = json.loads(open("config.json").read())
#     {
#     "diapason": [-30, 50],
#     "expression": "cos(x)**2 + 3*cos(x) + 1",
#     "method": "solve"
# }


def evaluator(expression):
    def __main__(_x_):
        return eval(expression.replace("x", "_x_"))

    return __main__


def integral(expression, diapason):
    def __main__():
        integral_function = str(sympy.integrate(expression.replace("x", "_x_")))
        _x_ = diapason[1]
        res = eval(integral_function)
        _x_ = diapason[0]
        res -= eval(integral_function)
        return res, integral_function.replace("_x_", "x").replace('**','^')

    return __main__


def differencial(expression):
    def __main__():
        diff_function = str(sympy.diff(expression))
        return diff_function

    return __main__


def arange(diapason):
    return *diapason, (diapason[1] - diapason[0]) / STEPS


def make_integral():
    x = np.arange(*arange(config["diapason"]))
    y = list(map(evaluator(config["expression"]), x))

    integrator = integral(config["expression"], config["diapason"])
    integr, fnc = integrator()

    plt.plot(x, y)
    plt.fill_between(x, y, 0, color="lightblue")
    plt.title(f"Int{' {' + fnc + '}'} = {'%0.4f' % integr}")
    plt.savefig(IMG)
    plt.close()


def make_diff():
    x = np.arange(*arange(config["diapason"]))

    diff = differencial(config["expression"])
    fnc = diff()
    y = list(map(evaluator(fnc), x))

    plt.plot(x, y)
    plt.title(f"Diff{' {' + fnc + '}'}")
    plt.savefig(IMG)
    plt.close()


def make_graph():
    x = np.arange(*arange(config["diapason"]))
    y = list(map(evaluator(config["expression"]), x))

    plt.plot(x, y)
    plt.title(f"Diff{' {' + config['expression'] + '}'}")
    plt.savefig(IMG)
    plt.close()


def make_solve():
    expressions = config["expression"]
    try:
        results = sympy.solve(expressions)
    except:
        results = []

    if len(results) == 0:
        print("No solutions")
    else:
        print("Solutions: ")
        for res in results:
            print("\t" + str(res))


if config["method"] == "solve":
    make_solve()
elif config["method"] == "integral":
    make_integral()
elif config["method"] == "differential":
    make_diff()
elif config["method"] == "graph":
    make_graph()
else:
    print(
        """
        in config.json:
            "method" should be one of {"solve", "integral", "differential", "graph"}
            
            for any except "solve" you should provide "diapason" like [-3, 5]
            
            you should provide "expression" like python-like expression
            
                you can also use:
                    sin(x), cos(x), tan(x), cot(x)
        """
    )
