from flask import Flask, request, jsonify
from sympy import symbols, diff, solve, sympify,denom,log, exp,sin,cos,tan,S , Symbol, solveset, limit,lambdify,Interval,pi,EmptySet,nan,Union, simplify,  FiniteSet,  solve_univariate_inequality,latex
import re
from sympy.calculus.util import continuous_domain, Interval, singularities
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import base64
from io import BytesIO
import plotly.graph_objects as go
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
matplotlib.use('Agg')

# Modify the find_domain function to return float values
#def find_domain(math_expr, x):
#    denomator = denom(math_expr)
#    domain = solve(denom, x)
#    return [float(point.evalf()) for point in domain]  # Change here

###tchum hagdara
def find_domain_other(func,domain_interval):
    x = Symbol("x")
    domain = continuous_domain(func, x, domain_interval)
    return str(domain)

# Modify the find_extreme_points function to return a list of dictionaries
def find_extreme_points(math_expr, x,domain_interval):
    f_prime = diff(math_expr, x)
    f_prime = simplify(f_prime)
    if f_prime.is_zero:
        filtered_critical_points = []
    else:
        critical_points = solveset(f_prime, x,domain =  domain_interval)
        if not isinstance(critical_points, FiniteSet):
            filtered_critical_points = []
        else:
            critical_points = [point.evalf() for point in critical_points]
            filtered_critical_points = [number for number in critical_points if number.is_real]

    types = ["Minimum" if (f_prime.subs(x, p-0.01).evalf() < 0) and (f_prime.subs(x, p+0.01).evalf() > 0) 
             else "Maximum" if (f_prime.subs(x, p-0.01).evalf() > 0) and (f_prime.subs(x, p+0.01).evalf() < 0)
             else None
             for p in filtered_critical_points]
    result = {"extreme_points": [{"x": round(float(point.evalf()),2),"y": round(float(math_expr.subs(x, point).evalf()),2) ,"type": t } for point, t in zip(filtered_critical_points, types) if t is not None]}
    return result

# Modify the find_increasing_decreasing_intervals function to return a list of tuples
def find_increasing_decreasing_intervals(math_expr, x,domain_interval):
    f_prime = diff(math_expr, x)  # First derivative
    if f_prime.is_zero:
        filtered_critical_points = []
    else:
        critical_points = solveset(f_prime, x, domain=domain_interval)  # Find critical points in real number domain
        if not isinstance(critical_points, FiniteSet):
            filtered_critical_points = []
        else:
            filtered_critical_points = [number for number in critical_points if number.is_real]
            filtered_critical_points = sorted([point.evalf() for point in critical_points])  # Sort critical points
    singular_points = singularities(math_expr, x, domain=S.Reals)
    if domain_interval == Interval(-2*pi, 2*pi):
        singular_points = singular_points.intersect(domain_interval)
    all_points= set(filtered_critical_points).union(singular_points)
    all_points = sorted(all_points)

    # Calculate the continuous domain of the function
    func_domain = continuous_domain(math_expr, x, domain_interval)
    if isinstance(func_domain, Union):
        # If it's a union of intervals
        intervals_list = list(func_domain.args)
    else:
    # If it's a single interval
        start_domain = func_domain.start
        end_domain = func_domain.end
        intervals_list = [Interval(start_domain, end_domain)]
    
    increasing_intervals = []
    decreasing_intervals = []

    # Adjust the start and end of your intervals list based on the function's domain
    for interval in intervals_list:
        start_domain = interval.start
        end_domain = interval.end
        start_domain = max(start_domain, -S.Infinity)
        end_domain = min(end_domain, S.Infinity)
        # Filter the critical and singular points that fall within the current domain
        filtered_critical_points = [pt for pt in all_points if interval.contains(pt)]
        # Create the intervals list
        interval_filled = [start_domain, *filtered_critical_points, end_domain]

        for i in range(len(interval_filled) - 1):
            # Test a point in the interval
            start, end = interval_filled[i], interval_filled[i + 1]
            # Determine the test point
            if start == -S.Infinity and end != S.Infinity:  # if the left boundary is -oo
                test_point = end - 1
            elif end == S.Infinity and start != -S.Infinity:  # if the right boundary is oo
                test_point = start + 1
            elif start != -S.Infinity and end != S.Infinity:  # if both boundaries are finite
                test_point = (start + end) / 2
            else:  # for the [-oo, oo] interval if it appears, skip or handle specially
                test_point = 0
            func_domain = continuous_domain(math_expr, x,domain_interval)
            f_prime_domain = continuous_domain(f_prime, x,domain_interval)
            if func_domain.contains(test_point) and f_prime_domain.contains(test_point) and f_prime.subs(x, test_point) > 0:
                increasing_intervals.append(
                    "[" + ("-oo" if interval_filled[i] == -S.Infinity else str(round(float(interval_filled[i]),2))) + 
                    ", " + 
                    ("oo" if interval_filled[i+1] == S.Infinity else str(round(float(interval_filled[i+1]),2))) + "]"
                    )
            elif func_domain.contains(test_point) and f_prime_domain.contains(test_point):
                decreasing_intervals.append(
                    "[" + ("-oo" if interval_filled[i] == -S.Infinity else str(round(float(interval_filled[i]),2))) + 
                    ", " + 
                    ("oo" if interval_filled[i+1] == S.Infinity else str(round(float(interval_filled[i+1]),2))) + "]"
                )
        
    result = {
        "increasing_intervals": increasing_intervals,
        "decreasing_intervals": decreasing_intervals
    }
    return result


def find_increasing_decreasing_intervals2(f_expr, x,domain_interval):
    # Compute the first derivative
    f_prime = diff(f_expr, x)

    # Find where the derivative is positive (i.e., the function is increasing)
    increasing_intervals = solve_univariate_inequality(f_prime > 0, x, relational=False, domain=S.Reals)

    # Find where the derivative is negative (i.e., the function is decreasing)
    decreasing_intervals = solve_univariate_inequality(f_prime < 0, x, relational=False, domain=S.Reals)

    result = {
        "increasing_intervals": str(increasing_intervals),
        "decreasing_intervals": str(decreasing_intervals)
    }
    return result
# Modify the find_asymptotes function to return a dictionary with float values
def find_asymptotes(math_expr, x, domain_interval):
    # Find the horizontal asymptote.
    expr = math_expr
    
    if not math_expr.has(sin) and not math_expr.has(cos) and not math_expr.has(tan) :
        horizontal_asymptote = limit(math_expr, x, S.Infinity)
    else: 
        horizontal_asymptote = nan
    
    # Find the vertical asymptotes by finding the singularities of the function.

    vertical_asymptotes = singularities(expr, x,domain=S.Reals)
    #if it's trigonometric
    if domain_interval == Interval(-2*pi, 2*pi):
        vertical_asymptotes = vertical_asymptotes.intersect(domain_interval)
        
    result = {
        "horizontal_asymptote": str(round(float(horizontal_asymptote.evalf()),2)),
        "vertical_asymptotes": [round(float(point.evalf()),2) for point in vertical_asymptotes]
    }
    return result

# Modify the find_inflection_points function to return a list of float values
def find_inflection_points(math_expr, x,domain_interval):
    f_double_prime = diff(math_expr, x, 2)  # Second derivative
    #critical_points = solve(f_double_prime, x, domain=S.Reals)  # Solve for zero
    f_double_prime = simplify(f_double_prime)
    if  f_double_prime.is_zero:
        filtered_critical_points = []
    else:
        critical_points = solveset(f_double_prime, x, domain=domain_interval)
        if not isinstance(critical_points, FiniteSet):
            filtered_critical_points = []
        else:
            critical_points = [point.evalf() for point in critical_points]
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
def find_intersections_with_axes(math_expr, x,domain_interval):
    func_domain = continuous_domain(math_expr, x, domain_interval)
    x_intersections = solveset(math_expr, x, domain=domain_interval)
    if not isinstance(x_intersections, FiniteSet):
        filtered_x_intersections = []
    else:
        x_intersections = [point.evalf() for point in x_intersections]
        filtered_x_intersections  = [number for number in x_intersections  if number.is_real]
    y_intersections = []
    if  func_domain.contains(0):
           y_intersections = [round(float(math_expr.subs(x, 0).evalf()) ,2)]
    result = {"with_x":[{"x": round(float(x_val.evalf()),2), "y": 0.0} for x_val in filtered_x_intersections], 
              "with_y": [{"x": 0.0, "y": y_val} for y_val in y_intersections]}  # Change here
    return result

def graph_representation(expr, domain_interval,extreme_points,inflection_points, intersections_with_axes):
    try:
        x = symbols('x')
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        x_values_from_inflection = []
        y_values_from_inflection = []
        x_values_from_extreme = []
        y_values_from_extreme = []
        x_values_from_intersections = []
        y_values_from_intersections = []
        intervals_list = []

        if isinstance(domain_interval, Union):
        # If it's a union of intervals
            intervals_list = list(domain_interval.args)
            start_domain = intervals_list[0].start
            end_domain = intervals_list[-1].end
        else:
        # If it's a single interval
            start_domain = domain_interval.start
            end_domain = domain_interval.end

        domain_start_numeric = float(start_domain.evalf())
        domain_end_numeric = float(end_domain.evalf())

        # Define a lambda function for the expression
        func = lambdify(x, expr, modules=["numpy"])

        if inflection_points["inflection_points"]:
            x_values_from_inflection = [point['x'] for point in inflection_points["inflection_points"]]
            y_values_from_inflection = [point['y'] for point in inflection_points["inflection_points"]]


        if extreme_points["extreme_points"]: # if the list isn't empty
            x_values_from_extreme = [point['x'] for point in extreme_points["extreme_points"]]
            y_values_from_extreme = [point['y'] for point in extreme_points["extreme_points"]]
        
        if intersections_with_axes["with_x"]: # if the list isn't empty
            x_values_from_intersections = [point['x'] for point in intersections_with_axes["with_x"]]

        if intersections_with_axes["with_y"]: # if the list isn't empty
            y_values_from_intersections = [point['y'] for point in intersections_with_axes["with_y"]]

        
        all_x_values = x_values_from_inflection + x_values_from_extreme + x_values_from_intersections
        all_y_values = y_values_from_inflection + y_values_from_extreme + y_values_from_intersections

        # max_distance_x = all_x_values[0]
        max_distance_x = 0
        for i in range(len(all_x_values) - 1):
            for j in range(i+1, len(all_x_values)):  # Start from i+1 to avoid comparing the point with itself
                distance = abs(all_x_values[j] - all_x_values[i])
                max_distance_x = max(max_distance_x, distance)

        max_distance_y = 0
        for i in range(len(all_y_values) - 1):
            for j in range(i+1, len(all_y_values)):  # Start from i+1 to avoid comparing the point with itself
                distance = abs(all_y_values[j] - all_y_values[i])
                max_distance_y = max(max_distance_y, distance)

        if all_x_values:
            min_x = min(all_x_values) if all_x_values else 0
            max_x = max(all_x_values) if all_x_values else 0
            min_y = min(all_y_values) if all_y_values else 0
            max_y = max(all_y_values) if all_y_values else 0
            x_vals = np.linspace(max(min_x - 0.5*abs(min_x)- 10 - max_distance_x,domain_start_numeric),min( max_x +0.5*abs(max_x)+ 10 + max_distance_x,domain_end_numeric), 20000)
            y_vals = func(x_vals)
        else:
            x_vals = np.linspace(max(-10,domain_start_numeric), min(10,domain_end_numeric), 20000)
            y_vals = func(x_vals)

        singular_points = singularities(expr, x,domain=S.Reals)
        if domain_interval == Interval(-2*pi, 2*pi):
            singular_points = singular_points.intersect(domain_interval)
        epsilon = 0.001
        for singular_point in singular_points:
            if singular_point.is_real:
                mask = (x_vals > float(singular_point) - epsilon) & (x_vals < float(singular_point) + epsilon)
                y_vals[mask] = np.nan

        # Create a plot for the function
        
        fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines'))
        fig.update_yaxes(range=[min_y - 0.5*abs(min_y) - 10 - max_distance_y , max_y + 0.5*abs(max_y) + 10 + max_distance_y])
        
        
        # Convert the figure to an image
        buf = BytesIO()
        fig.write_image(buf, format='png')
        buf.seek(0)

        # Encode the BytesIO object to base64 string
        graph_representation_str = base64.b64encode(buf.getvalue()).decode('utf8')
        return graph_representation_str

    except Exception as e:
        return str(e)
    
@app.route('/getCriticalPoints', methods=['GET', 'POST'])
def get_critical_points():
    math_function = request.args.get('mathFunction')
    
    # Parse the function and calculate the critical points
    x = symbols('x')
    try:
        # Replace '^' with '**' and parse the expression
        # Replace 4x to 4*x
        math_function = re.sub(r'(\d)(x|s|c|t|e)', r'\1*\2', math_function)
        math_function = re.sub(r'(\))(x)', r'\1*\2', math_function)
        math_function = re.sub(r'(x)(\()', r'\1*\2', math_function)
        math_function = re.sub(r'(\))(\()', r'\1*\2',math_function)
        math_function = re.sub(r'(\d)(\()', r'\1*\2',math_function)
        math_function = re.sub(r'(\))(\d|x|s|c|t|e)', r'\1*\2',math_function)
        expr1 = simplify(math_function.replace('^', '**').replace('e', 'exp(1)'))
        expr = expr1
        #expr2 is only for the latex.
        expr2 = sympify(math_function.replace('^', '**').replace('e', 'exp(1)'))
        
        # First derivative
        contains_sine_or_cosine = expr1.has(sin) or expr1.has(cos) or expr1.has(tan)
    
        # If the expression has sine or cosine, adjust the domain
        if contains_sine_or_cosine:
            domain_interval = Interval(-2*pi, 2*pi)
        else:
            domain_interval = continuous_domain(expr, x, S.Reals)  # or whatever default you want

        # these are caclculated first because other functions need these results.
        extreme_points = find_extreme_points(expr1, x, domain_interval)
        inflection_points = find_inflection_points(expr, x,domain_interval)
        intersections_with_axes = find_intersections_with_axes(expr, x,domain_interval)
        # Aggregate all the results into a JSON response
        result = {
            "latex" : latex(expr2),
            "domain": find_domain_other(expr1,domain_interval),
            "extreme_points": extreme_points,
            "increasing_decreasing_intervals": find_increasing_decreasing_intervals(expr, x,domain_interval),
            "asymptotes": find_asymptotes(expr, x,domain_interval),
            "inflection_points": inflection_points,
            "intersections_with_axes": intersections_with_axes,
            "graph_representation": graph_representation(expr, domain_interval, extreme_points, inflection_points, intersections_with_axes)
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=3000)