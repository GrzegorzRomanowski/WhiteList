def cleaning(number: str) -> str:
    punctuation_marks_to_be_removed = [" ", "-", "/", "\\", ".", ",", "(", ")", "[", "]"]
    for mark in punctuation_marks_to_be_removed:
        number = number.replace(mark, "")
    return number


def is_valid_nip(nip: str) -> bool:
    """ Validates NIP checking the number of digits and the last check digit.
    :param nip:-> like a 10 digits string
    :return: True or False
    """
    nip = cleaning(nip)

    # Is numeric and have 10 digits?
    if len(nip) != 10 or (not nip.isnumeric()):
        return False

    # Control list and modulo validation
    control_list = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    sum_value = 0
    for i in range(9):
        sum_value += int(nip[i]) * control_list[i]
    modulo = sum_value % 11
    if modulo == int(nip[9]):
        return True
    else:
        return False


def is_bank_account_valid(bank: str) -> bool:
    bank = cleaning(bank)


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    print("NIP validation:         ", is_valid_nip("593-21-67-267"))
    print("Bank account validation:", is_bank_account_valid("77 1240 1268 1111 0010 6850 0503"))
