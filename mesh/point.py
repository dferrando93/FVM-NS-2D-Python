import numpy as np

class Point():
    """
    Point class used to define mesh vertex or auxiliar points such as 
    central points.
    
    x: x coordinate
    y: y cordinate
    label: name of the point. If the point is calculated, the default label
    is aux
    """

    def __init__(self, x, y, label="aux"):

        self.x = x
        self.y = y
        self.label = label
        self.owner_faces = []
        self.owner_cells = []

    def __str__(self):
        return "Point {0}: ({1:.2f}, {2:.2f})".format(self.label, self.x, self.y)
    
    def __repr__(self):
        return "Point {0}: ({1:.2f}, {2:.2f})".format(self.label, self.x, self.y)

    def __add__(self, other):

        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):

        x = self.x - other.x
        y = self.y - other.y

        return Point(x, y)

    def __truediv__(self, i):

        x = self.x / i 
        y = self.y / i
        return Point(x, y)

    def __getitem__(self, key):
        if key == 0 or key == "x" or key == "X":
            return self.x
        
        elif key == 1 or key == "y" or key == "Y":
            return self.y
        else:
            return None

    def get_coordinates(self):
        return np.array([self.x, self.y])

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_label(self):
        return self.label
    
    def set_label(self, label):
        self.label = label
        
    def get_owner_faces(self):
        return self.owner_faces
    
    def get_owner_cells(self):
        return self.owner_cells
        
    def add_owner_face(self, label):
        if label not in self.owner_faces:
            self.owner_faces.append(label)
        
    def add_owner_cell(self, label):
        if label not in self.owner_cells:
            self.owner_cells.append(label)
    
if __name__ == "__main__":
    point0 = Point(0, 0, label = 0)
