import cv2

from core.script.camera import Camera


# Callback function to print the coordinates of the mouse click
def print_mouse_coordinates(event, x, y, flags, param, camera_width, camera_height):
    if event == cv2.EVENT_LBUTTONDOWN:  # Event when the left mouse button is pressed
        normalize_coordinates = (x / camera_width, y / camera_width)
        print(f"Mouse coordinates: ({x}, {y})")
        print(f"Mouse normalize coordinates: {normalize_coordinates}")


if __name__ == '__main__':
    # Create a window
    cv2.namedWindow('Image')

    # Set the mouse callback function to 'print_mouse_coordinates'

    camera = Camera()
    # Load an image
    image = camera.get_image()
    height, width, channels = image.shape
    print("Camera size: ", (width, height))

    # Display the image
    cv2.setMouseCallback('Image',
                         lambda event, x, y, flags, param: print_mouse_coordinates(event, x, y, flags, param, width,
                                                                                   height))
    while True:
        cv2.imshow('Image', image)
        if cv2.waitKey(20) & 0xFF == 27:  # Exit on pressing 'ESC'
            break
        image = camera.get_image()

    # Clean up
    cv2.destroyAllWindows()
