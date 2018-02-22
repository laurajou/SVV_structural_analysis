import numpy as np
import math
from helpers import *


class Geometry:
    def __init__(self, number_booms, booms):
        """
        Initialise instance of Geometry that describes an idealised cross-section.
        :param number_booms: number of booms in idealised cross-section.
        :param booms: list of Boom objects.
        """
        self.number_booms = number_booms
        self.booms = booms
        self.boom_areas = np.zeros(self.number_booms)
        self.centroid = np.zeros(2)
        self.neutral_axis = ()  # in the form A, B, C : neutral axis line Az + By + C = 0
        self.z_dists = np.zeros(self.number_booms)
        self.y_dists = np.zeros(self.number_booms)
        self.Iyy = 0.0
        self.Izz = 0.0
        self.Izy = 0.0

    def get_areas(self):
        """
        Update values in self.boom_areas to include the areas of the booms.
        """
        for i, boom in enumerate(self.booms):
            self.boom_areas[i] = boom.area

    def calc_centroid(self):
        """
        Calculate centroid position (z, y) taking as origin of coordinates the hinge point.
        Set self.centroid to calculated coordinates.
        """
        sum_y = 0.0
        sum_z = 0.0
        for boom in self.booms:
            sum_y += boom.area * boom.coordinates[1]
            sum_z += boom.area * boom.coordinates[0]

        self.centroid[1] = sum_y/sum(self.boom_areas)
        self.centroid[0] = sum_z/sum(self.boom_areas)

    def calc_y_dists(self):
        """
        Calculates the distance in y-direction from each boom to the centroid and store in a list y_dists.
        Modifies self.y_dists[]
        """
        for i, boom in enumerate(self.booms):
            self.y_dists[i] = boom.coordinates[1] - self.centroid[1]

    def calc_z_dists(self):
        """
        Calculates the distance in z-direction from each boom to the centroid and store in a list z_dists.
        Modifies self.z_dists[]
        """
        for i, boom in enumerate(self.booms):
            self.z_dists[i] = boom.coordinates[0] - self.centroid[0]

    def moment_inertia_Izz(self):
        """
        Calculates moment of inertia in z using Izz = Sigma(Bi * yi^2)
        Updates self.Izz to moment of inertia.
        """
        self.calc_y_dists()
        for i, area in enumerate(self.boom_areas):
            self.Izz += area * self.y_dists[i] ** 2

    def moment_inertia_Iyy(self):
        """
        Calculates moment of inertia in y using Izz = Sigma(Bi * zi^2)
        Updates self.Iyy to moment of inertia.
        """
        self.calc_z_dists()
        for i, area in enumerate(self.boom_areas):
            self.Iyy += area * self.z_dists[i] ** 2

    def moment_inertia_Izy(self):
        """
        Calculates moment of inertia in zy using Izy = Sigma(Bi * zi * yi)
        Updates self.Izy to moment of inertia.
        """
        self.calc_y_dists()
        self.calc_z_dists()
        for i, area in enumerate(self.boom_areas):
            self.Izy += area * self.z_dists[i] * self.y_dists[i]

    def set_neutral_axis(self, A, B, C):
        """
        Set neutral axis to new value
        """
        self.neutral_axis = (A, B, C)


