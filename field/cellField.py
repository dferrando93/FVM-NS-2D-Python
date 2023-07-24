"""
Modificaciones: 
    
    - Eliminar tipos de field, con el primero vale. Dentro de field crear una 
    funcion que devuelva el campo en caras o en celdas. Si se quiere hacer el 
    campo phi que sea una multiplicacion de U en caras por n y por el area de 
    la cara por ejemplo. 
         
    - Crear las condiciones de contorno bien hechas de Neumann y Dirichlet
    
    - Crear suma, resta, division y multiplicacion de campos
    
    - Crear una funcion que hace el producto vectorial dados 2 campos dando
      las direcciones dos a dos

"""
import sys
sys.path.append("../") 
sys.path.append("../functions/")
sys.path.append("../mesh") 
import numpy as np
from field import Field
from mesh import Mesh, create_mesh
from auxilary_functions import *

    
class CellField(Field):
    
    """
    """
    
    def __init__(self, field_name, mesh, data = 0, dimensions = None):
        Mesh.__init__(self,mesh.get_cells(),mesh.get_faces(),mesh.get_points())
        
        self.mesh = mesh
        self.name = field_name
        self.dimensions = dimensions
        self.set_values(data, self.get_number_of_cells())
    
    def __str__(self):
        if self.dimensions:
            return "Cell Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Cell Field {0}".format(self.name)
    
    def __repr__(self):
        if self.dimensions:
            return "Cell Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Cell Field {0}".format(self.name)

    def __add__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return CellField("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return CellField("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2.values, 
                             dimensions = self.dimensions)
    
    def __sub__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return CellField("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return CellField("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2.values, 
                             dimensions = self.dimensions)
    
    def __mul__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return CellField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            return CellField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2.values, 
                             dimensions = None)
    
    def __truediv__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            f2 += 1e-8
            return CellField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            f2 += 1e-8
            return CellField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2.values, 
                             dimensions = None)
    def interpolate_from_faces(self, face_field):
        check_field_lenghts(self, cell_field)
        faces = self.get_faces()
        cells = self.get_cells()
       
        for c in cells:
            cell_faces_labels = c.get_face_labels()
            face_centers = [faces[l].get_center() for l in cell_faces_labels]
            face_values = [self.face_values[l] for l in cell_faces_labels]
            cell_value = linear_cell_interpolation(c, face_centers, face_values)
            
            self.values[c.get_label()] = cell_value




if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 3, yMax = 3, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,3], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([3, 3], [0,3], "Outlet")
    mesh.create_boundary_condition([0,3], [3,3], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    T = CellField("T", mesh, dimensions = "K", data = 1)
    T2 = T * T
    print(T2.values)