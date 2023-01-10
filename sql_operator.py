import mysql.connector
from user import create_user, User
from typing import Any, Union, Optional
import datetime

user = create_user("DDDelta", "040806")
test1 = ("DDDelta", "event", "eat", datetime.date(2023, 12, 12), datetime.time(14, 20), datetime.time(14, 30), 1)
test2 = ("DDDelta", "event", "eat", datetime.date(2023, 12, 12), datetime.time(14, 20), datetime.time(14, 30), 2)


class StatementUtil:
    def __init__(self):
        raise TypeError("this is an utility class, call static method directly")

    @staticmethod
    def generate_condition_placeholder(separate: Union[str, tuple[str]], condition: dict[str, Any]):
        if isinstance(separate, str):
            condition_place_holder: str = " WHERE " + f" {separate} ".join([f"{key}=%s" for key in condition])
        elif len(separate) == len(condition) - 1:
            condition_place_holder: str = " WHERE " + " {} ".join([f"{key}=%s" for key in condition])
            condition_place_holder: str = condition_place_holder.format(*separate)
        else:
            raise ValueError(f"keywords: {len(separate)} does not fit between conditions: {len(condition)}")
        return condition_place_holder


class SqlSelector:
    def __init__(self, valid_user: User) -> None:
        self.connection: mysql.connector.connection = valid_user.connection
        self.cursor: mysql.connector.connection.MySQLCursor = valid_user.connection.cursor()

    def select_distinct_from_where(self, table: str,
                                   col_name: Union[str, tuple[str]] = "*",
                                   separate: Union[str, tuple[str]] = "AND",
                                   **condition: Any) -> tuple[tuple[Any], ...]:
        if isinstance(col_name, str):
            str_col_name: str = col_name
        else:
            str_col_name: str = ", ".join(col_name)
        if condition:
            condition_place_holder: str = StatementUtil.generate_condition_placeholder(separate, condition)
        else:
            condition_place_holder: str = ""
        select_statement = (f"SELECT DISTINCT {str_col_name} "
                            f"FROM {table}"
                            f"{condition_place_holder}")
        print(select_statement)
        self.cursor.execute(select_statement, tuple(condition.values()) if condition else None)
        return tuple(x for x in self.cursor)

    def select_from_where(self, table: str,
                          col_name: Union[str, tuple[str]] = "*",
                          separate: Union[str, tuple[str]] = "AND",
                          **condition: Any) -> tuple[tuple[Any], ...]:
        if isinstance(col_name, str):
            str_col_name: str = col_name
        else:
            str_col_name: str = ", ".join(col_name)
        if condition:
            condition_place_holder: str = StatementUtil.generate_condition_placeholder(separate, condition)
        else:
            condition_place_holder: str = ""
        select_statement = (f"SELECT {str_col_name} "
                            f"FROM {table}"
                            f"{condition_place_holder}")
        print(select_statement)
        self.cursor.execute(select_statement, tuple(condition.values()) if condition else None)
        return tuple(x for x in self.cursor)

    def select_with_custom_condition(self, table: str, col_name: str,
                                     condition_placeholder: str, data: Optional[tuple[Any]]) -> tuple[tuple[Any], ...]:
        select_statement = (f"SELECT {col_name}"
                            f"FROM {table}"
                            f"WHERE {condition_placeholder}")
        self.cursor.execute(select_statement, data)
        return tuple(x for x in self.cursor)


class SqlInserter:
    def __init__(self, valid_user: User) -> None:
        self.connection = valid_user.connection
        self.cursor = valid_user.connection.cursor()

    def insert_into_values(self, table: str, col_name: Union[tuple[str, ...], str] = "", values: tuple[Any, ...] = ()) -> None:
        if isinstance(col_name, str):
            str_col_name: str = col_name
        elif (vl := len(values)) != (cl := len(col_name)):
            raise ValueError(f"number of values: {vl} does not match number of columns: {cl}")
        else:
            str_col_name: str = str(col_name).replace("'", "") + " "
        data_placeholder: str = "(" + ", ".join(["%s" for _ in range(len(values))]) + ")"
        insert_statement = (f"INSERT INTO {table} "
                            f"{str_col_name}"
                            f"VALUES {data_placeholder}")
        self.cursor.execute(insert_statement, values)
        self.connection.commit()
        return


inserter = SqlInserter(user)
selector = SqlSelector(user)
print(selector.select_distinct_from_where("v2", "event_id", separate="AND", owner="DDDel", date=datetime.date(2023, 12, 12)))

