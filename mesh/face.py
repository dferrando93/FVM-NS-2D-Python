import sys
sys.path.append("../functions")
from auxilary_functions import *
from point import Point
import numpy as np


class Face():
    """
    Face class used to define mesh faces.
    
    points: list of points that form the face
    label: name of the face.
    face_type: kind of face. Internal or external. External faces can be also
    boundary conditions
    """

    def __init__(self, points, label, face_type = "internal"):
        self.points = points
        self.label = label
        self.face_type = face_type
        self.bc_type = None
        self.face_center = self.calculate_face_center()
        self.normal_vector = self.calculate_normal_vector()
        self.face_length= self.calculate_face_length()
        self.owner_cells = []
        self.set_slave_points()
        
    def __str__(self):
        return "Face {0}:".format(self.label) + "".join(["\n|--->{0}".format(f) for f in self.points])
   
    def __repr__(self):
        return "Face {0}".format(self.label)
        
    def calculate_face_center(self):
        
        central_point = ( self.points[0] + self.points[1] ) / 2
        central_point.set_label("FC{0}".format(self.label))
        return central_point

    def calculate_normal_vector(self):
        dx = self.points[1].get_x() - self.points[0].get_x()
        dy = self.points[1].get_y() - self.points[0].get_y()
       
        return np.array([dy, -dx]) / mag([dy, -dx])

    def calculate_face_length(self):
        return distance_between_points(self.points[0], self.points[1])  #hacer la funcion a parte

    def get_points(self):
        return self.points
  
    def get_point_labels(self):
        return [p.get_label() for p in self.points]
          
    def get_length(self):
        return self.face_length

    def get_center(self):
        return self.face_center

    def get_label(self):
        return self.label

    def get_normal(self):
        return self.normal_vector
    
    def get_face_type(self):
        return self.face_type
    
    def set_face_type(self, face_type):
        self.face_type = face_type
        
    def set_label(self, label):
        self.label = label
        
    def add_owner_cell(self, label):
        if label not in self.owner_cells:
            self.owner_cells.append(label)
    
    def get_owner_cell(self):
        return self.owner_cells

    def set_slave_points(self):
        for p in self.points:
            p.add_owner_face(self.label)
    
    def set_boundary_condition_type(self, bc_type, bc_value):
        self.bc_type = bc_type
        self.bc_value = bc_value
        
    def set_periodic_face(self, periodic_face):
        self.periodic_face = periodic_face

    def get_periodic_face(self):
        return self.periodic_face
    
if __name__ == "__main__":
    points = [Point(x, y, label = i) for i, x, y in zip([0, 1],[0, 0],[0, 1])]
   
    face0 = Face(points, label = 0, face_type = "internal")

