from math import remainder
import struct


def decimal_to_binary_direct_code(decimal_num: int) -> str:

    if decimal_num == 0:
        return "00000000"

    binary_num = ""

    is_negative = decimal_num < 0
    decimal_num = abs(decimal_num)

    while decimal_num > 0:
        modulo = decimal_num % 2
        binary_num = str(modulo) + binary_num
        decimal_num //= 2

    binary_num = binary_num.zfill(7)

    return ("1" if is_negative else "0") + binary_num


def decimal_to_binary_inverse_code(decimal_num: int) -> str:
    binary_inverse = decimal_to_binary_direct_code(decimal_num)

    if decimal_num >= 0:
        return binary_inverse

    binary_inverse = list(binary_inverse)
    for i in range(1, len(binary_inverse)):
        if binary_inverse[i] == '0':
            binary_inverse[i] = '1'
        else:
            binary_inverse[i] = '0'

    return "".join(binary_inverse)


def decimal_to_binary_additional_code(decimal_num: int) -> str:
    if decimal_num >= 0:
        binary_additional = decimal_to_binary_direct_code(decimal_num)
        return binary_additional
    else:
        binary_additional = decimal_to_binary_inverse_code(decimal_num)
        binary_additional = additional_code_binary_sum(binary_additional, '00000001')
        return binary_additional


def additional_code_binary_sum(first_binary: str, second_binary: str) -> str:
    carry_num = 0
    result_binary = ""
    for i in range(7, -1, -1):
        total = carry_num + (1 if list(first_binary)[i] == '1' else 0) + (1 if list(second_binary)[i] == '1' else 0)
        result_binary = str(total % 2) + result_binary
        carry_num = total // 2

    if carry_num:
        result_binary = '1' + result_binary

    if len(result_binary) > 8:
        result_binary = result_binary[1:]

    return result_binary

def binary_to_decimal_direct_code(binary_num: str) -> int:
    decimal_num = 0
    sign = binary_num[0]

    for i, digit in enumerate(reversed(binary_num[1:])):
        decimal_num += int(digit) * (2 ** i)

    if sign == '1':
        decimal_num *= -1

    return decimal_num

def binary_to_decimal_fract(binary_num: str) -> int:
    decimal_fract = 0

    for i, digit in enumerate(binary_num[0:]):
        decimal_fract += float(float(digit) * (2 ** (-1 * (i + 1 ))))

    return decimal_fract

def binary_to_decimal_additional_code(additional_binary_num: str) -> int:

    sign = additional_binary_num[0]

    if sign == '0':
        return binary_to_decimal_direct_code(additional_binary_num)
    else:
        additional_binary_num = list(additional_binary_num)
        for i in range(1, len(additional_binary_num)):
            if additional_binary_num[i] == '0':
                additional_binary_num[i] = '1'
            else:
                additional_binary_num[i] = '0'
        additional_binary_num = "".join(additional_binary_num)

        if sign == '1':
            additional_binary_num = additional_code_binary_sum(additional_binary_num, '00000001')

        decimal_num = binary_to_decimal_direct_code(additional_binary_num)

    return decimal_num

def binary_multiply(first_binary: str, second_binary: str) -> str:

    sign_value = '1' if first_binary[0] != second_binary[0] else '0'

    first_binary = str(int(first_binary[1:]))
    second_binary = str(int(second_binary[1:]))

    result = '0' * (len(first_binary) + len(second_binary))

    first_binary = first_binary[::-1]
    second_binary = second_binary[::-1]

    for i in range(len(first_binary)):
        if first_binary[i] == '1':
            shifted_second_binary = second_binary + '0' * i
            result = binary_add_shifted(result, shifted_second_binary)

    result_value = result[-7:].zfill(7)

    return str(sign_value) + result_value

def binary_add_shifted(first_binary: str, second_binary: str) -> str:
    max_len = max(len(first_binary), len(second_binary))
    first_binary = first_binary.zfill(max_len)
    second_binary = second_binary.zfill(max_len)

    carry_num = 0
    result_binary = []

    for i in range(max_len - 1, -1, -1):
        total = carry_num + int(first_binary[i]) + int(second_binary[i])
        result_binary.append(str(total % 2))
        carry_num = total // 2

    if carry_num:
        result_binary.append('1')

    return ''.join(result_binary[::-1])

def binary_remainder_divide(remainder: str, divisor:str) -> str:
    divisor_length = len(divisor)
    remainder_dividend = remainder.lstrip('0') + '000000'
    remainder_quotient = ''
    remainder = remainder.lstrip('0')
    if remainder_dividend == '0000000':
        return '00000'
    else:
        for bit in remainder_dividend[len(remainder) + 1:]:
            remainder += bit
            if len(remainder) >= divisor_length and int(remainder) >= int(divisor):
                remainder = binary_subtract(remainder, divisor)
                remainder_quotient += "1"
            else:
                remainder_quotient += "0"
    return remainder_quotient

def binary_integer_divide(dividend: str, divisor: str) -> tuple:

    quotient = remainder = ""
    dividend = dividend.lstrip('0')
    divisor_length = len(divisor)

    for bit in dividend:
        remainder += bit
        if len(remainder) >= divisor_length and remainder >= divisor:
            remainder = binary_subtract(remainder, divisor)
            remainder = remainder.lstrip('0')
            quotient += "1"
        else:
            remainder = remainder.lstrip('0')
            quotient += "0"
    return quotient, remainder

def binary_divide(dividend: str, divisor: str) -> str:

    sign_value = '0' if divisor[0] == dividend[0] else '1'

    dividend = dividend[1:]
    divisor = divisor[1:]

    if divisor == "0":
        raise ValueError("Zero Division Error")

    dividend = dividend.lstrip('0')
    divisor_length = len(divisor)

    if divisor_length == 0 or dividend == "":
        return "0"

    integer_quotient, remainder = binary_integer_divide(dividend, divisor)
    remainder_quotient = binary_remainder_divide(remainder, divisor)

    integer_quotient = integer_quotient.lstrip('0') or "0"
    return sign_value + integer_quotient + '.' + remainder_quotient

def binary_to_decimal_division(binary_value: str) -> float:
    sign_value = 1 if binary_value[0] == '0' else -1
    binary_value = binary_value[1:]
    integer_binary, fract_binary = binary_value.split('.')
    integer_decimal = binary_to_decimal_direct_code(integer_binary.zfill(8))
    fract_decimal = binary_to_decimal_fract(fract_binary)
    return sign_value * (integer_decimal + fract_decimal)

def binary_subtract(minuend: str, subtrahend: str) -> str:
    max_length = max(len(minuend), len(subtrahend))
    minuend = minuend.zfill(max_length)
    subtrahend = subtrahend.zfill(max_length)
    result = []
    borrow = 0
    for m, s in zip(reversed(minuend), reversed(subtrahend)):
        m_bit = int(m)
        s_bit = int(s)
        m_bit -= borrow
        if m_bit < s_bit:
            m_bit += 2
            borrow = 1
        else:
            borrow = 0
        result_bit = m_bit - s_bit
        result.append(str(result_bit))
    while len(result) > 1 and result[-1] == '0':
        result.pop()
    return ''.join(reversed(result))

def float_to_binary(value):
    int_representation = struct.unpack('!I', struct.pack('!f', value))[0]

    binary_representation = format(int_representation, '032b')
    return binary_representation


def add_floats(x, y):
    if x < 0 or y < 0:
        raise ValueError("Error Sign Value.")

    x_binary = float_to_binary(x)
    y_binary = float_to_binary(y)

    x_sign = int(x_binary[0], 2)
    x_exponent = int(x_binary[1:9], 2)
    x_mantissa = int(x_binary[9:], 2)

    y_sign = int(y_binary[0], 2)
    y_exponent = int(y_binary[1:9], 2)
    y_mantissa = int(y_binary[9:], 2)

    x_mantissa |= (1 << 23)
    y_mantissa |= (1 << 23)

    if x_exponent > y_exponent:
        y_mantissa >>= (x_exponent - y_exponent)
        exponent = x_exponent
    else:
        x_mantissa >>= (y_exponent - x_exponent)
        exponent = y_exponent

    result_mantissa = x_mantissa + y_mantissa

    if result_mantissa & (1 << 24):
        result_mantissa >>= 1
        exponent += 1

    result_mantissa &= ~(1 << 23)

    if exponent >= 255:
        raise OverflowError("Exponent Overflow.")

    result_binary = f"{0:01b}{format(exponent, '08b')}{format(result_mantissa, '023b')}"
    result_float = struct.unpack('!f', struct.pack('!I', int(result_binary, 2)))[0]

    return result_float, result_binary




