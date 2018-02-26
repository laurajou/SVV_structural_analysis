class Edge():
    def __init__(self, booms, thickness, length):
        self.thickness = thickness
        self.length = length
        self.booms = booms
        self.q_B = 0.0
        self.q_0 = 0.0
        self.q_total = 0.0

    def set_q_B(self, q_b):
        self.q_B = q_b

    def get_q_B(self):
        return self.q_B
