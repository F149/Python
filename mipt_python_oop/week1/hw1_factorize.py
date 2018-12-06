"""
Дана функция factorize(x) со следующим контрактом:
Написать комплект тестов:

test_wrong_types_raise_exception
test_negative
test_zero_and_one_cases
test_simple_numbers
test_two_simple_multipliers
test_many_multipliers
Проверить в них соответственно:

Что типы float и str (значения 'string', 1.5) вызывают исключение TypeError.
Что для отрицательных чисел -1, -10 и -100 вызывается исключение ValueError.
Что для числа 0 возвращается кортеж (0,), а для числа 1 кортеж (1,)
Что для простых чисел 3, 13, 29 возвращается кортеж, содержащий одно данное число.
Что для чисел 6, 26, 121 возвращаются соответственно кортежи (2, 3), (2, 13) и (11, 11).
Что для чисел 1001 и 9699690 возвращаются соответственно кортежи (7, 11, 13) и (2, 3, 5, 7, 11, 13, 17, 19).
При этом несколько различных проверок в рамках одного теста должны быть обработаны как подслучаи с указанием x: subTest(x=...).
"""
import unittest

def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        for x in 1.5, 'string':
            with self.subTest(x=x):
                with self.assertRaises(TypeError):
                    factorize(x)

    def test_negative(self):
        for x in -1, -10, -100:
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    factorize(x)

    def test_zero_and_one_cases(self):
        for x in 0, 1:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_simple_numbers(self):
        for x in 3, 13, 29:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        with self.subTest(x=6):
            self.assertEqual(factorize(6), (2, 3))
        with self.subTest(x=26):
            self.assertEqual(factorize(26), (2, 13))
        with self.subTest(x=121):
            self.assertEqual(factorize(121), (11, 11))

    def test_many_multipliers(self):
        with self.subTest(x=1001):
            self.assertEqual(factorize(1001), (7, 11, 13))
        with self.subTest(x=9699690):
            self.assertEqual(factorize(9699690), (2, 3, 5, 7, 11, 13, 17, 19))

if __name__ == "__main__":
    unittest.main()
