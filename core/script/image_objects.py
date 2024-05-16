from typing import Any

from cv2 import Mat
from numpy import ndarray, dtype, generic
from ultralytics import YOLO

from core.script.camera import Camera
from collections import defaultdict
import numpy as np


class ImageObjects:
    def __init__(self):
        self.camera: Camera = Camera()
        self.model_det_person = YOLO("core/ai_models/yolov8n.pt")
        self.model_det_face = YOLO("core/ai_models/last.pt")
        self.track_history = defaultdict(lambda: [])
        pass

    def get_objects(self) -> dict:
        result: dict = dict()
        detect_objects: list[dict] = list()
        img: Mat | ndarray[Any, dtype[generic | generic]] | ndarray = self.camera.get_image()

        persons: list[dict] = self.get_persons(img)
        if persons is not None:
            for person in persons:
                box = person["box"].detach().cpu().numpy().astype(int)
                x, y, width, height = box
                person_img = self.apply_mask_to_image(img, box)
                face: dict | None = self.get_face(person_img)

                if face is not None:
                    face_box = face["box"].detach().cpu().numpy().astype(int)
                    face["global_x"] = x + face_box[0]
                    face["global_y"] = y + face_box[1]

                result_data = dict()
                result_data["person"] = person
                result_data["face"] = face

                detect_objects.append(result_data)

        result["img"] = img
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
                if cls != 0: continue
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
        detect_results = self.model_det_face.track(img, persist=True, verbose=False)
        names = self.model_det_face.model.names

        boxes = detect_results[0].boxes.xyxy.cpu()

        if len(boxes) != 0:
            # Extract prediction detect_results
            clss = detect_results[0].boxes.cls.cpu().tolist()
            confs = detect_results[0].boxes.conf.float().cpu().tolist()

            for box, cls in zip(boxes, clss):
                result["cls"] = cls
                result["box"] = box
                result["names"] = names
                # add first face when the model find
                break
            return result
        return None

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
