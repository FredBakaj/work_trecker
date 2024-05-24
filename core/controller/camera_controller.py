from core.script.camera import Camera
from core.script.draw_camera import DrawCamera
from core.script.image_objects import ImageObjects


class CameraController:
    def __init__(self):
        self.camera = Camera()
        self.image_objects = ImageObjects()
        self.draw_camera = DrawCamera()
        self.frame_id = 0
        self.processing_frame = 6
        pass

    def call(self):
        self.frame_id += 1
        image_obj_data: dict | None = None

        img = self.camera.get_image()
        if self.frame_id % self.processing_frame == 0:
            image_obj_data = self.image_objects.get_objects(img)
        self.draw_camera.draw(img, image_obj_data)
        pass
