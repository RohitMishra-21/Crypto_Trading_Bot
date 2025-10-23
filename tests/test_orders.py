import unittest
from src.validator import validate_side, validate_order_type

class TestValidatorBasics(unittest.TestCase):
    def test_side(self):
        self.assertEqual(validate_side('buy'),'BUY')
        self.assertEqual(validate_side('SELL'),'SELL')
        with self.assertRaises(ValueError):
            validate_side('HOLD')

    def test_order_type(self):
        self.assertEqual(validate_order_type('market'),'MARKET')
        with self.assertRaises(ValueError):
            validate_order_type('XYZ')

if __name__ == '__main__':
    unittest.main()
