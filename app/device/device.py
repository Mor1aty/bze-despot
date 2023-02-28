import adbutils
from adbutils import AdbClient
from app.dao import device_mapper_instance, dao, device_dao


class DeviceManager:
    _adb: AdbClient = None
    _DEVICE_STATE_ONLINE: int = 1
    _DEVICE_STATE_NOT_ONLINE: int = 2

    def __init__(self):
        self._adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self.sync_device()

    def sync_device(self):
        insert_list = []
        for device in self._adb.device_list():
            serial_num = device.serial
            device = device_dao.Device(
                id=dao.DEFAULT_ID,
                serial_num=serial_num,
                brand=device.prop.get('ro.product.brand'),
                model=device.prop.get('persist.sys.device_name'),
                internal_model=device.prop.model,
                internal_name=device.prop.name,
                system='Android',
                system_version=int(device.prop.get('ro.bootimage.build.version.release')),
                imei1=device.prop.get('ro.ril.oem.imei1'),
                imei2=device.prop.get('ro.ril.oem.imei2'),
                online_state=self._DEVICE_STATE_ONLINE,
            )
            existed_device: device_dao.Device = device_mapper_instance.select_by_serial_num(device.serial_num)
            if existed_device is not None:
                device_mapper_instance.update_by_id(existed_device.id, device)
            else:
                insert_list.append(device)
        if insert_list:
            device_mapper_instance.insert_many(insert_list)
