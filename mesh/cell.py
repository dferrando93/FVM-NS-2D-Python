import sys
sys.path.append("../functions")
from auxilary_functions import *
from face import Face
from point import Point
import numpy as np

class Cell():
    """
    Cell class used to define mesh cells
    
    faces: faces that form the cell
    label: name of the cell. 

    """

    def __init__(self, faces, label):
        self.faces = faces
        self.label = label
        self.points = self.point_list()
        self.cell_center = self.calculate_cell_center()
        self.cell_surface = self.calculate_cell_surface()
        self.set_slave_points()
        self.set_slave_faces()

    def calculate_cell_center(self):
        x = sum([p.get_x() for p in self.points]) / 4
        y = sum([p.get_y() for p in self.points]) / 4
        
        return  Point(x, y, label = "CC{0}".format(self.label))

    def calculate_cell_surface(self):
        s1 = surface_triangle(self.points[0], self.points[1], self.points[2])
        s2 = surface_triangle(self.points[0], self.points[2], self.points[3])
        return s1+s2

    def __str__(self):
        return "Cell {0}:".format(self.label) + "".join(["\n|--->{0}".format(f) for f in self.faces])
    
    def __repr__(self):
        return "Cell {0}".format(self.label) #+ "".join(["\n|--->{0}".format(f) for f in self.faces])
    
    def point_list(self): #To improve
        non_sorted_points = list(set([p for f in self.faces for p in f.get_points()]))
        sorted_points = [None for i in range(len(non_sorted_points))]
        mag_points = [(p.get_x()**2+p.get_y()**2)**0.5 for p in non_sorted_points]
        y_points = [p.get_y()for p in non_sorted_points]
        
        for i, p in enumerate(non_sorted_points):
            mag = mag_points[i]
            y = y_points[i]
            
            if mag == min(mag_points):
                sorted_points[0] = p
            elif mag == max(mag_points):
                sorted_points[2] = p
            elif y == min(y_points):
                sorted_points[1] = p
            else:
                sorted_points[3] = p
        
        return sorted_points      
        
    def get_faces(self):
        return self.faces
    
    def get_face_labels(self):
        return [f.get_label() for f in self.faces]
    
    def get_points(self):
        return self.points

    def get_surface(self):
        return self.cell_surface

    def get_center(self):
        return self.cell_center

    def get_label(self):
        return self.label
    
    def set_slave_points(self):
        for p in self.get_points():
            p.add_owner_cell(self.label)
            
    def set_slave_faces(self):
        for f in self.get_faces():
            f.add_owner_cell(self.label)
    
    
if __name__ == "__main__":
    points = [Point(x, y, label = i) for i, x, y in zip([0, 1, 2, 3], 
                                                        [0, 0, 1, 1], 
                                                        [0, 1, 0, 1])]
    
    faces = [Face([points[0], points[1]], 0),
             Face([points[0], points[2]], 1),
             Face([points[1], points[3]], 2),
             Face([points[1], points[3]], 0)]
    
    cell0 = Cell(faces, 0)