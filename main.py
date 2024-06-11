import json

from core.handler.camera_handler import CameraHandler


def build_config():
    config: dict
    with open("config.json") as f:
        config = json.load(f)
    return config


if __name__ == "__main__":
    config = build_config()
    camera_handler = CameraHandler(config)

    camera_handler.call()
