import unittest
import app  # assuming your Flask app is named 'app.py'
import json

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
                "x"
                # Add more functions as needed
            ]

            for func in test_functions:
                response = self.app.get(f'/getCriticalPoints?mathFunction={func}')
                data = json.loads(response.data)

                # Basic check: Ensure there's no 'error' in the response
                self.assertNotIn('error', data, f"Failed for function: {func}")

if __name__ == '__main__':
    unittest.main()