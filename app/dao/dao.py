from typing import TypeVar, Generic
from dataclasses import dataclass

DEFAULT_ID = -1
ORDER_TYPE_DESC = 'DESC'
ORDER_TYPE_ASC = 'ASC'


class QueryOrder:
    could_order: bool
    order_by: str = None
    order_type: str = None

    def __init__(self, order_by: str = None, order_type: str = None):
        self.could_order = True if (order_by is not None and order_by != ''
                                    and order_type is not None and order_type != '' and
                                    (order_type == ORDER_TYPE_DESC or order_type == ORDER_TYPE_ASC)) else False
        if self.could_order:
            self.order_by = order_by
            self.order_type = order_type

    def order(self) -> str:
        return " ORDER BY = '" + self.order_by + "' " + self.order_type + " " if self.could_order else ''


class QueryPage:
    could_page: bool
    page_num: int = None
    page_size: int = None

    def __init__(self, page_num: int = None, page_size: int = None):
        self.could_page = True if (page_num is not None and page_num > 0
                                   and page_size is not None and page_size > 0) else False
        if self.could_page:
            self.page_num = (page_num - 1) * page_size
            self.page_size = page_size

    def page(self):
        return " limit " + str(self.page_num) + ", " + str(self.page_size) + " " if self.could_page else ''


PageDataType = TypeVar('PageDataType')


@dataclass
class PageResult:
    total: int
    list: Generic[PageDataType]


def print_sql(sql: str):
    print('will run sql: ', sql)
