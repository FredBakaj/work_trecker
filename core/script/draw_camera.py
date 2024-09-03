import cv2
from ultralytics.utils.plotting import colors, Annotator

from core.utils.vec_math import VecMath


class DrawCamera:
    def __init__(self):
        self.vec_math = VecMath()

    def draw(self, img, image_objects_data: dict | None, normal_line_zone: tuple | None, img_size: tuple):
        if image_objects_data is not None:
            detect_objects: list[dict] = image_objects_data["detect_objects"]
            annotator = Annotator(img, line_width=2)
            if detect_objects is not None:
                for detect_object in detect_objects:
                    person: dict = detect_object["person"]
                    person_box = person["box"]
                    person_cls = person["cls"]
                    person_names = person["names"]
                    person_track_move_points = person["track_move_points"]
                    face: dict | None = detect_object["face"]
                    if face is not None:
                        face_box = face["box"]
                        human_id: str | None = face["human_id"]
                        x_min, y_min, x_max, y_max, = face_box
                        # cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0),
                        #               2)  # зелёный цвет рамки, толщина 2
                        annotator.box_label(face_box, color=colors(3, True),
                                            label=str(human_id))

                    annotator.box_label(person_box, color=colors(int(person_cls), True),
                                        label=person_names[int(person_cls)])

                    if len(person_track_move_points) > 1:
                        # cv2.circle(img, (person_track_move_points[-1]), 7, colors(7, True), -1)
                        cv2.polylines(img, [person_track_move_points], isClosed=False, color=colors(7, True),
                                      thickness=2)

        if normal_line_zone is not None:
            zone_line_vec = self.vec_math.calculate_zone_line_vec(img_size, normal_line_zone)
            color = (255, 0, 0)  # Колір лінії (в даному випадку, червоний)
            thickness = 2  # Товщина лінії
            cv2.line(img, (zone_line_vec[0], zone_line_vec[1]),
                     (zone_line_vec[2], zone_line_vec[3]), color, thickness)

        cv2.imshow('Camera', img)
