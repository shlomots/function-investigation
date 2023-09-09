from flask import Flask, request, jsonify
from sympy import symbols, diff, solve, sympify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/getCriticalPoints')
def get_critical_points():
    math_function = request.args.get('mathFunction')
    # print(str(solve('(3*x**2 + 4)/x - (x**3 + 4*x)/x**2')))
    # Parse the function and calculate the critical points
    x = symbols('x')
    expr1 = sympify(math_function.replace('^', '**'))
    expr_string = str(expr1)
    try:
        expr = eval(expr_string)
        # First derivative
        f_prime = diff(expr, x)
        # Solve for critical points
        critical_points = solve(f_prime, x)
        critical_points = [round(point.evalf(),2) for point in critical_points]
        ##print(str(critical_points[0]))
        return jsonify({"result": str(critical_points)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=3000)