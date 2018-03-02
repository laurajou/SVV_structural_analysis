class Edge:
    def __init__(self, booms, thickness, length):
        """

        :param booms: list of booms that the edge is uniting
        :param thickness: thickness of the skin section the edge represents
        :param length: length of the skin section the edge represents
        """
        self.thickness = thickness
        self.length = length
        self.booms = booms
        self.q_B = 0.0
        self.q_0 = 0.0
        self.q_total = 0.0
        self.q_T = 0.0
        self.shear_stress = 0.0

