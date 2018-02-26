import unittest
import geometry
import helpers
import boom
import edges
import numpy as np
import structural_analysis

class TestGeometry(unittest.TestCase):
    def test_inertia(self):
        # test moment of inertia calculation comparing it to results of example 20.2 in Megson
        # IMPORTANT: this only passes the test if on the moment of inertia calculator the line where the list of
        # distances is calculated is COMMENTED OUT!! this is because the list of distances that should be used is given
        # directly on the example so they should NOT be recalculated.
        example_20_2 = geometry.Geometry(16, [0], [])
        example_20_2.boom_areas = [640, 600, 600, 600, 620, 640, 640, 850, 640, 600, 600, 600, 620, 640, 640, 850]
        example_20_2.y_dists = np.array([660, 600, 420, 228, 25, -204, -396, -502, -540, 600, 420, 228, 25, -204, -396, -502])
        example_20_2.centroid = (0, 0)
      #  example_20_2.moment_inertia_Izz()
        # 1 is a good enough error because in Megson they round the contribution of each boom, so they accumulate error
        # from the 16 components
       # self.assertTrue(abs(example_20_2.Izz*10**(-6) - 1854) < 1)
        print('--- end of inertia test ---')

    def test_boom_area_1(self):
        # following the example 20.1 of Megson with only one boom.
        neutral_axis = (0, 1, 0)
        boom0 = boom.Boom(0, [0, 200], 300, neutral_axis)
        boom1 = boom.Boom(1, [597.927455, 150], 300, neutral_axis)
        boom2 = boom.Boom(2, [0, -200], 300, neutral_axis)
        edge01 = edges.Edge([0, 1], 2, 600)
        edge02 = edges.Edge([0, 2], 3, 400)
        example_20_1 = geometry.Geometry(3, [boom0, boom1, boom2], [edge01, edge02])
        example_20_1.construct_geometry()
        boom0.calculate_area(example_20_1)
        self.assertTrue(abs(boom0.area - 1050) < 0.1)

    def test_boom_area_2(self):
        # following the example on slide 43 of https://www.slideshare.net/scemd3/lec6aircraft-structural-idealisation-1
        # set up boom architecture
        neutral_axis = (0, 1, 0)
        boom0 = boom.Boom(0, [-250, 150], 1000, neutral_axis)
        boom1 = boom.Boom(1, [250, 150], 640, neutral_axis)
        boom2 = boom.Boom(2, [250, -150], 640, neutral_axis)
        boom3 = boom.Boom(3, [-250, -150], 1000, neutral_axis)
        edge01 = edges.Edge([0, 1], 10, 500)
        edge03 = edges.Edge([0, 3], 10, 300)
        edge12 = edges.Edge([1, 2], 8, 300)
        edge23 = edges.Edge([2, 3], 10, 500)

        # calculate area for each boom
        example_43 = geometry.Geometry(4, [boom0, boom1, boom2, boom3], [edge01, edge03, edge12, edge23])
        example_43.construct_geometry()
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

    def test_inertia(self):
        # problem 20.1 taken from Megson. Solution is given on the book
        neutral_axis = (0, 1, 0)
        # set up boom architecture
        boom0 = boom.Boom(0, [0, 150], 1000, neutral_axis)
        boom1 = boom.Boom(1, [500, 150], 50 * 8 + 30 * 8, neutral_axis)
        boom2 = boom.Boom(2, [500, -150], 50 * 8 + 30 * 8, neutral_axis)
        boom3 = boom.Boom(3, [0, -150], 1000, neutral_axis)
        edge01 = edges.Edge([0, 1], 10, 500)
        edge03 = edges.Edge([0, 3], 10, 300)
        edge12 = edges.Edge([1, 2], 8, 300)
        edge23 = edges.Edge([2, 3], 10, 500)

        booms = [boom0, boom1, boom2, boom3]
        edge_list = [edge01, edge03, edge12, edge23]
        problem_20_1 = geometry.Geometry(4, booms, edge_list)
        problem_20_1.construct_geometry()

        # calculate boom area for each boom
        for element in booms:
            element.calculate_area(problem_20_1)
        self.assertTrue(abs(boom0.area - 4000) < 1)
        self.assertTrue(abs(boom0.area - boom3.area) < 0.01)
        self.assertTrue(abs(boom1.area - 3540) < 1)
        self.assertTrue(abs(boom1.area - boom2.area) < 0.01)

    def test_shear_flow(self):
        # following the problem 23.6 in Megson
        # set up booms and edges
        neutral_axis = (0, 1, 0)
        boom0 = boom.Boom(0, [1092, 153], 0.0, neutral_axis)
        boom1 = boom.Boom(1, [736, 153], 0.0, neutral_axis)
        boom2 = boom.Boom(2, [380, 153], 0.0, neutral_axis)
        boom3 = boom.Boom(3, [0, 153], 0.0, neutral_axis)
        boom4 = boom.Boom(4, [0, -153], 0.0, neutral_axis)
        boom5 = boom.Boom(5, [380, -153], 0.0, neutral_axis)
        boom6 = boom.Boom(6, [736, -153], 0.0, neutral_axis)
        boom7 = boom.Boom(7, [1092, -153], 0.0, neutral_axis)
        boom_list = [boom0, boom1, boom2, boom3, boom4, boom5, boom6, boom7]
        edge01 = edges.Edge([0, 1], 0.915, 356)
        edge70 = edges.Edge([7, 0], 1.250, 306)
        edge12 = edges.Edge([1, 2], 0.915, 356)
        edge32 = edges.Edge([3, 2], 0.783, 380)
        edge25 = edges.Edge([2, 5], 1.250, 306)
        edge43 = edges.Edge([4, 3], 1.250, 610)
        edge54 = edges.Edge([5, 4], 0.783, 380)
        edge56 = edges.Edge([5, 6], 0.915, 356)
        edge67 = edges.Edge([6, 7], 0.915, 356)
        edge_list = [edge25, edge12, edge01, edge70, edge67, edge56, edge25, edge54, edge43, edge32]
        problem_23_6 = geometry.Geometry(8, boom_list, edge_list, [217872, 167780], 24.2*10**9)
        problem_23_6.set_cells([[edge25, edge56, edge67, edge70, edge01, edge12], [edge25, edge54, edge43, edge32]])
        boom0.area = 1290
        boom1.area = 645
        boom2.area = 1290
        boom3.area = 645
        boom4.area = 645
        boom5.area = 1290
        boom6.area = 645
        boom7.area = 1290
        problem_23_6.get_areas()
        problem_23_6.construct_geometry()
        problem_23_6.calc_centroid()
        problem_23_6.moment_inertia_Izy()
        problem_23_6.moment_inertia_Iyy()
        problem_23_6.moment_inertia_Izz()

        for boom_element in boom_list:
            boom_element.calc_y_dist(problem_23_6)
            boom_element.calc_z_dist(problem_23_6)
        # calculate geometrical properties

        self.assertTrue(abs(problem_23_6.Izz * 10**(-6) - 181.2) < 1)
        # calculate shear flow due to shear forces

        T = lambda x: 10 ** 6
        problem_23_6_section = structural_analysis.DiscreteSection(neutral_axis, problem_23_6)
        problem_23_6_section.calc_shear_flow(0, 66750)
        print('calculation of the shear flow due to torsion')
        problem_23_6_section.torsion_shear_flow(T, problem_23_6, 1.0)


    def test_helper(self):
        self.assertTrue(abs(helpers.distance((-4, 6.5), (-7, 17)) - 10.920164833920778) < 0.001)
        self.assertTrue(abs(helpers.distance((50.67, -4.006), (-3.345, 36.98)) - 67.80466371128169) < 0.001)

    def test_helpers_point_line(self):
        self.assertTrue(abs(helpers.distance_point_line((5, 6), (-2, 3, 4)) - 3.328) < 0.001)
        self.assertTrue(abs(helpers.distance_point_line((-3, 7), (6, -5, 10)) - 5.506) < 0.001)


if __name__ == '__main__':
    tester = TestGeometry()
    tester.test_shear_flow()