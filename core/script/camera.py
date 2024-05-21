from typing import Any

import cv2
import numpy as np
import requests
from cv2 import VideoCapture, Mat
from numpy import ndarray, dtype, generic
import face_recognition


class Camera:
    cap: VideoCapture

    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        #from video
        # video_path = "data/media_w670536183_19695.ts"
        # self.cap = cv2.VideoCapture(video_path)
        # self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # self.frame_id = 1

        pass

    def get_image(self) -> Mat | ndarray[Any, dtype[generic]] | ndarray:
        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        #from camera
        frame: Mat | ndarray[Any, dtype[generic]] | ndarray
        ret, frame = self.cap.read()

        #from video
        # if self.frame_count <= self.frame_id:
        #     self.frame_id = 1
        #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)
        # # Read the frame
        # ret, frame = self.cap.read()
        # self.frame_id += 1

        #from url
        # url = "https://static.wikia.nocookie.net/nijisanjilore/images/e/ef/Humans.jpg/revision/latest?cb=20220830053327"
        # response = requests.get(url)
        # # Преобразование содержимого в формат, подходящий для чтения OpenCV
        # image_data = np.array(bytearray(response.content), dtype=np.uint8)
        # # Чтение изображения с использованием OpenCV
        # frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        #from file
        # frame = face_recognition.load_image_file("data/img2.png")

        return frame
