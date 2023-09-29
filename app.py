from flask import Flask, request, jsonify
from sympy import symbols, diff, solve, sympify,denom,log, exp,sin,cos,S , Symbol, solveset, limit
from sympy.calculus.util import continuous_domain, Interval, singularities
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Modify the find_domain function to return float values
#def find_domain(math_expr, x):
#    denomator = denom(math_expr)
#    domain = solve(denom, x)
#    return [float(point.evalf()) for point in domain]  # Change here

###tchum hagdara
def find_domain_other(func):
    x = Symbol("x")
    domain = continuous_domain(func, x, S.Reals)
    return domain

# Modify the find_extreme_points function to return a list of dictionaries
def find_extreme_points(math_expr, x):
    f_prime = diff(math_expr, x)
    critical_points = solve(f_prime, x)
    types = ["Minimum" if (f_prime.subs(x, p-1).evalf() < 0) and (f_prime.subs(x, p+1).evalf() > 0) 
             else "Maximum" if (f_prime.subs(x, p-1).evalf() > 0) and (f_prime.subs(x, p+1).evalf() < 0)
             else None
             for p in critical_points]
    result = [{"point": float(point.evalf()), "type": t} for point, t in zip(critical_points, types)]  # Change here
    return result

# Modify the find_increasing_decreasing_intervals function to return a list of tuples
def find_increasing_decreasing_intervals(math_expr, x):
    f_prime = diff(math_expr, x)  # First derivative
    critical_points = solveset(f_prime, x, domain=S.Reals)  # Find critical points in real number domain
    
    critical_points = sorted([point.evalf() for point in critical_points])  # Sort critical points
    
    # Add negative and positive infinity to the list of critical points to define the intervals
    intervals = [-S.Infinity, *critical_points, S.Infinity]
    
    increasing_intervals = []
    decreasing_intervals = []
    
    for i in range(len(intervals) - 1):
        # Test a point in the interval
        test_point = (intervals[i] + intervals[i+1]) / 2
        if f_prime.subs(x, test_point) > 0:
            increasing_intervals.append((float(intervals[i]), float(intervals[i+1])))
        else:
            decreasing_intervals.append((float(intervals[i]), float(intervals[i+1])))
    
    result = {
        "increasing_intervals": increasing_intervals,
        "decreasing_intervals": decreasing_intervals
    }
    return result

# Modify the find_asymptotes function to return a dictionary with float values
def find_asymptotes(math_expr, x):
    # Find the horizontal asymptote.
    expr = math_expr
    
    horizontal_asymptote = limit(math_expr, x, S.Infinity)
    
    # Find the vertical asymptotes by finding the singularities of the function.

    vertical_asymptotes = singularities(expr, x)
    
    result = {
        "horizontal_asymptote": float(horizontal_asymptote.evalf()),
        "vertical_asymptotes": [float(point.evalf()) for point in vertical_asymptotes]
    }
    return result

# Modify the find_inflection_points function to return a list of float values
def find_inflection_points(math_expr, x):
    f = sympify(math_expr.replace('^', '**').replace('e', 'exp(1)'))
    f_double_prime = diff(f, x, 2)
    inflection_points = solve(f_double_prime, x)
    result = [float(point.evalf()) for point in inflection_points]  # Change here
    return result

# Modify the find_intersections_with_axes function to return a list of dictionaries
def find_intersections_with_axes(math_expr, x):
    f = sympify(math_expr.replace('^', '**').replace('e', 'exp(1)'))
    x_intersections = solve(f, x)
    y_intersections = [float(f.subs(x, 0).evalf())]
    result = [{"x": float(x_val.evalf()), "y": 0} for x_val in x_intersections] + [{"x": 0, "y": y_val} for y_val in y_intersections]  # Change here
    return result

@app.route('/getCriticalPoints', methods=['GET', 'POST'])
def get_critical_points():
    math_function = request.args.get('mathFunction')
    
    # Parse the function and calculate the critical points
    x = symbols('x')
    try:
        # Replace '^' with '**' and parse the expression
        expr1 = sympify(math_function.replace('^', '**').replace('e', 'exp(1)'))
        
        # Calculate the expression
        expr = expr1
        singularities(expr,x)
        
        # First derivative
        f_prime = diff(expr, x)
        
        # Solve for critical points
        critical_points = solve(f_prime, x)
        
        # Format and round the critical points to two decimal places
        formatted_critical_points = [round(point.evalf(),2) for point in critical_points]

        # Aggregate all the results into a JSON response
        result = {
            "critical_points": str(formatted_critical_points),
            #"domain": find_domain_other(expr1),
            #"extreme_points": find_extreme_points(expr1, x),
            #"increasing_decreasing_intervals": find_increasing_decreasing_intervals(math_function, x),
            "asymptotes": find_asymptotes(expr, x),
            #"inflection_points": find_inflection_points(math_function, x),
            #"intersections_with_axes": find_intersections_with_axes(math_function, x)
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=3000)