# importing packages
import mysql.connector
import logging

logging.basicConfig(filename='info.log', format='%(name)s - %(levelname)s - %(message)s', filemode="w")


# function used to get user object
def create_user(username, password):
    """
    attempt to get n user object with given arguments
    :param username: str
    :param password: str
    :return: User
    raise ValueError when fails to create connection
    """
    user = None
    counter = 5
    while user is None and counter != 0:
        try:
            user = User(username, password)
        except mysql.connector.Error as err:
            logging.warning("connection failed {} time(s)\n"
                            "caught exception from mysql server: \n "
                            "{}".format(str(6-counter), err))
        finally:
            counter -= 1
    if user is not None:
        return user
    else:
        logging.error("unable to get user object")
        raise ValueError("unable to connect to mysql server with given")


"""
This object represents a user
"""


class User:
    def __init__(self, username, password):
        """
        construct object
        :param username: str
        :param password: str
        """
        self.username = username
        self.password = password
        self.connection = mysql.connector.connect(host="localhost",
                                                  username=username,
                                                  password=password,
                                                  database="calendar")
