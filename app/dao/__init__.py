from app.dao import device_dao

SQLITE_URI = './app/dao/bzt-despot.db'

device_mapper_instance = device_dao.DeviceMapper(SQLITE_URI)
