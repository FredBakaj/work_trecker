import cv2

from core.controller.camera_controller import CameraController


class CameraHandler:
    frame_id: int
    is_frame_limit: bool
    cameras: CameraController

    def __init__(self, config: dict):
        self.cameras: list[CameraController] = self.build_camera_controllers(config["cameras_config"])
        self.frame_id = 0
        self.is_frame_limit = False
        self.frame_limit = 6
        pass

    def call(self):
        while True:
            if cv2.waitKey(20) & 0xFF == 27:  # Exit on pressing 'ESC'
                break

            if self.is_frame_limit and self.frame_id > self.frame_limit:
                continue
            for camera in self.cameras:
                camera.call()

            self.frame_id += 1
        pass

    def build_camera_controllers(self, cameras_config: list[dict]) -> list[CameraController]:
        result: list = list()
        for config in cameras_config:
            normal_line_zone: tuple = tuple(config["normal_line_zone"])
            camera_pc_id: int = config["camera_pc_id"]
            camera_id: int = config["camera_id"]
            camera_group_id: int = config["camera_group_id"]
            left_zone_id: int = config["left_zone_id"]
            right_zone_id: int = config["right_zone_id"]
            processing_frame: int = config["processing_frame"]
            frame_shift: int = config["frame_shift"]

            item = CameraController(
                normal_line_zone,
                camera_pc_id,
                camera_id,
                camera_group_id,
                left_zone_id,
                right_zone_id,
                processing_frame,
                frame_shift,
            )
            result.append(item)
            print(f"pc camera {camera_pc_id} is build")
        return result

