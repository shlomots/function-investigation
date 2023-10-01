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

    return str(domain)

# Modify the find_extreme_points function to return a list of dictionaries
def find_extreme_points(math_expr, x):
    f_prime = diff(math_expr, x)
    critical_points = [point.evalf() for point in solve(f_prime, x, domain=S.Reals)]
    filtered_critical_points = [number for number in critical_points if number.is_real]
    types = ["Minimum" if (f_prime.subs(x, p-1).evalf() < 0) and (f_prime.subs(x, p+1).evalf() > 0) 
             else "Maximum" if (f_prime.subs(x, p-1).evalf() > 0) and (f_prime.subs(x, p+1).evalf() < 0)
             else None
             for p in filtered_critical_points]
    result = {"extreme_points": [{"x": round(float(point.evalf()),2),"y": round(float(math_expr.subs(x, point).evalf()),2) ,"type": t } for point, t in zip(filtered_critical_points, types)]}
    return result

# Modify the find_increasing_decreasing_intervals function to return a list of tuples
def find_increasing_decreasing_intervals(math_expr, x):
    f_prime = diff(math_expr, x)  # First derivative
    critical_points = solveset(f_prime, x, domain=S.Reals)  # Find critical points in real number domain
    filtered_critical_points = [number for number in critical_points if number.is_real]
    filtered_critical_points = sorted([point.evalf() for point in critical_points])  # Sort critical points
    
    singular_points = singularities(math_expr, x, domain=S.Reals)
    all_points= set(filtered_critical_points).union(singular_points)
    all_points = sorted(all_points)

    # Add negative and positive infinity to the list of critical points to define the intervals
    intervals = [-S.Infinity, *all_points, S.Infinity]
    
    increasing_intervals = []
    decreasing_intervals = []
    
    for i in range(len(intervals) - 1):
        # Test a point in the interval
        start, end = intervals[i], intervals[i + 1]
        # Determine the test point
        if start == -S.Infinity and end != S.Infinity:  # if the left boundary is -oo
            test_point = end - 1
        elif end == S.Infinity and start != -S.Infinity:  # if the right boundary is oo
            test_point = start + 1
        elif start != -S.Infinity and end != S.Infinity:  # if both boundaries are finite
            test_point = (start + end) / 2
        else:  # for the [-oo, oo] interval if it appears, skip or handle specially
            continue
        func_domain = continuous_domain(math_expr, x, S.Reals)
        if func_domain.contains(test_point) and f_prime.subs(x, test_point) > 0:
            increasing_intervals.append(
                "[" + ("-oo" if intervals[i] == -S.Infinity else str(round(float(intervals[i]),2))) + 
                ", " + 
                ("oo" if intervals[i+1] == S.Infinity else str(round(float(intervals[i+1]),2))) + "]"
                )
        elif func_domain.contains(test_point):
            decreasing_intervals.append(
                "[" + ("-oo" if intervals[i] == -S.Infinity else str(round(float(intervals[i]),2))) + 
                ", " + 
                ("oo" if intervals[i+1] == S.Infinity else str(round(float(intervals[i+1]),2))) + "]"
            )
    
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
        "horizontal_asymptote": str(float(horizontal_asymptote.evalf())),
        "vertical_asymptotes": [float(point.evalf()) for point in vertical_asymptotes]
    }
    return result

# Modify the find_inflection_points function to return a list of float values
def find_inflection_points(math_expr, x):
    f_double_prime = diff(math_expr, x, 2)  # Second derivative
    #critical_points = solve(f_double_prime, x, domain=S.Reals)  # Solve for zero
    critical_points = [point.evalf() for point in solve(f_double_prime, x, domain=S.Reals)]
    filtered_critical_points = [number for number in critical_points if number.is_real]
    filtered_critical_points = sorted([point.evalf() for point in filtered_critical_points])  # Sort critical points
    
    inflection_points = []
    func_domain = continuous_domain(math_expr, x, S.Reals)
    for p in filtered_critical_points:
        if not func_domain.contains(p):
            continue  # skip to the next iteration if p is not in the domain
        test_point_left = p - 0.1
        test_point_right = p + 0.1
        
        # Calculate the sign of the second derivative at test points
        sign_left = f_double_prime.subs(x, test_point_left).evalf()
        sign_right = f_double_prime.subs(x, test_point_right).evalf()
        
        if sign_left * sign_right < 0:  # One positive, one negative
            x_value = round(float(p), 2)
            y_value = round(float(math_expr.subs(x, p).evalf()), 2)
            inflection_points.append({"x": x_value, "y":  y_value})
    
    result = {"inflection_points":inflection_points}
    
    return result # Return only the valid inflection points


# Modify the find_intersections_with_axes function to return a list of dictionaries
def find_intersections_with_axes(math_expr, x):
    func_domain = continuous_domain(math_expr, x, S.Reals)
    x_intersections = solve(math_expr, x)
    y_intersections = []
    if  func_domain.contains(0):
           y_intersections = [round(float(math_expr.subs(x, 0).evalf()) ,2)]
    result = {"with_x":[{"x": round(float(x_val.evalf()),2), "y": 0.0} for x_val in x_intersections], 
              "with_y": [{"x": 0.0, "y": y_val} for y_val in y_intersections]}  # Change here
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
        
        # First derivative
        f_prime = diff(expr, x)
        
        # Solve for critical points
        critical_points = solve(f_prime, x)
        
        # Format and round the critical points to two decimal places
        formatted_critical_points = [round(point.evalf(),2) for point in critical_points]

        # Aggregate all the results into a JSON response
        result = {
            #"critical_points": str(formatted_critical_points),
            "domain": find_domain_other(expr1),
            "extreme_points": find_extreme_points(expr1, x),
            "increasing_decreasing_intervals": find_increasing_decreasing_intervals(expr, x),
            "asymptotes": find_asymptotes(expr, x),
            "inflection_points": find_inflection_points(expr, x),
            "intersections_with_axes": find_intersections_with_axes(expr, x)
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=3000)