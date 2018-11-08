import sys


def printd(message):
    print(message, file=sys.stderr)


def format_numerals(maya_digit_width, maya_digit_height, lines):
    def cut_line(line, maya_digit_width):
        res = []
        for i in range(0, 20 * maya_digit_width, maya_digit_width):
            res.append(line[slice(i, i + maya_digit_width, 1)])
        return res

    double_list_numerals = []
    for line in lines:
        double_list_numerals.append(cut_line(line, maya_digit_width))

    formatted_numerals = {}
    for y in range(0, maya_digit_height):
        for x in range(0, 20):
            formatted_numerals[x] = "{}{}".format(formatted_numerals.get(x, ""), double_list_numerals[y][x])

    return formatted_numerals


def get_digits_from_maya_number(width, height, number):
    """
    From "o...____........ooo............." to ["ooo.............", "o...____........"]

    :param width:
    :type width: integer
    :param height:
    :type height: integer
    :param number:
    :type number: string
    :return: the list of the maya number digits
    :rtype: list[string]
    """
    res = []
    step = width * height
    for i in range(0, len(number), step):
        res.append(number[slice(i, i + step, 1)])
    return res[::-1]


def calculate_decimal_operation(numerals, digits_maya_number_1, digits_maya_number_2, operation):
    """

    :param numerals:
    :type numerals: dict
    :param digits_maya_number_1:
    :type digits_maya_number_1: list[string]
    :param digits_maya_number_2:
    :type digits_maya_number_2: list[string]
    :param operation:
    :type operation:
    :return:
    :rtype: integer
    """
    nb1_decimal = convert_base_20_to_decimal(maya_to_base_20(numerals, digits_maya_number_1))
    nb2_decimal = convert_base_20_to_decimal(maya_to_base_20(numerals, digits_maya_number_2))

    return eval("{}{}{}".format(nb1_decimal, operation, nb2_decimal))


def convert_decimal_to_base20(decimal_number):
    """

    :param decimal_number: the decimal number to convert
    :type decimal_number: integer
    :return: a list container the digit of the converted number into the base 20
    :rtype: list[integer]
    """
    quotient = 10
    number = decimal_number
    base_x_number = []

    while quotient != 0:
        remainder = number % 20
        quotient = number // 20
        number = quotient
        base_x_number.append(remainder)
    return base_x_number


def base_20_number_to_maya(numerals, base_20_number):
    """

    :param numerals:
    :type numerals: dict
    :param base_20_number:
    :type base_20_number: list[integer]
    :return:
    :rtype: list[string]
    """
    res = []
    for number in base_20_number[::-1]:
        res.append(numerals[number])

    return res


def maya_to_base_20(numerals, maya_number):
    """

    :param numerals:
    :type numerals: dict
    :param maya_number:
    :type maya_number: list[string]
    :return:
    :rtype: list[integer]
    """

    res = []
    for item in maya_number:
        for key, value in numerals.items():
            if value == item:
                res.append(key)
    return res


def convert_base_20_to_decimal(number):
    """

    :param number:
    :type number: list[integer]
    :return:
    :rtype: integer
    """
    res = 0

    for index, value in enumerate(number):
        res = res + value * (20 ** index)

    return res


def format_result(numerals, width, decimal_number):
    base_20_number = convert_decimal_to_base20(decimal_number)
    base_20_maya = base_20_number_to_maya(numerals, base_20_number)

    all_res = []
    for item in base_20_maya:
        res = []
        for i in range(0, len(item), width):
            res.append(item[slice(i, i + width, 1)])
        all_res.append("\n".join(res))
    return "\n".join(all_res)


def my_main():
    maya_digit_width, maya_digit_height = [int(i) for i in input().split()]

    raw_numerals = []
    for i in range(maya_digit_height):
        line = input()
        raw_numerals.append(line)

    numerals = format_numerals(maya_digit_width, maya_digit_height, raw_numerals)

    string_maya_number_1 = ""
    s1 = int(input())
    for i in range(s1):
        num_1line = input()
        string_maya_number_1 = string_maya_number_1 + num_1line
    digits_maya_number_1 = get_digits_from_maya_number(maya_digit_width, maya_digit_height, string_maya_number_1)

    string_maya_number_2 = ""
    s2 = int(input())
    for i in range(s2):
        num_2line = input()
        string_maya_number_2 = string_maya_number_2 + num_2line

    digits_maya_number_2 = get_digits_from_maya_number(maya_digit_width, maya_digit_height, string_maya_number_2)

    operation = input()

    decimal_result = calculate_decimal_operation(numerals, digits_maya_number_1, digits_maya_number_2, operation)
    result = format_result(numerals, maya_digit_width, decimal_result)

    print(result)


if __name__ == '__main__':
    my_main()
