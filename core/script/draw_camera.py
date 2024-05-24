import cv2
from cv2 import VideoCapture, Mat
from ultralytics.utils.plotting import colors, Annotator


class DrawCamera:
    def __init__(self):
        pass

    def draw(self, img, image_objects_data: dict | None):
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
                        #cv2.circle(img, (person_track_move_points[-1]), 7, colors(7, True), -1)
                        cv2.polylines(img, [person_track_move_points], isClosed=False, color=colors(7, True), thickness=2)

        cv2.imshow('Camera', img)
