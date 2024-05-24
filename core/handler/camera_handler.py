import cv2

from core.controller.camera_controller import CameraController


class CameraHandler:
    frame_id: int
    is_frame_limit: bool
    cameras: CameraController

    def __init__(self):
        self.cameras = CameraController()
        self.frame_id = 0
        self.is_frame_limit = False
        self.frame_limit = 6
        pass

    def call(self):
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if self.is_frame_limit and self.frame_id > self.frame_limit:
                continue

            self.cameras.call()

            self.frame_id += 1
        pass
