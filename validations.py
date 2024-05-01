from datetime import datetime


def cleaning(number: str) -> str:
    """ Remove some commonly used punctuation marks from the string being a number.
    :param number: input number like PL: 80-180
    :return: return cleaned number like PL80180
    """
    punctuation_marks_to_be_removed = [" ", "-", "/", "\\", ".", ",", "(", ")", "[", "]", ":"]
    for mark in punctuation_marks_to_be_removed:
        number = number.replace(mark, "")
    return number


def only_digits(number: str) -> str:
    """ Remains only digits from the string being a number.
    :param number: input number like PL: 80-180
    :return: return cleaned number like 80180
    """
    new_number = "".join(char for char in number if char.isdigit())
    return new_number


def format_bank_account(number: str) -> str:
    """ Format bank account number to contain only digits and spaces.
    :param number: uncleaned bank account
    :return: formatted bank account
    """
    new_number = only_digits(number)
    account = new_number[0:2]
    for digit_index in range(2, len(new_number)):
        if digit_index % 4 == 2:
            account += " "
        account += new_number[digit_index]
    return account


def is_valid_bank_account(bank: str) -> bool:
    """ Validates POLISH bank account number checking the number of digits and modulo.
    :param bank: like a 10 digits string
    :return: True or False
    """
    bank = cleaning(bank)
    modified_bank = bank[-24:] + "2521" + bank[-26:-24]  # "2521" is for POLISH bank accounts

    # Is numeric and has 30 digits?
    if len(modified_bank) != 30 or (not modified_bank.isnumeric()):
        return False

    # Modulo
    if int(modified_bank) % 97 == 1:
        return True
    else:
        return False


def is_valid_nip(nip: str) -> bool:
    """ Validates POLISH NIP checking the number of digits and comparing last digit with modulo.
    :param nip: like a 10 digits string
    :return: True or False
    """
    nip = only_digits(nip)

    # Is numeric and has 10 digits?
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


def is_valid_regon(regon: str) -> bool:
    """ Validates POLISH REGON checking the number of digits and modulo.
    :param regon: like a 7 or 9 digits string
    :return: True or False
    """
    regon = only_digits(regon)

    # Is numeric and has 7 or 9 digits?
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


def is_valid_date(date_str: str, date_format="%d-%m-%Y") -> str:
    """ Validates given string can be a date in the correct format and older than today.
    :param date_str: given date as string
    :param date_format: date format like: "%d-%m-%Y"
    :return: unchanged string or empty string
    """
    try:
        date = datetime.strptime(date_str, date_format).date()
        if date < datetime.today().date():
            return date_str
        else:
            return ""
    except ValueError:
        return ""


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    assert is_valid_bank_account("77 1240 1268 1111 0010 6850 0503")
    assert is_valid_bank_account("PL77 1240-1268/1111,0010.6850\\0503")
    assert not is_valid_bank_account("PL77 1240 1268 1111 0010 6850 0504")  # Wrong modulo
    assert not is_valid_bank_account("77 1240 1268 1111 0010 6850")  # "Too short"
    assert not is_valid_bank_account("77 1240 1268 1111 text 0010 6850 0503")  # "Containing letters (not in prefix)"

    assert is_valid_nip("593-21-67-267")
    assert is_valid_nip("593 21/67\\267")
    assert not is_valid_nip("593-21-67-268")  # "Wrong modulo"
    assert not is_valid_nip("593-21-67-26")  # "Too short"

    assert is_valid_regon("191805758")
    assert is_valid_regon("191x805-758")
    assert not is_valid_regon("191805757")  # "Wrong modulo"
    assert not is_valid_regon("19180575")  # "Wrong numbers of digits"

    assert is_valid_date("01-04-2024")
    assert not is_valid_date("01-04-2124")  # Later than today
    assert not is_valid_date("01-13-2024")  # Wrong month
    assert not is_valid_date("2024-04-01")  # Wrong format
