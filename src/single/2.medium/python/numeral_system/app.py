def split_equality(equality):
    equality_split = equality.split("=")
    sum = equality_split[0]
    z = equality_split[1]
    x = sum.split("+")[0]
    y = sum.split("+")[1]

    return x, y, z


def convert_number_from_x_base_to_decimal(number, base):
    try:
        res = int(number, base)

        return res
    except Exception:
        return None


def try_all_bases(number1, number2, number3):
    for base in range(2, 37):
        converted_number1 = convert_number_from_x_base_to_decimal(number1, base)
        converted_number2 = convert_number_from_x_base_to_decimal(number2, base)
        converted_number3 = convert_number_from_x_base_to_decimal(number3, base)

        try:
            if converted_number1 + converted_number2 == converted_number3:
                return base
        except Exception:
            pass


def my_main():
    equality = input()

    x, y, z = split_equality(equality)

    base = try_all_bases(x, y, z)

    print(base)


if __name__ == '__main__':
    my_main()
