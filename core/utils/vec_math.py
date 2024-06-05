from typing import Any


class VecMath:
    def point_relative_to_vector(self, A, B, P):
        """
        Определяет, на какой стороне от вектора AB находится точка P.

        :param A: кортеж (x1, y1) координаты точки A
        :param B: кортеж (x2, y2) координаты точки B
        :param P: кортеж (x3, y3) координаты точки P
        :return: строка "left", "right" или "on the line"
        """
        x1, y1 = A
        x2, y2 = B
        x3, y3 = P

        # Вычисление псевдоскалярного произведения
        cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

        if cross > 0:
            return -1  # "left"
        elif cross < 0:
            return 1  # "right"
        else:
            return 0  # "on the line"

    def calculate_zone_line_vec(self, img_size: tuple, zone_line_normal_vec: tuple) -> tuple[Any, Any, Any, Any]:
        zone_line_vec: tuple[Any, Any, Any, Any] = (int(zone_line_normal_vec[0] * img_size[0]),
                                                    int(zone_line_normal_vec[1] * img_size[1]),
                                                    int(zone_line_normal_vec[2] * img_size[0]),
                                                    int(zone_line_normal_vec[3] * img_size[1])
                                                    )
        return zone_line_vec
