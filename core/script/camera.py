from typing import Any

import cv2
import face_recognition
from cv2 import VideoCapture, Mat
from numpy import ndarray, dtype, generic


class Camera:
    cap: VideoCapture

    def __init__(self, camera_pc_id: int) -> None:
        self.cap = cv2.VideoCapture(camera_pc_id)
        #from video
        #video_path = "data/video_bar6.mp4"
        video_path = "data/avi/IPC2_20240830130859 (4).avi"
        self.cap = cv2.VideoCapture(video_path)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_id = 1

        pass

    def get_image(self) -> Mat | ndarray[Any, dtype[generic]] | ndarray:
        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        #from camera
        # frame: Mat | ndarray[Any, dtype[generic]] | ndarray
        # ret, frame = self.cap.read()


        #from video
        if self.frame_count <= self.frame_id:
            self.frame_id = 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)
        # Read the frame
        ret, frame = self.cap.read()
        self.frame_id += 1
        frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        #from url
        # url = "https://static.wikia.nocookie.net/nijisanjilore/images/e/ef/Humans.jpg/revision/latest?cb=20220830053327"
        # response = requests.get(url)
        # # Преобразование содержимого в формат, подходящий для чтения OpenCV
        # image_data = np.array(bytearray(response.content), dtype=np.uint8)
        # # Чтение изображения с использованием OpenCV
        # frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        #from file
        # frame = face_recognition.load_image_file("data/rrr.jpg")
        # frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        return frame

    def get_camera_size(self) -> tuple:
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return (frame_width, frame_height)
