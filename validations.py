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
    bank = bank[-24:] + "2521" + bank[-26:-24]

    # Is numeric and have 30 digits?
    if len(bank) != 30 or (not bank.isnumeric()):
        return False

    # modulo
    if int(bank) % 97 == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    assert is_valid_nip("593-21-67-267")
    assert not is_valid_nip("593-21-67-268")  # "Wrong modulo"
    assert not is_valid_nip("593-21-67-26")  # "Too short"
    assert not is_valid_nip("593-21-6xxx7-267")  # "Containing letters"

    assert is_bank_account_valid("77 1240 1268 1111 0010 6850 0503")
    assert is_bank_account_valid("PL77 1240 1268 1111 0010 6850 0503")
    assert not is_bank_account_valid("PL77 1240 1268 1111 0010 6850 0504")  # Wrong modulo
    assert not is_bank_account_valid("77 1240 1268 1111 0010 6850")  # "Too short"
    assert not is_bank_account_valid("77 1240 1268 1111 text 0010 6850 0503")  # "Containing letters (not in prefix)"
