from typing import Any

from core.handler.data_base_handler import DataBaseHandler
from core.utils.vec_math import VecMath


class PersonCrossedZoneEvent:
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

        self.triggered_person_crossed_zone_collection: dict = dict()
        self.generations_of_appearances: list = list()
        self.db = DataBaseHandler()
        self.vec_math = VecMath()

    def call(self, img_obj_data: dict, img_size: tuple[Any, Any]):
        self._person_crossed_zone(img_obj_data, img_size)
        pass

    def _person_crossed_zone(self, img_obj_data: dict, img_size: tuple[Any, Any]):
        detect_objects: list[dict] = img_obj_data["detect_objects"]
        zone_line_vec = self.vec_math.calculate_zone_line_vec(img_size, self.zone_line_normal_vec)

        # self._clear_triggered_appeared_person_collection(detect_objects)

        if detect_objects is not None:
            # logic of trigger response to new IDs
            for detect_object in detect_objects:
                person: dict = detect_object["person"]
                person_box = person["box"]
                person_cls = person["cls"]
                person_names = person["names"]
                person_track_move_points: list = person["track_move_points"]
                person_track_id = person["track_id"]
                # якщо в колекції позицій менше 2 записів, значить, що персонаж щойно з'явився, і не може
                # перетнути кордон
                if len(person_track_move_points) < 2: continue
                # person_id: int = self.db.get_new_person_id()
                # self.triggered_person_crossed_zone_collection[person_track_id] = person_id

                # --визначення перетину межі
                previous_person_point = tuple(person_track_move_points[-2][0])
                person_point = tuple(person_track_move_points[-1][0])
                # визначає зону з попереднього кадру
                previous_side_relative_to_vector = self.vec_math.point_relative_to_vector(
                    (zone_line_vec[0], zone_line_vec[1]),
                    (zone_line_vec[2], zone_line_vec[3]),
                    previous_person_point
                )

                # визначає зону з поточного кадру
                side_relative_to_vector = self.vec_math.point_relative_to_vector(
                    (zone_line_vec[0], zone_line_vec[1]),
                    (zone_line_vec[2], zone_line_vec[3]),
                    person_point
                )

                # якщо зони не збігаються, то вважаємо, що був перехід між зонами
                if previous_side_relative_to_vector != side_relative_to_vector:

                    # zone id, based on the position of the point relative to the vector
                    current_zone_id: int = None
                    abandoned_zone_id: int = None
                    if side_relative_to_vector > 0:
                        current_zone_id = self.left_zone_id
                        abandoned_zone_id = self.right_zone_id
                    elif side_relative_to_vector < 0 or side_relative_to_vector == 0:
                        current_zone_id = self.right_zone_id
                        abandoned_zone_id = self.left_zone_id

                    self.db.person_crossed_zone_create(
                        self.db.get_person_id_by_track_id(person_track_id), self.camera_id,
                        self.camera_group_id, current_zone_id, abandoned_zone_id)
