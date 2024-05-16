import cv2

from core.controller.camera_controller import CameraController


class CameraHandler:
    cameras: CameraController

    def __init__(self):
        self.cameras = CameraController()
        pass

    def call(self):
        while True:
            self.cameras.call()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        pass