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
            result = binary_add(result, shifted_second_binary)

    result_value = result[-7:].zfill(7)

    return str(sign_value) + result_value

def binary_add(first_binary: str, second_binary: str) -> str:
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


def binary_division(dividend: str, divisor: str) -> str:
    if divisor == "00000000":
        return "Zero Division Error"

    sign_value = '1' if dividend[0] != divisor[0] else '0'

    dividend = dividend[1:]
    divisor = divisor[1:]

    dividend = dividend.lstrip('0')
    divisor = divisor.lstrip('0')

    if not dividend:
        return "0"

    if len(dividend) < len(divisor) or (len(dividend) == len(divisor) and dividend < divisor):
        return "0" + '.' + dividend

    quotient = ''
    remainder = ''

    for bit in dividend:
        remainder += bit

        if remainder >= divisor:
            remainder = binary_subtract(remainder, divisor)
            quotient += '1'
        else:
            quotient += '0'

    dividend = (remainder + "00000")[:6]
    remainder = ''
    remainder_quotient = ''
    if dividend == '000000':
        return sign_value + quotient.zfill(7) + '.' + '00000'
    else:
        for bit in dividend:
            remainder += bit
            if remainder >= divisor:
                remainder = binary_subtract(remainder, divisor)
                remainder_quotient += '1'
            else:
                remainder_quotient += '0'

    remainder_quotient = quotient.lstrip('0') or '0'

    return sign_value + quotient.zfill(7) + '.' + remainder_quotient


def binary_subtract(bin1: str, bin2: str) -> str:
    max_len = max(len(bin1), len(bin2))

    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = []
    borrow = 0

    for i in range(max_len - 1, -1, -1):
        bit1 = int(bin1[i])
        bit2 = int(bin2[i])

        if borrow:
            if bit1 == 0:
                bit1 = 1
                borrow = 1
            else:
                bit1 = 0
                borrow = 0

        if bit1 < bit2:
            bit1 += 2
            borrow = 1

        result_bit = bit1 - bit2
        result.append(str(result_bit))

    return ''.join(result[::-1]).lstrip('0') or '0'

import struct

def float_to_binary(num:float):
    packed = struct.pack('>f', num)
    return ''.join(f'{byte:08b}' for byte in packed)

def binary_to_float(b):
    return struct.unpack('>f', int(b, 2).to_bytes(4, byteorder='big'))[0]

def sum_floats(a:float, b:float) -> float:
    a_bin = float_to_binary(a)
    b_bin = float_to_binary(b)

    sign_a, exponent_a, mantissa_a = a_bin[0], int(a_bin[1:9], 2), a_bin[9:]
    sign_b, exponent_b, mantissa_b = b_bin[0], int(b_bin[1:9], 2), b_bin[9:]

    exponent_a -= 127
    exponent_b -= 127

    if exponent_a > exponent_b:
        exponent_b = exponent_a
        mantissa_b = mantissa_b.lstrip('0')
        mantissa_b = mantissa_b + '0' * (23 - len(mantissa_b))
    elif exponent_a < exponent_b:
        exponent_a = exponent_b
        mantissa_a = mantissa_a.lstrip('0')
        mantissa_a = mantissa_a + '0' * (23 - len(mantissa_a))

    if sign_a == sign_b:
        mantissa_sum = bin(int(mantissa_a, 2) + int(mantissa_b, 2))[2:]
        sign_result = sign_a
    else:
        mantissa_a_int = int(mantissa_a, 2)
        mantissa_b_int = int(mantissa_b, 2)
        if mantissa_a_int >= mantissa_b_int:
            mantissa_sum = bin(mantissa_a_int - mantissa_b_int)[2:]
            sign_result = sign_a
        else:
            mantissa_sum = bin(mantissa_b_int - mantissa_a_int)[2:]
            sign_result = sign_b

    if len(mantissa_sum) > 23:
        mantissa_sum = mantissa_sum[:-1]
        exponent_a += 1

    new_mantissa = mantissa_sum.zfill(23)
    new_exponent = format(exponent_a + 127, '08b')

    result_bin = sign_result + new_exponent + new_mantissa

    return binary_to_float(result_bin)

def binary_reminder_to_float(division_result_binary:str) -> float:

    print(division_result_binary)

    first_bin = division_result_binary[:8]
    second_bin = division_result_binary[10:]

    print(first_bin)
    print(second_bin)

    first_bin = str(binary_to_decimal_direct_code(first_bin))
    second_bin = str(binary_to_decimal_direct_code(second_bin.zfill(8)))

    result_float = first_bin + '.' + second_bin

    print(result_float)

    return float(result_float)






