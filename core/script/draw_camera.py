import cv2
from cv2 import VideoCapture, Mat
from ultralytics.utils.plotting import colors, Annotator


class DrawCamera:
    def __init__(self):
        pass

    def draw(self, image_objects_data: dict):
        img = image_objects_data["img"]
        detect_objects: list[dict] = image_objects_data["detect_objects"]
        # obj = image_objects_data["obj"]
        # obj_tracks = obj["obj_tracks"]
        # obj_points = obj["obj_points"]
        # obj_cls = obj["obj_cls"]
        annotator = Annotator(img, line_width=2)
        if detect_objects is not None:
            for detect_object in detect_objects:
                person: dict = detect_object["person"]
                person_box = person["box"]
                person_cls = person["cls"]
                person_names = person["names"]
                face: dict | None = detect_object["face"]
                if face is not None:
                    face_box = face["box"].detach().cpu().numpy().astype(int)
                    face_cls = face["cls"]
                    face_names = face["names"]
                    x_min, y_min, x_max, y_max = face_box

                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0),
                                  2)  # зелёный цвет рамки, толщина 2

                annotator.box_label(person_box, color=colors(int(person_cls), True),
                                     label=person_names[int(person_cls)])


                # cv2.circle(img, (obj_tracks[i][-1]), 7, colors(int(obj_cls[i]), True), -1)
                # cv2.polylines(img, [obj_points[i]], isClosed=False, color=colors(int(obj_cls[i]), True), thickness=2)

        cv2.imshow('Camera', img)
