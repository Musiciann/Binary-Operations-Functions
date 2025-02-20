from unittest import TestCase
import BinaryOperations
import pytest

class Test(TestCase):
    def test_decimal_to_binary_direct_code(self):
        binary_direct = BinaryOperations.decimal_to_binary_direct_code(2)
        assert binary_direct == "00000010"

    def test_decimal_to_binary_direct_code_zero(self):
        binary_direct = BinaryOperations.decimal_to_binary_direct_code(0)
        assert binary_direct == "00000000"

    def test_decimal_to_binary_direct_code_negative(self):
        binary_direct = BinaryOperations.decimal_to_binary_direct_code(-2)
        assert binary_direct == "10000010"

    def test_decimal_to_binary_inverse_code(self):
        binary_inverse = BinaryOperations.decimal_to_binary_inverse_code(2)
        assert binary_inverse == "00000010"

    def test_decimal_to_binary_additional_code(self):
        binary_additional = BinaryOperations.decimal_to_binary_additional_code(2)
        assert binary_additional == "00000010"

    def test_decimal_to_binary_inverse_code_negative(self):
        binary_inverse = BinaryOperations.decimal_to_binary_inverse_code(-2)
        assert binary_inverse == "11111101"

    def test_decimal_to_binary_additional_code_negative(self):
        binary_additional = BinaryOperations.decimal_to_binary_additional_code(-2)
        assert binary_additional == "11111110"

    def test_additional_code_binary_sum(self):
        binary_additional = BinaryOperations.additional_code_binary_sum(BinaryOperations.decimal_to_binary_additional_code(-2),
                                                                    BinaryOperations.decimal_to_binary_additional_code(2))
        assert binary_additional == "00000000"

    def test_binary_to_decimal_direct_code_negative(self):
        decimal = BinaryOperations.binary_to_decimal_direct_code('10000010')
        assert decimal == -2

    def test_binary_to_decimal_direct_code(self):
        decimal = BinaryOperations.binary_to_decimal_direct_code('00000010')
        assert decimal == 2

    def test_binary_to_decimal_additional_code(self):
        decimal = BinaryOperations.binary_to_decimal_additional_code(BinaryOperations.decimal_to_binary_additional_code(3))
        assert decimal == 3

    def test_binary_to_decimal_additional_code_negative(self):
        decimal = BinaryOperations.binary_to_decimal_additional_code(BinaryOperations.decimal_to_binary_additional_code(-3))
        assert decimal == -3

    def test_binary_multiply(self):
        binary_direct = BinaryOperations.binary_multiply('00001100','00000011')
        decimal = BinaryOperations.binary_to_decimal_direct_code(binary_direct)
        assert decimal == 36

    def test_binary_multiply_negative(self):
        binary_direct = BinaryOperations.binary_multiply('00001100','10000011')
        decimal = BinaryOperations.binary_to_decimal_direct_code(binary_direct)
        assert decimal == -36

    def test_binary_multiply_negatives(self):
        binary_direct = BinaryOperations.binary_multiply('10001100','10000011')
        decimal = BinaryOperations.binary_to_decimal_direct_code(binary_direct)
        assert decimal == 36

    def test_binary_division(self):
        binary_direct = BinaryOperations.binary_division('00001100', '00000011')
        assert binary_direct == '00000100.00000'

    def test_binary_division_zero(self):
        binary_direct = BinaryOperations.binary_division('00001100', '00000000')
        assert binary_direct == 'Zero Division Error'

    def test_binary_division_zero_dividend(self):
        binary_direct = BinaryOperations.binary_division('00000000', '00000010')
        assert binary_direct == '0'

    def test_sum_floats(self):
        float_num = BinaryOperations.sum_floats(2.5, 3.75)
        assert float_num == 6.25

    def test_binary_reminder_to_float(self):
        float_num = BinaryOperations.binary_reminder_to_float('00011')
        assert float_num == 3.0

    def test_binary_subtract(self):
        binary_num = BinaryOperations.binary_subtract('00000101', '00000010')
        assert binary_num == '11'

