"""
Modificaciones: 
    
    - Eliminar tipos de field, con el primero vale. Dentro de field crear una 
    funcion que devuelva el campo en caras o en celdas. Si se quiere hacer el 
    campo phi que sea una multiplicacion de U en caras por n y por el area de 
    la cara por ejemplo. 
    
    - Los tiempos están bien para poder almacenar el actual [0] el anterior
      [-1] y el siguiente [+1] y que se vayan actualizando. 
      
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
    
class FaceField(Field):
    
    """
    Field class and its functions.
    
    field_name: name of the field
    mesh: Mesh class which the field is refered to
    dimensions: dimensions of the variable, just informative
    """
    
    def __init__(self, field_name, mesh, data = None, dimensions = None):
        Mesh.__init__(self,mesh.get_cells(),mesh.get_faces(),mesh.get_points())
        
        self.mesh = mesh
        self.name = field_name
        self.dimensions = dimensions
        self.set_values(data, self.get_number_of_faces())
    
    def __str__(self):
        if self.dimensions:
            return "Face Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Face Field {0}".format(self.name)
    
    def __repr__(self):
        if self.dimensions:
            return "Face Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Face Field {0}".format(self.name)

    def __add__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return FaceField("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return FaceField("{0} + {1}".format(self.name, f2),
                             self.mesh, data = self.values + f2.values, 
                             dimensions = self.dimensions)
    
    def __sub__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return FaceField("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2, 
                             dimensions = self.dimensions)
        
        elif isinstance(f2, type(self)):
            return FaceField("{0} - {1}".format(self.name, f2),
                             self.mesh, data = self.values - f2.values, 
                             dimensions = self.dimensions)
    
    def __mul__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            return FaceField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            return FaceField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values * f2.values, 
                             dimensions = None)
    
    def __truediv__(self, f2):
        if isinstance(f2, float) or isinstance(f2, int):
            f2 += 1e-8
            return FaceField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2, 
                             dimensions = None)
        
        elif isinstance(f2, type(self)):
            f2 += 1e-8
            return FaceField("{0} * {1}".format(self.name, f2),
                             self.mesh, data = self.values / f2.values, 
                             dimensions = None)
    
    def set_boundary_condition(self, bc_name, bc_type, value):
        faces = self.get_faces()
        
        for i, face in enumerate(faces):
            
            if face.get_face_type() == bc_name:
                
                if bc_type.lower() == "dirichlet":
                    face.set_boundary_condition_type("dirichlet", value)
                    self.values[i] = value
                
                if bc_type.lower() == "neumann":
                    face.set_boundary_condition_type("neumann", value)
                    cell = face.get_owner_cell()
                    self.values[i] = self.cell_values[cell]
    
    def interpolate_from_cells(self, cell_field):
        check_field_lenghts(self, cell_field)
        faces = self.get_faces()
        cells = self.get_cells()
       
        for f in faces:
            if f.get_face_type().lower() == "internal":
                face_center = f.get_center()
                owners = f.get_owner_cell()
                cell_centers = [cells[l].get_center() for l in owners]
                values = [self.cell_values[l] for l in owners]
                face_value = linear_interpolation(face_center, cell_centers[0],
                                         cell_centers[1], values[0], values[1])
                
                self.values[f.get_label()] = face_value
                                
  


if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 3, yMax = 3, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,3], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([3, 3], [0,3], "Outlet")
    mesh.create_boundary_condition([0,3], [3,3], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    T = FaceField("T", mesh, dimensions = "K", data = 1)
    T2 = T * T
    print(T2.values)