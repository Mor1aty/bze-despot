import typing
from dataclasses import dataclass
from app.dao import dao, device_dao
from app.bean import req_bean, resp_bean
from app.device import device
from app.lib import resp_wrap


@dataclass
class DeviceService:
    _device_dao: device_dao.DeviceMapper
    _device_manager: device.DeviceManager

    def find_device(self, req: req_bean.DeviceFindDeviceReq) -> resp_wrap.RespWrap[resp_bean.BaseQueryResp]:
        self._device_manager.sync_device()
        result: dao.PageResult = self._device_dao.select_device_with_complex_condition(
            device_dao.DeviceQueryColumn(serial_num=req.serial_num,
                                         brand=req.brand,
                                         model=req.model,
                                         system=req.system,
                                         system_version=req.system_version,
                                         online_state=req.online_state,
                                         ),
            dao.QueryOrder(order_by=req.order_by,
                           order_type=req.order_type,
                           ),
            dao.QueryPage(page_num=req.page_num,
                          page_size=req.page_size,
                          ),
        )
        return resp_wrap.resp_wrap_ok(data=resp_bean.BaseQueryResp(page_num=req.page_num,
                                                                   page_size=req.page_size,
                                                                   total=result.total,
                                                                   list=result.list,
                                                                   ))

    def list_search_param(self) -> resp_wrap.RespWrap[resp_bean.DeviceListSearchParamResp]:
        result: device_dao.DeviceSearchParamResult = self._device_dao.select_device_search_param()
        brand_list: typing.List[str] = []
        for brand in result.brand_list.split(','):
            brand_list.append(brand)
        system_list: typing.List[str] = []
        for system in result.system_list.split(','):
            system_list.append(system)
        return resp_wrap.resp_wrap_ok(data=resp_bean.DeviceListSearchParamResp(
            brand_list=[brand for brand in result.brand_list.split(',')] if result.brand_list is not None else [],
            system_list=[system for system in result.system_list.split(',')] if result.system_list is not None else [],
        ))
