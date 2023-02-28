from dataclasses import dataclass


@dataclass
class BaseQueryReq:
    page_num: int = None
    page_size: int = None
    order_by: str = None
    order_type: str = None


@dataclass
class DeviceFindDeviceReq(BaseQueryReq):
    serial_num: str = None
    brand: str = None
    model: str = None
    system: str = None
    system_version: float = None
    online_state: int = None
