from typing import Any

from core.handler.data_base_handler import DataBaseHandler
from core.utils.vec_math import VecMath


class AppearedPersonInCameraEvent:
    def __init__(self, camera_id: int,
                 camera_group_id: int,
                 zone_line_normal_vec: tuple,
                 left_zone_id: int,
                 right_zone_id: int):

        self.max_count_person_key = 3
        self.right_zone_id = right_zone_id
        self.left_zone_id = left_zone_id
        self.zone_line_normal_vec = zone_line_normal_vec

        self.camera_id: int = camera_id
        self.camera_group_id: int = camera_group_id

        self.triggered_appeared_person_collection: dict = dict()
        self.generations_of_appearances: list = list()
        self.db = DataBaseHandler()
        self.vec_math = VecMath()

    def call(self, img_obj_data: dict, img_size: tuple[Any, Any]):
        self._appeared_person_in_camera_trigger(img_obj_data, img_size)
        pass

    def _appeared_person_in_camera_trigger(self, img_obj_data: dict, img_size: tuple[Any, Any]) -> None:
        detect_objects: list[dict] = img_obj_data["detect_objects"]
        zone_line_vec = self.vec_math.calculate_zone_line_vec(img_size, self.zone_line_normal_vec)

        self._clear_triggered_appeared_person_collection(detect_objects)

        if detect_objects is not None:
            # logic of trigger response to new IDs
            for detect_object in detect_objects:
                person: dict = detect_object["person"]
                person_box = person["box"]
                person_cls = person["cls"]
                person_names = person["names"]
                person_track_move_points: list = person["track_move_points"]
                person_track_id = person["track_id"]

                if person_track_id not in self.triggered_appeared_person_collection.keys() \
                        and len(person_track_move_points) > 0:

                    person_id: int = self.db.get_new_person_id()
                    self.triggered_appeared_person_collection[person_track_id] = person_id
                    person_point = tuple(person_track_move_points[-1][0])

                    side_relative_to_vector = self.vec_math.point_relative_to_vector(
                        (zone_line_vec[0], zone_line_vec[1]),
                        (zone_line_vec[2], zone_line_vec[3]),
                        person_point
                    )
                    # zone id, based on the position of the point relative to the vector
                    appeared_zone_id: int = None
                    if side_relative_to_vector > 0:
                        appeared_zone_id = self.left_zone_id
                    elif side_relative_to_vector < 0 or side_relative_to_vector == 0:
                        appeared_zone_id = self.right_zone_id

                    self.db.appeared_person_in_camera_create(person_id, self.camera_id, self.camera_group_id,
                                                             appeared_zone_id)

    # delete track IDs that are out of camera range
    def _clear_triggered_appeared_person_collection(self, detect_objects: list[dict]):
        persons: list = list()

        if detect_objects is None:
            self.triggered_appeared_person_collection.clear()
        else:
            for detect_object in detect_objects:
                try:
                    persons.append(detect_object["person"])
                except:
                    pass
            #определяет все ид которые приходят с изображения
            all_track_ids = [person["track_id"] for person in persons]
            new_triggered_appeared_person_collection = dict()
            #цикл по все ид которые были обработаны ранее
            for person_collection_key in self.triggered_appeared_person_collection.keys():
                #если ранее обработаного ид нету в колекции то добавить в его список на удаление
                if person_collection_key not in all_track_ids:
                    self.generations_of_appearances.append(person_collection_key)
                # если кол-во записей на удаление привышает максимально допустимое, удалить это ид из колекции
                if self.generations_of_appearances.count(person_collection_key) <= self.max_count_person_key:
                    new_triggered_appeared_person_collection[person_collection_key] = \
                        self.triggered_appeared_person_collection[person_collection_key]
                else:
                    #чистит список на удаление от того ид который был уже удалён из колекции triggered_appeared_person_collection
                    self.generations_of_appearances = [key for key in self.generations_of_appearances if key != person_collection_key]

            self.triggered_appeared_person_collection = new_triggered_appeared_person_collection
