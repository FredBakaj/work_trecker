import json
from datetime import datetime

import pyodbc

track_id_person_id_collection = dict()


class DataBaseHandler:
    def __init__(self):
        self.last_person_id_file_path: str = "data/meta/last_person_id.txt"
        self.last_person_id: int = None
        self.file_appeared_person_in_camera_path = "temp_storage/appeared_person_in_camera.json"
        self.track_id_person_id_collection_path = "temp_storage/track_id_person_id_collection.json"

        pass

    def get_new_person_id(self) -> int:
        if self.last_person_id is None:
            with open(self.last_person_id_file_path, 'r') as f:
                self.last_person_id = int(f.read())

        self.last_person_id += 1
        with open(self.last_person_id_file_path, 'w') as f:
            f.write(str(self.last_person_id))
        return self.last_person_id

    def get_person_id_by_track_id(self, person_track_id):
        return track_id_person_id_collection[person_track_id]

    def delete_person_id_by_track_id(self, person_track_id):
        del track_id_person_id_collection[person_track_id]

    def create_person_id_by_track_id(self, person_track_id, person_id):
        track_id_person_id_collection[person_track_id] = person_id

    def is_create_track_id(self, track_id):
        return track_id in track_id_person_id_collection.keys()

    def appeared_person_in_camera_create(self, person_id: int, camera_id: int, camera_group_id: int,
                                         appeared_zone_id: int):
        attributes = [
            ('person_id', int.__name__, person_id),
            ('camera_id', int.__name__, camera_id),
            ('camera_group_id', int.__name__, camera_group_id),
            ('appeared_zone_id', int.__name__, appeared_zone_id)
        ]
        # TODO remove print
        print("appeared in camera \n", attributes)
        self._event_log_insert("appeared_in_camera", attributes)


        pass

    def person_crossed_zone_create(self, person_id: int, camera_id: int, camera_group_id: int,
                                   current_zone_id: int, abandoned_zone_id: int):
        attributes =[
            ('person_id', int.__name__, person_id),
            ('camera_id', int.__name__, camera_id),
            ('camera_group_id', int.__name__, camera_group_id),
            ('current_zone_id', int.__name__, current_zone_id),
            ('abandoned_zone_id', int.__name__, abandoned_zone_id)
        ]

        # TODO remove print
        print("crossed_zone \n", attributes)

        self._event_log_insert("crossed_zone", attributes)
        pass

    def person_identification_create(self, person_id: int, camera_id: int, camera_group_id: int, human_id: int):
        attributes = [
            ('person_id', int.__name__, person_id),
            ('camera_id', int.__name__, camera_id),
            ('camera_group_id', int.__name__, camera_group_id),
            ('human_id', int.__name__, human_id)
        ]
        # TODO remove print
        print("person_identification \n", attributes)
        self._event_log_insert("person_identification", attributes)

        pass

    def _get_connection(self):
        connection = pyodbc.connect(
            'Driver={ODBC Driver 18 for SQL Server};'
            'Server=tcp:db-server-work-tracker.database.windows.net,1433;'
            'Database=db-work-tracker;'
            'Uid=work-tracker-user;'
            'Pwd=3ji2d093jmQQ;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'


        )
        return connection

    def _event_log_insert(self, log_type: str, attributes: list[tuple]):
        connection = self._get_connection()
        cursor = connection.cursor()
        # Вставка нового лога
        cursor.execute("INSERT INTO Logs (timestamp, log_type) VALUES (?, ?)", datetime.utcnow(), log_type)
        cursor.execute("SELECT @@IDENTITY AS id")
        log_id = cursor.fetchone()[0]

        for attribute_name, attribute_type, value in attributes:
            cursor.execute("SELECT id FROM Attributes WHERE attribute_name = ?", attribute_name)
            row = cursor.fetchone()
            if row:
                attribute_id = row[0]
            else:
                cursor.execute("INSERT INTO Attributes (attribute_name, attribute_type) VALUES (?, ?)", attribute_name,
                               attribute_type)
                cursor.execute("SELECT @@IDENTITY AS id")
                attribute_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO LogValues (log_id, attribute_id, value) VALUES (?, ?, ?)", log_id, attribute_id,
                           value)
        connection.commit()
        cursor.close()
        connection.close()
