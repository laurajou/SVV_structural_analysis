import unittest
import geometry
import helpers
import numpy as np



class TestGeometry(unittest.TestCase):
    def test_inertia(self):
        # test moment of inertia calculation comparing it to results of example 20.2 in Megson
        example_20_2 = geometry.Geometry(16, 0.0)
        example_20_2.boom_areas = [640, 600, 600, 600, 620, 640, 640, 850, 640, 600, 600, 600, 620, 640, 640, 850]
        example_20_2.y_dists = np.array(
            [660, 600, 420, 228, 25, -204, -396, -502, -540, 600, 420, 228, 25, -204, -396, -502])
        example_20_2.centroid = (0, 0)
        example_20_2.moment_inertia_Izz()
        self.assertTrue(example_20_2.y_dists.size == example_20_2.number_booms)
        self.assertTrue(len(example_20_2.boom_areas) == example_20_2.y_dists.size)
        # 1 is a good enough error because in Megson they round the contribution of each boom, so they accumulate error
        # from the 16 components
        self.assertTrue(abs(example_20_2.Izz*10**(-6) - 1854) < 1)
        return None

    def test_boom_area_1(self):
        # following the example 20.1 of Megson with only one boom. It is difficult to test the rest due to
        # lengths and thicknesses of segments not constant through cross-section. To solve it properly would mean adding
        # features to the code that are not necessary to solve the aileron problem.
        example_20_1 = geometry.Geometry(1, 300.0)
        example_20_1.boom_graph.append([2, 3])  # BOOM 1
        example_20_1.set_neutral_axis(0, 1, 0)
        example_20_1.boom_coordinates = [(0, 200), (597.927455, 150), (0, -200)]
        area = example_20_1.calc_boom_areas(2)
        self.assertTrue(abs(area[0] - 983.333) < 0.1)

    def test_boom_area_2(self):
        # following the example on slide 43 of https://www.slideshare.net/scemd3/lec6aircraft-structural-idealisation-1
        example_43 = geometry.Geometry(4, 1000)
        # set up boom architecture
        example_43.boom_graph.append([2, 4])  # BOOM 1
        example_43.boom_graph.append([1, 3])  # BOOM 2
        example_43.boom_graph.append([2, 4])  # BOOM 3
        example_43.boom_graph.append([1, 3])  # BOOM 4
        example_43.set_neutral_axis(1, 0, 0)
        # set coordinate center at centroid
        example_43.boom_coordinates = [(-250, 150), (250, 150), (250, -150), (-250, -150)]
        # example slightly modified to have uniform thickness and all stringers area are equal to 1000.
        # this means all boom areas should be equal to 4000.
        areas = example_43.calc_boom_areas(10)
        test_passed = True
        for area in areas:
            if area != 4000:
                test_passed = False
        self.assertTrue(test_passed)


    def test_helper(self):
        self.assertTrue(abs(helpers.distance((-4, 6.5), (-7, 17)) - 10.920164833920778) < 0.001)
        self.assertTrue(abs(helpers.distance((50.67, -4.006), (-3.345, 36.98)) - 67.80466371128169) < 0.001)

    def test_helpers_point_line(self):
        self.assertTrue(abs(helpers.distance_point_line((5, 6), (-2, 3, 4)) - 3.328) < 0.001)
        self.assertTrue(abs(helpers.distance_point_line((-3, 7), (6, -5, 10)) - 5.506) < 0.001)


if __name__ == '__main__':
    unittest.main()