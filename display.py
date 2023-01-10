# importing packages
import os


def clear_screen():
    """
    clearing text from terminal
    :return: None
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    return


def dict_to_str_table(dic):
    """
    convert dictionary to a long string table
    :param dic: dict
    :return: texttable.Texttable
    """
    pass

