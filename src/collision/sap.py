from src.collision.box import Box


class SAP:

    __boxes = []
    __end_points_x = []
    __end_points_y = []
    __end_points_z = []

    @classmethod
    def add_box(cls, box: Box):
        cls.__end_points_x.extend(box.get_x())
        cls.__end_points_x.sort(key=lambda x: x.value)
        cls.__end_points_y.extend(box.get_y())
        cls.__end_points_y.sort(key=lambda x: x.value)
        cls.__end_points_z.extend(box.get_z())
        cls.__end_points_z.sort(key=lambda x: x.value)

        cls.__boxes.append(box)

    @classmethod
    def batch_insertion(cls, boxes: list[Box]) -> None:
        x_values = []
        y_values = []
        z_values = []
        for box in boxes:
            x_values.extend(box.get_x())
            y_values.extend(box.get_y())
            z_values.extend(box.get_z())
        x_values.sort(key=lambda x: x.value)
        y_values.sort(key=lambda x: x.value)
        z_values.sort(key=lambda x: x.value)

        if not cls.__end_points_x:
            cls.__end_points_x.append(x_values.pop(0))
            cls.__end_points_y.append(y_values.pop(0))
            cls.__end_points_z.append(z_values.pop(0))

        for i in range(len(x_values) + len(cls.__end_points_x)):
            if i == len(cls.__end_points_x):
                cls.__end_points_x.append(x_values.pop(0))
            elif x_values[0] <= cls.__end_points_x[i]:
                cls.__end_points_x.insert(0, x_values.pop(0))

            if i == len(cls.__end_points_y):
                cls.__end_points_y.append(y_values.pop(0))
            elif y_values[0] <= cls.__end_points_y[i]:
                cls.__end_points_y.insert(0, y_values.pop(0))

            if i == len(cls.__end_points_z):
                cls.__end_points_z.append(z_values.pop(0))
            elif z_values[0] <= cls.__end_points_z[i]:
                cls.__end_points_z.insert(0, z_values.pop(0))
        cls.__boxes.extend(boxes)

    @classmethod
    def update_object(cls, box: Box, min_points: list[float], max_points: list[float]) -> None:
        box.update(min_points, max_points)
        cls.__end_points_x.sort(key=lambda x: x.value)
        cls.__end_points_y.sort(key=lambda x: x.value)
        cls.__end_points_z.sort(key=lambda x: x.value)

    @classmethod
    def get_colliding_boxes(cls, compare_box: Box) -> list:
        colliding_boxes = []
        for box in cls.__boxes:
            if (box.get_x()[0] < compare_box.get_x()[0] < box.get_x()[1] < compare_box.get_x()[1] or
               box.get_x()[1] > compare_box.get_x()[1] > box.get_x()[0] > compare_box.get_x()[0]) and \
               (box.get_y()[0] < compare_box.get_y()[0] < box.get_y()[1] < compare_box.get_y()[1] or
               box.get_y()[1] > compare_box.get_y()[1] > box.get_y()[0] > compare_box.get_y()[0]) and \
               (box.get_z()[0] < compare_box.get_z()[0] < box.get_z()[1] < compare_box.get_z()[1] or
               box.get_z()[1] > compare_box.get_z()[1] > box.get_z()[0] > compare_box.get_z()[0]):
                colliding_boxes.append(box)

        return colliding_boxes

    @classmethod
    def get_colliding_pairs(cls) -> list[list]:
        overlapping_pairs = []
        for box in cls.__boxes:
            if any(box in sl for sl in overlapping_pairs):
                # box partner was already found, no need for duplicate check
                continue
            overlapping_x = [x.owner for x in cls.__end_points_x[cls.__end_points_x.index(box.get_min_x())+1:cls.__end_points_x.index(box.get_max_x())]]
            overlapping_y = [x.owner for x in cls.__end_points_y[cls.__end_points_y.index(box.get_min_y())+1:cls.__end_points_y.index(box.get_max_y())]]
            overlapping_z = [x.owner for x in cls.__end_points_z[cls.__end_points_z.index(box.get_min_z())+1:cls.__end_points_z.index(box.get_max_z())]]

            overlapping_owners = list(set.intersection(*map(set, [overlapping_x, overlapping_y, overlapping_z])))
            for owner in overlapping_owners:
                overlapping_pairs.append([box, owner])

        return overlapping_pairs

    @classmethod
    def get_end_points_x(cls) -> list:
        return cls.__end_points_x

    @classmethod
    def get_end_points_y(cls) -> list:
        return cls.__end_points_y

    @classmethod
    def get_end_points_z(cls) -> list:
        return cls.__end_points_z

