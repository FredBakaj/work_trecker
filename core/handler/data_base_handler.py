import json


class DataBaseHandler:
    def __init__(self):
        self.last_person_id_file_path: str = "data/meta/last_person_id.txt"
        self.last_person_id: int = None
        self.file_appeared_person_in_camera_path = "temp_storage/appeared_person_in_camera.json"
        pass

    def get_new_person_id(self) -> int:
        if self.last_person_id is None:
            with open(self.last_person_id_file_path, 'r') as f:
                self.last_person_id = int(f.read())

        self.last_person_id += 1
        with open(self.last_person_id_file_path, 'w') as f:
            f.write(str(self.last_person_id))
        return self.last_person_id

    def appeared_person_in_camera_create(self, person_id: int, camera_id: int, camera_group_id: int,
                                         appeared_zone_id: int):
        data = {
            'person_id': person_id,
            'camera_id': camera_id,
            'camera_group_id': camera_group_id,
            'appeared_zone_id': appeared_zone_id
        }
        #TODO remove
        print(data)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        pass

