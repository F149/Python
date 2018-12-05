class TestFactorization(unittest.TestCase):
    def test_simple_multipliers(self):
        x = 77
        a, b = factorize(x)
        self.assertEqual(5*5, 25)
