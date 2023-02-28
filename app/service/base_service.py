from app.lib import resp_wrap
from app.bean import resp_bean


class BaseService:
    _name: str = 'BZT Despot'
    _version: str = '1.0'
    _description: str = 'some interesting info'

    def bzt_despot_info(self) -> resp_wrap.RespWrap[resp_bean.BaseBztDespotInfoResp]:
        return resp_wrap.resp_wrap_ok(
            data=resp_bean.BaseBztDespotInfoResp(name=self._name, version=self._version, description=self._description))
