import random
from datetime import datetime

from core.handler.data_base_handler import DataBaseHandler

db = DataBaseHandler(is_moke_datetime=True)

from datetime import datetime, timedelta


def person_create_log(datetime_appeared_zone_id, appeared_person_log,
                      datetime_person_identification, person_identification,
                      datetime_person_crossed_zone, person_crossed_zone):
    person_id, camera_id, camera_group_id, appeared_zone_id = appeared_person_log
    db.set_moke_datetime(datetime_appeared_zone_id)
    db.appeared_person_in_camera_create(person_id, camera_id, camera_group_id, appeared_zone_id)

    person_id, camera_id, camera_group_id, human_id = person_identification
    db.set_moke_datetime(datetime_person_identification)
    db.person_identification_create(person_id, camera_id, camera_group_id, human_id)

    person_id, camera_id, camera_group_id, current_zone_id, abandoned_zone_id = person_crossed_zone
    db.set_moke_datetime(datetime_person_crossed_zone)
    db.person_crossed_zone_create(person_id, camera_id, camera_group_id, current_zone_id, abandoned_zone_id)


def create_log(human_id, person_id, month, day):
    camera_group_id = 0
    minutes = [1,4,6,15,30,46,22]
    actions = [
        (datetime(2024, month, day, 8, 0, 0), (person_id, 0, camera_group_id, 0),
         datetime(2024, month, day, 8, 0, 1), (person_id, 0, camera_group_id, human_id),
         datetime(2024, month, day, 8, 0, 3), (person_id, 0, camera_group_id, 0, 1)),

        (datetime(2024, month, day, 9, 0, 0), (person_id + 1, 1, camera_group_id, 1),
         datetime(2024, month, day, 9, 0, 1), (person_id + 1, 1, camera_group_id, human_id),
         datetime(2024, month, day, 9, 0, 3), (person_id + 1, 1, camera_group_id, 1, 0)),

        (datetime(2024, month, day, 9, 13, 0), (person_id + 2, 0, camera_group_id, 0),
         datetime(2024, month, day, 9, 13, 1), (person_id + 2, 0, camera_group_id, human_id),
         datetime(2024, month, day, 9, 13, 3), (person_id + 2, 0, camera_group_id, 0, 1)),

        (datetime(2024, month, day, 14, 16, 0), (person_id + 3, 1, camera_group_id, 1),
         datetime(2024, month, day, 14, 16, 1), (person_id + 3, 1, camera_group_id, human_id),
         datetime(2024, month, day, 14, 16, 3), (person_id + 3, 1, camera_group_id, 1, 0)),

        (datetime(2024, month, day, 14, 49, 0), (person_id + 4, 0, camera_group_id, 0),
         datetime(2024, month, day, 14, 49, 1), (person_id + 4, 0, camera_group_id, human_id),
         datetime(2024, month, day, 14, 49, 3), (person_id + 4, 0, camera_group_id, 0, 1)),

        (datetime(2024, month, day, 17, 0, 0), (person_id + 5, 0, camera_group_id, 1),
         datetime(2024, month, day, 17, 0, 1), (person_id + 5, 0, camera_group_id, human_id),
         datetime(2024, month, day, 17, 0, 3), (person_id + 5, 0, camera_group_id, 1, 0))
    ]

    for action in actions:
        person_create_log(*action)

if __name__ == "__main__":
    create_log(2, 200, 6, 17)
