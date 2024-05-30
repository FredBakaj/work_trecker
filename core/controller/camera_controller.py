from core.script.camera import Camera
from core.script.draw_camera import DrawCamera
from core.script.Events.events import Events
from core.script.image_objects import ImageObjects


class CameraController:
    def __init__(self):
        self.camera = Camera()
        self.image_objects = ImageObjects()
        self.events = Events(0, 0, (0.386458, 0.40208, 0.91875, 0.49792), 0, 1)
        self.draw_camera = DrawCamera()
        self.frame_id = 0
        self.processing_frame = 6
        pass

    def call(self):
        self.frame_id += 1
        image_obj_data: dict | None = None

        img = self.camera.get_image()
        if self.frame_id % self.processing_frame == 0:
            height, width, channels = img.shape
            img_size = (width, height)
            image_obj_data = self.image_objects.get_objects(img)
            self.events.call(image_obj_data, img_size)
        self.draw_camera.draw(img, image_obj_data)
        pass
