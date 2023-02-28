import typing
from dataclasses import dataclass
import sqlite3
from app.dao import dao


@dataclass
class Device:
    id: int
    serial_num: str
    brand: str
    model: str
    internal_model: str
    internal_name: str
    system: str
    system_version: float
    imei1: str
    imei2: str
    online_state: int

    def generate_insert(self) -> str:
        return " (" \
            + "'" + (self.serial_num if self.serial_num is not None else 'NULL') + "'," \
            + "'" + (self.brand if self.brand is not None else 'NULL') + "'," \
            + "'" + (self.model if self.model is not None else 'NULL') + "'," \
            + "'" + (self.internal_model if self.internal_model is not None else 'NULL') + "'," \
            + "'" + (self.internal_name if self.internal_name is not None else 'NULL') + "'," \
            + "'" + (self.system if self.system is not None else 'NULL') + "'," \
            + "'" + (str(self.system_version) if self.system_version is not None else 'NULL') + "'," \
            + "'" + (self.imei1 if self.imei1 is not None else 'NULL') + "'," \
            + "'" + (self.imei2 if self.imei2 is not None else 'NULL') + "'," \
            + "'" + (str(self.online_state) if self.online_state is not None else '2') + "'" \
            + ") "


@dataclass
class DeviceQueryColumn:
    serial_num: str = None
    brand: str = None
    model: str = None
    system: str = None
    system_version: float = None
    online_state: int = None

    def where(self) -> str:
        _SQL = ''
        if self.serial_num is not None and self.serial_num != '':
            _SQL += " AND serial_num LIKE '%" + self.serial_num + "%'"
        if self.brand is not None and self.brand != '':
            _SQL += " AND brand LIKE '%" + self.brand + "%'"
        if self.model is not None and self.model != '':
            _SQL += " AND model LIKE '%" + self.model + "%'"
        if self.system is not None and self.system != '':
            _SQL += " AND system LIKE '%" + self.system + "%'"
        if self.system_version is not None and self.system_version > 0:
            _SQL += " AND system_version = '" + str(self.system_version) + "'"
        if self.online_state is not None and self.online_state > 0:
            _SQL += " AND online_state = '" + str(self.online_state) + "'"
        return _SQL + ' '


@dataclass
class DeviceSearchParamResult:
    brand_list: str
    system_list: str


@dataclass
class DeviceMapper:
    _sqlite_uri: str

    def insert(self, device: Device) -> int:
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = """
                INSERT INTO device
                (
                    serial_num,
                    brand,
                    model,
                    internal_model,
                    internal_name,
                    system,
                    system_version,
                    imei1,
                    imei2,
                    online_state
                )
                VALUES 
            """ + device.generate_insert()
            dao.print_sql(_SQL)
            cursor = conn.cursor()
            cursor.execute(_SQL)
            conn.commit()
            return cursor.lastrowid

    def insert_many(self, device_list: typing.List[Device]):
        if device_list is None or len(device_list) <= 0:
            return
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = """
                INSERT INTO device
                (
                    serial_num,
                    brand,
                    model,
                    internal_model,
                    internal_name,
                    system,
                    system_version,
                    imei1,
                    imei2,
                    online_state
                )
                VALUES 
            """
            for device in device_list:
                _SQL += device.generate_insert() + ','
            _SQL = _SQL[:-1]
            dao.print_sql(_SQL)
            cursor = conn.cursor()
            cursor.execute(_SQL)
            conn.commit()
            return

    def update_by_id(self, device_id: int, device: Device):
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = 'UPDATE device SET'
            _SET_SQL = (" serial_num = '" + device.serial_num + "'," if device.serial_num is not None else '') + \
                       (" brand = '" + device.brand + "'," if device.brand is not None else '') + \
                       (" model = '" + device.model + "'," if device.model is not None else '') + \
                       (" internal_model = '" + device.internal_model + "',"
                        if device.internal_model is not None else '') + \
                       (" internal_name = '" + device.internal_name + "',"
                        if device.internal_name is not None else '') + \
                       (" system = '" + device.system + "',"
                        if device.system is not None else '') + \
                       (" system_version = '" + str(device.system_version) + "',"
                        if device.system_version is not None else '') + \
                       (" imei1 = '" + device.imei1 + "'," if device.imei1 is not None else '') + \
                       (" imei2 = '" + device.imei2 + "'," if device.imei2 is not None else '') + \
                       (" online_state = '" + str(device.online_state) + "',"
                        if device.online_state is not None else '')
            if _SET_SQL == '':
                return
            _SQL += _SET_SQL[:-1] + ' WHERE id = ' + str(device_id)
            dao.print_sql(_SQL)
            conn.cursor().execute(_SQL)
            conn.commit()

    def select_by_serial_num(self, serial_num: str) -> Device:
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = """
                    SELECT
                        id,
                        serial_num,
                        brand,
                        model,
                        internal_model,
                        internal_name,
                        system,
                        system_version,
                        imei1,
                        imei2,
                        online_state 
                    FROM 
                        device
                    WHERE serial_num='""" + serial_num + "' LIMIT 1"
            dao.print_sql(_SQL)
            result = conn.cursor().execute(_SQL).fetchone()
            return Device(
                id=result[0],
                serial_num=result[1],
                brand=result[2],
                model=result[3],
                internal_model=result[4],
                internal_name=result[5],
                system=result[6],
                system_version=result[7],
                imei1=result[8],
                imei2=result[9],
                online_state=result[10]) if result is not None else None

    def select_device_with_complex_condition(self, device_query_column: DeviceQueryColumn = None,
                                             query_order: dao.QueryOrder = None,
                                             query_page: dao.QueryPage = None) -> dao.PageResult:
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = """
                    SELECT
                        id,
                        serial_num,
                        brand,
                        model,
                        internal_model,
                        internal_name,
                        system,
                        system_version,
                        imei1,
                        imei2,
                        online_state 
                    FROM 
                        device
                    WHERE 1 = 1
                """
            _SQL_COUNT = 'SELECT COUNT(*) FROM device WHERE 1 = 1'
            if device_query_column is not None:
                where = device_query_column.where()
                _SQL += where
                _SQL_COUNT += where

            if query_order is not None:
                _SQL += query_order.order()
            if query_page is not None:
                _SQL += query_page.page()
            dao.print_sql(_SQL)
            result = conn.cursor().execute(_SQL).fetchall()
            dao.print_sql(_SQL_COUNT)
            result_count = conn.cursor().execute(_SQL_COUNT).fetchone()

            return dao.PageResult(
                total=result_count[0],
                list=[Device(
                    id=row[0],
                    serial_num=row[1],
                    brand=row[2],
                    model=row[3],
                    internal_model=row[4],
                    internal_name=row[5],
                    system=row[6],
                    system_version=row[7],
                    imei1=row[8],
                    imei2=row[9],
                    online_state=row[10],
                ) for row in result]
            )

    def select_device_search_param(self) -> DeviceSearchParamResult:
        with sqlite3.connect(self._sqlite_uri) as conn:
            _SQL = """
                SELECT
                    (SELECT GROUP_CONCAT(DISTINCT(brand)) FROM device) AS brand_list,
                    (SELECT GROUP_CONCAT(DISTINCT(`system`)) FROM device) AS system_list"""
            dao.print_sql(_SQL)
            result = conn.cursor().execute(_SQL).fetchone()
            return DeviceSearchParamResult(
                brand_list=result[0],
                system_list=result[1]
            )
