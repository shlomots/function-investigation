import unittest
import app  # assuming your Flask app is named 'app.py'
import json
from urllib.parse import quote  # import the quote function

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_endpoint(self):
        test_functions = [
            "x^2",
            "2^x",
            "e^x",
            "sqrt(x-3)",
            "cos(x)",
            "(sin(x))^2",
            "x",
            "sin(x)/cos(x)",
            "tan(x)",
            "sqrt(x^2)",
            "ln(1+e^-x)+(1/3)x",
            #"sqrt(x^2+x-2)/(2x-6)",
             "-2x*e^(-x^2/3)",
             "(1-ln(x))/ln(x)",
             "sin(x)*(cos(x))^3",
             "x+sqrt(x^2-4)"
            # Add more functions as needed
        ]

        for func in test_functions:
            encoded_func = quote(func)  # URL-encode the function
            response = self.app.get(f'/getCriticalPoints?mathFunction={encoded_func}')
            data = json.loads(response.data)

            # Basic check: Ensure there's no 'error' in the response
            self.assertNotIn('error', data, f"Failed for function: {func}")

if __name__ == '__main__':
    unittest.main()