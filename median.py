import numpy as np
import unittest


def median(input_list, filter_length):
    if filter_length % 2 == 0:
        raise ValueError("Please enter an odd number")

    outsider = filter_length // 2
    filtered_list = []
    input_padding_same = (
        [0] * outsider + input_list + [0] * outsider)

    for i in range(outsider, len(input_padding_same) - outsider):
        window = input_padding_same[i - outsider:i + outsider + 1]
        window_sorted = sorted(window)
        median_value = window_sorted[filter_length // 2]
        filtered_list.append(median_value)

    return filtered_list

class TestMedianFilterWithNumpy(unittest.TestCase):
    def test_median_filter(self):
        input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        filter_length = 3
        result = median(input_list, filter_length)

        numpy_result = []
        for i in range(len(input_list)):
            start = max(0, i - filter_length // 2)
            end = min(len(input_list), i + filter_length // 2 + 1)
            window = input_list[start:end]
            if len(window) < filter_length:
                window = [0] * (filter_length - len(window)) + window
            numpy_result.append(int(np.median(window)))

        self.assertEqual(result, numpy_result)

        with self.assertRaises(ValueError):
            median(input_list, 4)


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
