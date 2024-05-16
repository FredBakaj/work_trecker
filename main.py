import json


from core.handler.camera_handler import CameraHandler


def build_config(binder):
    with open("config.json") as f:
        config = json.load(f)


if __name__ == "__main__":
    camera_handler = CameraHandler()

    camera_handler.call()
