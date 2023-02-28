import typing
from typing import TypeVar, Generic
from dataclasses import dataclass

BaseQueryRespListDataType = TypeVar('BaseQueryRespListDataType')


@dataclass
class BaseQueryResp:
    page_num: int
    page_size: int
    total: int
    list: Generic[BaseQueryRespListDataType]


@dataclass
class BaseBztDespotInfoResp:
    name: str
    version: str
    description: str


@dataclass
class DeviceListSearchParamResp:
    brand_list: typing.List[str]
    system_list: typing.List[str]
