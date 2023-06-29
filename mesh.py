"""
Mesh classes and utilities. 
- Classes defined:
    - Point()
    - Face()
    - Cell()
    - Mesh()
    
- Functions defined:
    - createMesh()
"""

"""
Modificaciones a hacer:
    
    - Crear condicion de contorno periodic.
"""

import auxilary_functions as af
import numpy as np
import matplotlib.pyplot as plt

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
       
        return np.array([dy, -dx]) / af.mag([dy, -dx])

    def calculate_face_length(self):
        return af.distance_between_points(self.points[0], self.points[1])  #hacer la funcion a parte

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
        s1 = af.surface_triangle(self.points[0], self.points[1], self.points[2])
        s2 = af.surface_triangle(self.points[0], self.points[2], self.points[3])
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
    


class Mesh:
    """
    Mesh class
    
    cells: list of cells
    faces: list of faces
    points: list of points
    """
    
    def __init__(self,  cells, faces, points):
        self.cells = cells
        self.faces = faces
        self.points = points
        self.nCells = len(cells)
        self.nFaces = len(faces)
        self.nPoints = len(points)
        self.xMin = self.__xMin()
        self.xMax = self.__xMax()
        self.yMin = self.__yMin()
        self.yMax = self.__yMax()
    
    def __repr__(self):
        text = "Mesh with {0} cells.\nLimiting points:".format(self.nCells)
        text += "\n\t Lower left: {0}".format(Point(self.xMin, self.yMin, "MPmin"))
        text += "\n\t Upper rigth: {0}".format(Point(self.xMax, self.yMax, "MPmax"))
        return text
    
    def __str__(self):
        text = "Mesh with {0} cells.\nLimiting points:".format(self.nCells)
        text += "\n\t Lower left: {0}".format(Point(self.xMin, self.yMin, "MPmin"))
        text += "\n\t Upper rigth: {0}".format(Point(self.xMax, self.yMax, "MPmax"))
        return text
    
    
    def get_cells(self):
        return self.cells
    
    def get_faces(self):
        return self.faces
    
    def get_points(self):
        return self.points
    
    def get_number_of_cells(self):
        return self.nCells
    
    def get_number_of_faces(self):
        return self.nFaces
    
    def get_number_of_points(self):
        return self.nPoints
    
    def __xMin(self):
        return min([p.get_x() for p in self.points])
    
    def __xMax(self):
        return max([p.get_x() for p in self.points])
    
    def __yMin(self):
        return min([p.get_y() for p in self.points])
    
    def __yMax(self):
        return max([p.get_y() for p in self.points])
    
    def get_xMin(self):
        return self.xMin
    
    def get_xMax(self):
        return self.xMax
    
    def set_boundary_condition(self, labels, bc_name):
        for f in self.faces:
            if f.get_label() in labels:
                f.set_face_type(bc_name)     

    
    def get_yMin(self):
        return self.yMin
    
    def get_yMax(self):
        return self.yMax

    def create_boundary_condition(self, list_x, list_y, bc_name):
        faces = self.get_faces()
        labels = [f.get_label() for f in faces if 
                 (f.get_center().get_x() >= list_x[0] and 
                  f.get_center().get_x() <= list_x[1] and
                  f.get_center().get_y() >= list_y[0] and 
                  f.get_center().get_y() <= list_y[1] 
                  )]
        self.set_boundary_condition(labels, bc_name)
    
    def set_periodic_patch(self, patch1, patch2):
        
        faces_1 = [f for f in self.get_faces() if f.get_face_type() == patch1]
        faces_2 = [f for f in self.get_faces() if f.get_face_type() == patch2]
        
        if len(faces_1) != len(faces_2):
            raise("Patch {0} and patch {1} has different number of faces".format(
                   patch1, patch2))
        
        for f1, f2 in zip(faces_1, faces_2):
            f1.set_periodic_face(f2.get_label())
            f1.set_face_type("periodic")
            f2.set_periodic_face(f1.get_label())
            f2.set_face_type("periodic")
                
    def visualize_mesh(self, show_points = False, show_faces = False):
        fig = plt.figure()
        for p in self.points:
            plt.scatter(p.get_x(), p.get_y(), c = "black")
            
            if show_points:
                plt.text(p.get_x(), p.get_y(), p.get_label(), c = "black",
                         ha = "left", va = "bottom")
        
        for f in self.faces:
            p1 = f.get_points()[0]
            p2 = f.get_points()[1]
            face_type = f.get_face_type()
            
            if face_type.lower() == "internal":
                color = "black"  
            elif face_type.lower() == "inlet":
                color = "green"
            elif face_type.lower() == "outlet":
                color = "red"
            elif face_type.lower() == "wall":
                color = "brown"    
            elif face_type.lower() == "periodic":
                color = "blue"
            else:
                color = "grey"
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c = color)
            
            if show_faces:
                fc = f.get_center()
                plt.text(fc[0], fc[1], f.get_label(), c = color,
                         ha = "left", va = "bottom")
        
        for c in self.cells:
            pc = c.get_center()
            plt.text(pc.get_x(), pc.get_y(), c.get_label(), c = "blue" ,
                     ha = "center", va = "center")
        
        plt.show()


def create_mesh(xMin, yMin, xMax, yMax, nx, ny):
    
    """
    Mesh generator. Create a structured isotropic grid.
    
    xMin, yMin, xMax, yMax: Coordinates to define mesh boundaries
    nx, ny: Number of elements in the axis x and y
    
    return: A Mesh class
    """
    
    dx = abs(xMax - xMin) / nx
    dy = abs(yMax - yMin) / ny
    
    x = [dx * i for i in range(nx + 1)]
    y = [dy * i for i in range(ny + 1)]
    
    points = np.array([Point(xi, yi, i+j*(nx+1)) 
                       for j, yi in enumerate(y) for i, xi in enumerate(x)])
    points = points.reshape(ny + 1, nx + 1)
    
    faces_H = np.array([Face([points[i,j], points[i, j+1]], j+i*nx)
                       for i in range(ny+1) for j in range(nx)])
    faces_H = faces_H.reshape(ny +1 , nx)

    faces_V = np.array([Face([points[i,j], points[i + 1, j]], 
                      faces_H[-1,-1].get_label() + j + i*(nx+1) + 1)
                       for i in range(ny) for j in range(nx+1)])
    faces_V = faces_V.reshape(ny, nx + 1)
        
    cells = np.array([Cell([faces_H[i, j], faces_H[i + 1, j], 
                            faces_V[i, j], faces_V[i, j+1]],
                            j + nx*i)
                      for i in range(ny) for j in range(nx)])
    
    faces = [f for l in faces_H for f in l] + [f for l in faces_V for f in l]
    points = [p for l in points for p in l]
    
    return Mesh(cells, faces, points)
   
    
if __name__ == "__main__":
    
    
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 4, yMax = 4, nx = 3, ny = 4)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([4,4], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.set_periodic_patch("Inlet", "Outlet")
    mesh.visualize_mesh(show_points = False, show_faces=True)
