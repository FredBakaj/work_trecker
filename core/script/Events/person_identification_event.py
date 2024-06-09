from typing import Any

from core.handler.data_base_handler import DataBaseHandler
from core.utils.vec_math import VecMath


class PersonIdentificationEvent:
    def __init__(self,
                 camera_id: int,
                 camera_group_id: int, ):

        self.camera_id: int = camera_id
        self.camera_group_id: int = camera_group_id
        # хранит в себе ид тех людей, которые уже были записаны
        self.person_records: dict = dict()
        self.db = DataBaseHandler()
        self.vec_math = VecMath()

    def call(self, img_obj_data: dict, img_size: tuple[Any, Any]):
        self._person_identification_trigger(img_obj_data, img_size)
        pass

    def _person_identification_trigger(self, img_obj_data: dict, img_size: tuple[Any, Any]) -> None:
        detect_objects: list[dict] = img_obj_data["detect_objects"]
        if detect_objects is not None:
            # logic of trigger response to new IDs
            for detect_object in detect_objects:
                person: dict = detect_object["person"]
                face: dict = detect_object["face"]
                # person_box = person["box"]
                # person_cls = person["cls"]
                # person_names = person["names"]
                if person is not None and face is not None:
                    person_track_move_points: list = person["track_move_points"]
                    person_track_id = person["track_id"]
                    face_human_id = face["human_id"]
                    person_id = self.db.get_person_id_by_track_id(person_track_id)
                    # проверка на то нету ли track id в колекции или не равен track id значению person id
                    # это значит что появился новый person id у track id и это нужно записать в базу
                    if (len(self.person_records.keys()) == 0
                            or any([key == person_track_id and value != person_id for key, value in
                                    list(self.person_records.items())])
                            or person_track_id not in self.person_records.keys()):
                        self.db.person_identification_create(person_id, self.camera_id, self.camera_group_id,
                                                             face_human_id)
                        self.person_records[person_track_id] = person_id
