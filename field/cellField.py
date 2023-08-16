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
from fieldFunctions import *

    
class Cell_Field(Field):
    
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
            return Cell_Field("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return Cell_Field("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2.values, 
                             dimensions = self.dimensions)
    
    def __sub__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return Cell_Field("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return Cell_Field("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2.values, 
                             dimensions = self.dimensions)
    
    def __mul__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return Cell_Field("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            return Cell_Field("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2.values, 
                             dimensions = None)
    
    def __truediv__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            f2 += 1e-8
            return Cell_Field("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            f2 += 1e-8
            return Cell_Field("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2.values, 
                             dimensions = None)
    
    def interpolate_from_faces(self, face_field):
        check_field_lenghts(self, face_field)
        faces = self.get_faces()
        cells = self.get_cells()
       
        for c in cells:
            cell_faces_labels = c.get_face_labels()
            face_centers = [faces[l].get_center() for l in cell_faces_labels]
            face_values = [face_field.values[l] for l in cell_faces_labels]
            cell_value = linear_cell_interpolation(c, face_centers, face_values)
            self.values[c.get_label()] = cell_value


if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 5, yMax = 1, nx = 5, ny = 1)
    mesh.create_boundary_condition([0,5], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,1], "Inlet")
    mesh.create_boundary_condition([5, 5], [0,1], "Outlet")
    mesh.create_boundary_condition([0,5], [1,1], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    #Ux = Face_Field("Ux", mesh, dimensions = "m/s", data = [-1, -1, 0, -1, -1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1])
    Vx = Cell_Field("Ux", mesh, dimensions = "m/s", data = 0)
    #Vx.interpolate_from_faces(Ux)

    