def cleaning(number: str) -> str:
    punctuation_marks_to_be_removed = [" ", "-", "/", "\\", ".", ",", "(", ")", "[", "]"]
    for mark in punctuation_marks_to_be_removed:
        number = number.replace(mark, "")
    return number


def is_valid_nip(nip: str) -> bool:
    """ Validates POLISH NIP checking the number of digits and comparing last digit with modulo.
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
    for i in range(len(nip)-1):
        sum_value += int(nip[i]) * control_list[i]
    modulo = sum_value % 11
    if modulo == int(nip[-1]):
        return True
    else:
        return False


def is_bank_account_valid(bank: str) -> bool:
    """ Validates POLISH bank account number checking the number of digits and modulo.
    :param bank:-> like a 10 digits string
    :return: True or False
    """
    bank = cleaning(bank)
    modified_bank = bank[-24:] + "2521" + bank[-26:-24]

    # Is numeric and have 30 digits?
    if len(modified_bank) != 30 or (not modified_bank.isnumeric()):
        return False

    # modulo
    if int(modified_bank) % 97 == 1:
        return True
    else:
        return False


def is_regon_valid(regon: str) -> bool:
    """ Validates POLISH REGON checking the number of digits and modulo.
    :param regon:-> like a 7 or 9 digits string
    :return: True or False
    """
    regon = cleaning(regon)

    # Is numeric and have 7 or 9 digits?
    if regon.isnumeric() and (len(regon) == 7 or len(regon) == 9):
        pass
    else:
        return False

    # Control list and modulo validation
    sum_value = 0
    control_list = [8, 9, 2, 3, 4, 5, 6, 7]
    for i in range(len(regon) - 1):
        sum_value += int(regon[-(i+2)]) * control_list[-(i+1)]
    modulo = sum_value % 11
    if modulo == int(regon[-1]):
        return True
    else:
        return False


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    assert is_valid_nip("593-21-67-267")
    assert is_valid_nip("593 21/67\\267")
    assert not is_valid_nip("593-21-67-268")  # "Wrong modulo"
    assert not is_valid_nip("593-21-67-26")  # "Too short"
    assert not is_valid_nip("593-21-6xxx7-267")  # "Containing letters"

    assert is_bank_account_valid("77 1240 1268 1111 0010 6850 0503")
    assert is_bank_account_valid("PL77 1240-1268/1111,0010.6850\\0503")
    assert not is_bank_account_valid("PL77 1240 1268 1111 0010 6850 0504")  # Wrong modulo
    assert not is_bank_account_valid("77 1240 1268 1111 0010 6850")  # "Too short"
    assert not is_bank_account_valid("77 1240 1268 1111 text 0010 6850 0503")  # "Containing letters (not in prefix)"

    assert is_regon_valid("191805758")
    assert is_regon_valid("191 805-758")
    assert not is_regon_valid("191805757")  # "Wrong modulo"
    assert not is_regon_valid("19180575")  # "Wrong numbers of digits"
    assert not is_regon_valid("1918057xxx58")  # "Containing letters"
