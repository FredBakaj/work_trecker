from collections import defaultdict
from typing import Any

import face_recognition
import numpy as np
from cv2 import Mat
from numpy import ndarray, dtype, generic
from ultralytics import YOLO

from core.script.camera import Camera
from core.script.profile_tracking import ProfileTracking
from core.utils.box_math import BoxMath


class ImageObjects:
    def __init__(self):
        self.camera: Camera = Camera()
        self.model_det_person = YOLO("core/ai_models/yolov8n.pt")
        self.model_det_face = YOLO("core/ai_models/last.pt")
        self.track_history = defaultdict(lambda: [])
        self.profile_tracking = ProfileTracking()
        self.box_math = BoxMath()
        pass

    def get_objects(self, img) -> dict:
        result: dict = dict()
        detect_objects: list[dict] = list()

        persons: list[dict] = self.profile_tracking.delta_time_call(self.get_persons.__name__,
                                                                    lambda: self.get_persons(img))
        faces: list[dict] = list()
        if persons is not None:
            faces = self.profile_tracking.delta_time_call(self.get_faces.__name__,
                                                          lambda: self.get_faces(img))
            pass

        if persons is not None:
            for person in persons:
                face: dict | None = None
                if len(faces) > 0:
                    for face_ in faces:
                        person_box = person["box"].detach().cpu().numpy().astype(int)
                        face_box = face_["box"]
                        is_person_face = self.box_math.is_box_within(face_box, person_box)
                        if is_person_face:
                            face = face_

                result_data = dict()
                result_data["person"] = person
                result_data["face"] = face

                detect_objects.append(result_data)

        result["detect_objects"] = detect_objects
        return result

    def get_persons(self, img) -> list[dict] | None:
        result: list[dict] = list()
        detect_results = self.model_det_person.track(img, persist=True, verbose=False)
        names = self.names = self.model_det_person.model.names

        boxes = detect_results[0].boxes.xyxy.cpu()

        if detect_results[0].boxes.id is not None:
            # Extract prediction detect_results
            clss = detect_results[0].boxes.cls.cpu().tolist()
            track_ids = detect_results[0].boxes.id.int().cpu().tolist()
            confs = detect_results[0].boxes.conf.float().cpu().tolist()
            for box, cls, track_id in zip(boxes, clss, track_ids):
                # if cls is not person
                if cls != 0:
                    continue
                # Store tracking history
                track = self.track_history[track_id]
                track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                if len(track) > 30:
                    track.pop(0)

                # Plot tracks
                track_move_points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))

                result_data = dict()
                result_data["track_id"] = track_id
                result_data["cls"] = cls
                result_data["track_move_points"] = track_move_points
                result_data["box"] = box
                result_data["names"] = names

                result.append(result_data)

            return result

        return None

    def get_face(self, img) -> dict | None:
        result: dict = dict()
        face_locations: list[tuple] = face_recognition.face_locations(img)
        if len(face_locations) != 0:
            y_min, x_min, y_max, x_max = face_locations[0]
            result["box"] = (x_min, y_min, x_max, y_max)
            return result
        return None

    def get_faces(self, img) -> list[dict]:
        result: list[dict] = list()
        face_locations: list[tuple] = face_recognition.face_locations(img)
        if len(face_locations) != 0:
            for location in face_locations:
                face_data = dict()
                y_min, x_min, y_max, x_max = location
                face_data["box"] = (x_min, y_min, x_max, y_max)
                result.append(face_data)
        return result

    def get_faces2(self, img):
        result: list[dict] = list()
        detect_results = self.model_det_face.track(img, persist=True, verbose=False)
        names = self.names = self.model_det_face.model.names

        boxes = detect_results[0].boxes.xyxy.cpu()

        if len(boxes) > 0:
            # Extract prediction detect_results
            clss = detect_results[0].boxes.cls.cpu().tolist()
            confs = detect_results[0].boxes.conf.float().cpu().tolist()
            for box, cls in zip(boxes, clss):
                result_data = dict()
                result_data["cls"] = cls
                result_data["box"] = box
                result_data["names"] = names

                result.append(result_data)

        return result

    def apply_mask_to_image(self, image, box):
        # Распаковка координат бокса
        x_min, y_min, x_max, y_max = box

        # Создание маски того же размера, что и изображение, и заполнение ее нулями
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # Установка области бокса на 1
        mask[y_min:y_max, x_min:x_max] = 1

        # Преобразование маски в формат с тремя каналами, если изображение цветное
        if len(image.shape) == 3:
            mask = np.stack([mask] * 3, axis=-1)

        # Умножение изображения на маску
        masked_image = image * mask

        return masked_image

    def get_person_recognition(self, img):
        biden_encoding = self.profile_tracking.delta_time_call(face_recognition.face_encodings.__name__,
                                                               lambda: face_recognition.face_encodings(img))
        print(f"count faces {biden_encoding}")
        # unknown_encoding = face_recognition.face_encodings(img)
        #
        # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
        return
