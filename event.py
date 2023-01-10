from __future__ import annotations
from date_utils import DateUtil
from datetime import date, time
from typing import Optional

"""
represents the table for event ids
singleton class
"""


class IdTable:
    __instance: Optional[IdTable] = None

    # magic methods
    def __init__(self) -> None:
        self.used_id: list[int] = list(self.__get_used_id())

    def __new__(cls) -> IdTable:
        if cls.__instance is None:
            cls.__instance = super(IdTable, cls).__new__(cls)
        return cls.__instance

    # private methods
    def __get_used_id(self) -> set[int]:
        return {3, 4, 5, 7, 8, 10}

    # public methods
    def get_unused_id(self) -> int:
        def diff(lst: list[int]) -> int:
            return lst[-1] - lst[0]

        def find_absence(lst: list[int]) -> int:
            length = len(lst)
            if length == 2:
                return lst[0] + 1
            m = length // 2
            left = lst[:m + 1]
            right = lst[m:]
            if diff(left) > len(left) - 1:
                return find_absence(left)
            else:
                return find_absence(right)

        id_count = len(self.used_id)
        if id_count == diff(self.used_id) + 1:
            return self.used_id[-1] + 1
        else:
            return find_absence(self.used_id)


# creating singleton
_ = IdTable()


class CalendarEvent:
    # magic methods
    def __init__(self) -> None:
        self.__event_type: Optional[str] = None  # one of "due_date" "task" "event" "reminder"
        self.__owner: Optional[str] = None
        self.__event_name: Optional[str] = None
        self.__date: Optional[time] = None
        self.__start_time: Optional[time] = None
        self.__end_time: Optional[time] = None
        self.__event_id: Optional[int] = None
        self.__event_description: Optional[str] = None
        self.__id_table: IdTable = IdTable()

    def __eq__(self, other: CalendarEvent) -> bool:
        return self.get_event_id() == other.get_event_id()

    def __repr__(self):
        return f"type: {type(self)}\nattribute: {self.to_tuple()}"

    # getters
    # no need for type annotation
    def get_event_type(self):
        return self.__event_type

    def get_owner(self):
        return self.__owner

    def get_event_name(self):
        return self.__event_name

    def get_date(self):
        return self.__date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_event_id(self):
        return self.__event_id

    def get_event_description(self):
        return self.__event_description

    # setters
    # all returns self
    def set_owner(self, owner: str):
        """
        username
        """
        self.__owner = owner
        return self

    def set_event_name(self, event_name: str):
        """
        maximum string length 15
        """
        if (l := len(event_name)) <= 30:
            self.__event_name = event_name
            return self
        else:
            raise ValueError(f"event name is too long\nthere are {l} characters which is over 15")

    def set_date(self, event_date: date):
        """
        must be today or future
        """
        if (today := DateUtil.get_today_date()) <= event_date:
            self.__date = event_date
            return self
        else:
            raise ValueError(f"event ended in the past\ntoday is {today.isoformat()}")

    def set_start_time(self, start_time: time):
        """
        any valid time
        """
        self.__start_time = start_time
        return self

    def set_end_time(self, end_time: time):
        """
        must end after start
        """
        if (start := self.get_start_time()) <= end_time:
            self.__end_time = end_time
            return self
        else:
            raise ValueError(f"event must end after its start at {start.isoformat()}")

    def assign_event_id(self):
        """
        auto assigned
        """
        self.__event_id = self.__id_table.get_unused_id()
        return self

    def set_event_description(self, description):
        self.__event_description = description
        return self

    # predicate
    def is_complete(self) -> bool:
        ret = True
        for item in self.to_tuple()[:-1]:
            ret = ret and item is not None
        return ret

    # public methods
    def to_tuple(self) -> \
            tuple[Optional[str], Optional[str], Optional[str], Optional[date],
                  Optional[time], Optional[time], Optional[str], Optional[str]]:
        return self.__owner, self.__event_type, self.__event_name, self.__date, self.__start_time, self.__end_time,\
            self.__event_id, self.__event_description


class RegularEvent(CalendarEvent):
    # override
    def __init__(self):
        super().__init__()
        self.__event_type: str = "event"


class DueDateEvent(CalendarEvent):
    # override
    def __init__(self):
        super().__init__()
        self.__event_type: str = "due_date"

    def set_start_time(self, start_time: time) -> DueDateEvent:
        super().set_start_time(start_time).set_end_time(start_time)
        return self


class TaskEvent(CalendarEvent):
    # override
    def __init__(self):
        super().__init__()
        self.__event_type: str = "task"

    def set_start_time(self, start_time: time) -> TaskEvent:
        super().set_start_time(start_time).set_end_time(start_time)
        return self


class ReminderEvent(CalendarEvent):
    # override
    def __init__(self):
        super().__init__()
        self.__event_type: str = "reminder"


if __name__ == "__main__":
    event_1 = CalendarEvent()\
        .set_event_name("eat")\
        .set_start_time(time(hour=5, minute=10))\
        .set_owner("DDDelta")\
        .set_end_time(time(hour=6, minute=20))\
        .set_date(date(2023, 12, 23))\
        .assign_event_id()
    event_2 = DueDateEvent()
    event_2.set_start_time(time(hour=23, minute=30))
    print(event_1.is_complete())
    print(repr(event_1))
    print(repr(event_2))
