from core.script.camera import Camera
from core.script.draw_camera import DrawCamera
from core.script.Events.events import Events
from core.script.image_objects import ImageObjects
from core.utils.vec_math import VecMath


class CameraController:
    def __init__(self):
        self.vec_math = VecMath()

        self.normal_line_zone = (0.42916666666666664, 0.65, 0.809375, 0.8537037037037037)
        self.camera = Camera()
        self.image_objects = ImageObjects()
        self.events = Events(0, 0, self.normal_line_zone, 0, 1)
        self.draw_camera = DrawCamera()
        self.frame_id = 0
        self.processing_frame = 6

    def call(self):
        self.frame_id += 1
        img = self.camera.get_image()

        image_obj_data: dict | None = None
        height, width, channels = img.shape
        # img_size = (width, height)
        img_size = (width, height)
        #print(img_size)
        if self.frame_id % self.processing_frame == 0:
            image_obj_data = self.image_objects.get_objects(img)
            self.events.call(image_obj_data, img_size)
        self.draw_camera.draw(img, image_obj_data, self.normal_line_zone, img_size)
        pass
