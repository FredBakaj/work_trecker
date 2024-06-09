import json

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
        data = {
            'person_id': person_id,
            'camera_id': camera_id,
            'camera_group_id': camera_group_id,
            'appeared_zone_id': appeared_zone_id
        }
        # TODO remove print
        print("appeared in camera \n", data)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        pass

    def person_crossed_zone_create(self, person_id: int, camera_id: int, camera_group_id: int,
                                   current_zone_id: int, abandoned_zone_id: int):
        data = {
            'person_id': person_id,
            'camera_id': camera_id,
            'camera_group_id': camera_group_id,
            'current_zone_id': current_zone_id,
            'abandoned_zone_id': abandoned_zone_id,
        }
        # TODO remove print
        print("crossed_zone \n", data)
        pass

    def person_identification_create(self, person_id: int, camera_id: int, camera_group_id: int, human_id: int):
        data = {
            'person_id': person_id,
            'camera_id': camera_id,
            'camera_group_id': camera_group_id,
            'human_id': human_id
        }
        # TODO remove print
        print("person_identification \n", data)
        pass
