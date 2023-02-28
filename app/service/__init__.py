from app.service import base_service, device_service
from app.dao import device_mapper_instance
from app.device import device_manager_instance

base_service_instance = base_service.BaseService()
device_service_instance = device_service.DeviceService(_device_dao=device_mapper_instance,
                                                       _device_manager=device_manager_instance)
