# importing packages
from user import User, create_user
import display
from date_utils import DateUtil


"""
This object represents a user's own weekly calendar
"""


class MainCalendar:
    def __init__(self, valid_user: User, week_start=None):
        """
        construct object
        :param
        valid_user: User
        week_start: date
        """
        self.user = valid_user
        self.connection = valid_user.connection
        self.cursor = valid_user.connection.cursor()
        self.today = DateUtil.get_today_date()
        self.week_start = week_start if week_start else DateUtil.get_monday_from_today()


if __name__ == '__main__':
    user_login = None
    
    # getting a valid user object with database connection
    while user_login is None:
        try:
            username = input("username:\n")
            password = input("password:\n")
            user_login = create_user(username, password)
        except ValueError as err:
            print("unable to login with given username and password\n"
                  "please double-check your input and server status")
        input("press enter to continue\n")
        display.clear_screen()
    calendar = MainCalendar(user_login)
    print(calendar)
