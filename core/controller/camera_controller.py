from core.script.draw_camera import DrawCamera
from core.script.image_objects import ImageObjects


class CameraController:
    def __init__(self):
        self.image_objects = ImageObjects()
        self.draw_camera = DrawCamera()
        pass

    def call(self):
        image_obj_data: dict = self.image_objects.get_objects()
        self.draw_camera.draw(image_obj_data)
        pass
