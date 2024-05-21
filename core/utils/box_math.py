class BoxMath:
    def box_area(self, box):
        x_min, y_min, x_max, y_max = box
        return (y_max - y_min) * (x_max - x_min)

    def intersection_area(self, box1, box2):
        x_min1, y_min1, x_max1, y_max1 = box1
        x_min2, y_min2, x_max2, y_max2 = box2

        # Calculate the coordinates of the intersection rectangle
        inter_x_min = max(x_min1, x_min2)
        inter_y_min = max(y_min1, y_min2)
        inter_x_max = min(x_max1, x_max2)
        inter_y_max = min(y_max1, y_max2)

        # Check if there is an intersection
        if inter_x_min < inter_x_max and inter_y_min < inter_y_max:
            return (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        else:
            return 0

    @staticmethod
    def is_box_collision(box1, box2, threshold=0.8):
        """
        Check if two boxes collide with at least `threshold` overlap area.

        Parameters:
        box1 (tuple): (x_min, y_min, x_max, y_max) of the first box.
        box2 (tuple): (x_min, y_min, x_max, y_max) of the second box.
        threshold (float): Minimum fraction of overlap area required for collision.

        Returns:
        bool: True if the boxes collide with at least `threshold` overlap area, False otherwise.
        """
        # Unpack the box coordinates
        x_min1, y_min1, x_max1, y_max1 = box1
        x_min2, y_min2, x_max2, y_max2 = box2

        # Calculate the (x, y)-coordinates of the intersection rectangle
        x_min_inter = max(x_min1, x_min2)
        y_min_inter = max(y_min1, y_min2)
        x_max_inter = min(x_max1, x_max2)
        y_max_inter = min(y_max1, y_max2)

        # Compute the area of intersection rectangle
        inter_width = max(0, x_max_inter - x_min_inter)
        inter_height = max(0, y_max_inter - y_min_inter)
        inter_area = inter_width * inter_height

        # Compute the area of both the prediction and ground-truth rectangles
        box1_area = (x_max1 - x_min1) * (y_max1 - y_min1)
        box2_area = (x_max2 - x_min2) * (y_max2 - y_min2)

        # Compute the intersection over union (IoU) by taking the intersection area
        # and dividing it by the sum of prediction + ground-truth areas - the intersection area
        union_area = box1_area + box2_area - inter_area

        # Compute the ratio of the intersection area to the union area
        iou = inter_area / union_area

        # Return True if IoU is greater than or equal to the threshold
        return iou >= threshold

    def is_box_within(self, box1, box2):
        """
        Check if box1 is completely within box2.

        Parameters:
        box1 (tuple): (x_min, y_min, x_max, y_max) of the first box.
        box2 (tuple): (x_min, y_min, x_max, y_max) of the second box.

        Returns:
        bool: True if box1 is within box2, False otherwise.
        """
        # Unpack the box coordinates
        x_min1, y_min1, x_max1, y_max1 = box1
        x_min2, y_min2, x_max2, y_max2 = box2

        # Check if all the corners of box1 are within the bounds of box2
        return (x_min1 >= x_min2 and y_min1 >= y_min2 and
                x_max1 <= x_max2 and y_max1 <= y_max2)

