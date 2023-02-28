from flask import Flask, request
from flask_cors import CORS

from app.lib import resp_wrap
from app.service import base_service_instance, device_service_instance
from app.bean import req_bean, resp_bean

app = Flask(__name__)

CORS(app, resources=r'/*')


@app.route("/base/bzt-despot-info", methods=['POST'])
@resp_wrap.rest_resp
def base_bzt_despot_info() -> resp_wrap.RespWrap[str]:
    """
    基础, bze despot 信息
    :return: RespWrap with str
    """
    print('POST /base/bzt-despot-info')
    return base_service_instance.bzt_despot_info()


@app.route("/device/find-device", methods=['POST'])
@resp_wrap.rest_resp
def device_find_device() -> resp_wrap.RespWrap[resp_bean.BaseQueryResp]:
    """
    设备, 获取设备
    :return: RespWrap with List of Device
    """
    req = req_bean.DeviceFindDeviceReq(**request.json)
    print('POST /device/find-device, req:', req)
    return device_service_instance.find_device(req)


@app.route("/device/list-search-param", methods=['POST'])
@resp_wrap.rest_resp
def device_list_search_param() -> resp_wrap.RespWrap[resp_bean.DeviceListSearchParamResp]:
    """
    设备, 获取搜索参数
    :return: RespWrap with DeviceListSearchParamResp
    """
    print('POST /device/list-search-param')
    return device_service_instance.list_search_param()


if __name__ == '__main__':
    app.run(debug=True)
