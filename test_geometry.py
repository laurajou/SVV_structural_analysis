import unittest
import geometry
import helpers
import boom
import numpy as np



class TestGeometry(unittest.TestCase):
    def test_inertia(self):
        # test moment of inertia calculation comparing it to results of example 20.2 in Megson
        # IMPORTANT: this only passes the test if on the moment of inertia calculator the line where the list of
        # distances is calculated is COMMENTED OUT!! this is because the list of distances that should be used is given
        # directly on the example so they should NOT be recalculated.
        example_20_2 = geometry.Geometry(16, [0])
        example_20_2.boom_areas = [640, 600, 600, 600, 620, 640, 640, 850, 640, 600, 600, 600, 620, 640, 640, 850]
        example_20_2.y_dists = np.array([660, 600, 420, 228, 25, -204, -396, -502, -540, 600, 420, 228, 25, -204, -396, -502])
        example_20_2.centroid = (0, 0)
      #  example_20_2.moment_inertia_Izz()
        self.assertTrue(example_20_2.y_dists.size == example_20_2.number_booms)
        self.assertTrue(len(example_20_2.boom_areas) == example_20_2.y_dists.size)
        # 1 is a good enough error because in Megson they round the contribution of each boom, so they accumulate error
        # from the 16 components
       # self.assertTrue(abs(example_20_2.Izz*10**(-6) - 1854) < 1)
        print('--- end of inertia test ---')

    def test_boom_area_1(self):
        # following the example 20.1 of Megson with only one boom.
        neutral_axis = (0, 1, 0)
        boom0 = boom.Boom([0, 200], [[1, 2, 600], [2, 3, 400]], 300, neutral_axis)
        boom1 = boom.Boom([597.927455, 150], [], 300, neutral_axis)
        boom2 = boom.Boom([0, -200], [], 300, neutral_axis)
        example_20_1 = geometry.Geometry(3, [boom0, boom1, boom2])
        boom0.calculate_area(example_20_1)
        self.assertTrue(abs(boom0.area - 1050) < 0.1)
        print('--- end of test area calculation ---')


    def test_boom_area_2(self):
        # following the example on slide 43 of https://www.slideshare.net/scemd3/lec6aircraft-structural-idealisation-1
        # set up boom architecture
        neutral_axis = (0, 1, 0)
        boom0 = boom.Boom([-250, 150], [[1, 10, 500], [3, 10, 300]], 1000, neutral_axis)
        boom1 = boom.Boom([250, 150], [[0, 10, 500], [2, 8, 300]], 640, neutral_axis)
        boom2 = boom.Boom([250, -150], [[1, 8, 300], [3, 10, 500]], 640, neutral_axis)
        boom3 = boom.Boom([-250, -150], [[0, 10, 300], [2, 10, 500]], 1000, neutral_axis)

        example_43 = geometry.Geometry(4, [boom0, boom1, boom2, boom3])
        for element in [boom0, boom1, boom2, boom3]:
            element.calculate_area(example_43)

        # test the boom areas
        example_43.get_areas()
        self.assertTrue(abs(example_43.boom_areas[0] - example_43.boom_areas[3]) < 0.01 and
                        abs(example_43.boom_areas[0] - 4000) < 0.01)
        self.assertTrue(abs(example_43.boom_areas[1] - example_43.boom_areas[1]) < 0.01 and
                        abs(example_43.boom_areas[1] - 3540) < 0.01)

        # test centroid
        example_43.calc_centroid()
        print(example_43.centroid)
        self.assertTrue(abs(abs(example_43.centroid[0]) - 15.25) < 0.1)
        self.assertTrue(abs(abs(example_43.centroid[1]) - 0.0) < 0.1)

        # test moments of inertia
        example_43.moment_inertia_Izz()
        example_43.moment_inertia_Iyy()
        example_43.moment_inertia_Izy()
        self.assertTrue(abs(example_43.Izz - 339300000) < 1)
        self.assertTrue(abs(example_43.Iyy - 938992042.5) < 1)
        self.assertTrue(abs(example_43.Izy) < 1)

        print('--- end of combination test ---')


        return None


    def test_helper(self):
        self.assertTrue(abs(helpers.distance((-4, 6.5), (-7, 17)) - 10.920164833920778) < 0.001)
        self.assertTrue(abs(helpers.distance((50.67, -4.006), (-3.345, 36.98)) - 67.80466371128169) < 0.001)

    def test_helpers_point_line(self):
        self.assertTrue(abs(helpers.distance_point_line((5, 6), (-2, 3, 4)) - 3.328) < 0.001)
        self.assertTrue(abs(helpers.distance_point_line((-3, 7), (6, -5, 10)) - 5.506) < 0.001)


if __name__ == '__main__':
    unittest.main()