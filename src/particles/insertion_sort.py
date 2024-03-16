
class InsertionSort:

    @staticmethod
    def sort_high_to_low(particle_list: list) -> None:
        for i in range(1, len(particle_list)):
            item = particle_list[i]
            if item.get_distance() > particle_list[i - 1].get_distance():
                InsertionSort.sort_up_high_to_low(particle_list, i)

    @staticmethod
    def sort_up_high_to_low(particle_list: list, index: int) -> None:
        item = particle_list[index]
        attempt_pos = index - 1
        while attempt_pos != 0 and particle_list[attempt_pos - 1].get_distance() < item.get_distance():
            attempt_pos -= 1
        particle_list.pop(index)
        particle_list.insert(attempt_pos, item)
