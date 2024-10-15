import unittest
from main import (
    evaluate_postfix,
    parse_array,
    parse_config,
)

class TestConfigParser(unittest.TestCase):

    # -== Тесты для функции evaluate_postfix ==-

    def test_evaluate_postfix_basic(self):
        constants = {"x": 5, "y": 10}
        expression = "x y +"
        result = evaluate_postfix(expression, constants)
        self.assertEqual(result, 15)

    def test_evaluate_postfix_with_constants(self):
        constants = {"a": 3, "b": 2}
        expression = "a b -"
        result = evaluate_postfix(expression, constants)
        self.assertEqual(result, 1)

    def test_evaluate_postfix_sqrt(self):
        constants = {"x": 16}
        expression = "x sqrt"
        result = evaluate_postfix(expression, constants)
        self.assertEqual(result, 4.0)

    def test_evaluate_postfix_invalid_expression(self):
        constants = {"x": 5}
        expression = "x z +"
        result = evaluate_postfix(expression, constants)
        self.assertIsNone(result)

    # -== Тесты для функции parse_array ==-

    def test_parse_array_valid(self):
        result = parse_array(0, "[1 2 3]")
        expected_output = "\n  - 1\n  - 2\n  - 3\n"
        self.assertEqual(result, expected_output)

    def test_parse_array_empty(self):
        result = parse_array(1, "[]")
        self.assertEqual(result, "\n")

    def test_parse_array_invalid_format(self):
        result = parse_array(1, "1 2 3")
        self.assertIsNone(result)

    def test_parse_array_invalid_nested(self):
        result = parse_array(1, "[1 2 3")
        self.assertIsNone(result)

    # -== Тесты для функции parse_config ==-

    def test_parse_config_with_constants(self):
        file_content = """
        x: 10
        y: 20
        z: ^(x y +)
        """
        expected_output = "x: 10\ny: 20\nz: 30.0\n"
        result = parse_config(file_content)
        self.assertEqual(result, expected_output)

    def test_parse_config_with_array(self):
        file_content = """
        arr: [1 2 3]
        """
        expected_output = "arr:\n  - 1\n  - 2\n  - 3\n"
        result = parse_config(file_content)
        self.assertEqual(result, expected_output)

    def test_parse_config_with_dict(self):
        file_content = """
        test: {
            x = 1
            y = 2
        }
        """
        expected_output = "test:\n  x: 1\n  y: 2\n"
        result = parse_config(file_content)
        self.assertEqual(result, expected_output)

    def test_parse_config_invalid_expression(self):
        file_content = """
        x: 10
        y: 20
        ^(x z +)
        """
        with self.assertRaises(ValueError):
            parse_config(file_content)

    def test_parse_config_invalid_array(self):
        file_content = """
        arr = [1 2
        """
        with self.assertRaises(ValueError):
            parse_config(file_content)


if __name__ == '__main__':
    unittest.main()