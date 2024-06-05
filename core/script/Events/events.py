from typing import Any

from core.script.Events.appeared_person_in_camera_event import AppearedPersonInCameraEvent
from core.script.Events.person_crossed_zone_event import PersonCrossedZoneEvent


class Events:
    def __init__(self, camera_id: int,
                 camera_group_id: int,
                 zone_line_normal_vec: tuple,
                 left_zone_id: int,
                 right_zone_id: int):

        self.right_zone_id = right_zone_id
        self.left_zone_id = left_zone_id
        self.zone_line_normal_vec = zone_line_normal_vec

        self.camera_id: int = camera_id
        self.camera_group_id: int = camera_group_id

        self.appeared_person_in_camera_event = AppearedPersonInCameraEvent(
            self.camera_id,
            self.camera_group_id,
            self.zone_line_normal_vec,
            self.left_zone_id,
            self.right_zone_id
        )

        self.person_crossed_zone_event = PersonCrossedZoneEvent(
            self.camera_id,
            self.camera_group_id,
            self.zone_line_normal_vec,
            self.left_zone_id,
            self.right_zone_id
        )

    def call(self, img_obj_data: dict, img_size: tuple[Any, Any]) -> None:
        self.appeared_person_in_camera_event.call(img_obj_data, img_size)
        self.person_crossed_zone_event.call(img_obj_data, img_size)
        pass


