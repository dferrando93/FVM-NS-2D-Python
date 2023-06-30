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
sys.path.append("..") 
import numpy as np
from mesh.mesh import Mesh, create_mesh
from mesh.face import Face
from mesh.point import Point
from mesh.cell import Cell

    
class Field(Mesh):
    
    """
    Field class and its functions.
    
    field_name: name of the field
    mesh: Mesh class which the field is refered to
    dimensions: dimensions of the variable, just informative
    """
    
    def __init__(self, field_name, mesh, data = None, dimensions = None):
        Mesh.__init__(self,mesh.get_cells(),mesh.get_faces(),mesh.get_points())
        
        self.dimensions = dimensions
    
    def get_field_name(self):
        return self.name
    
    def get_dimensions(self):
        return self.dimensions
    
    def get_cell_values(self):
        
        if self.cell_values:
            return self.cell_values
        else:
            pass
            #return interpolate_from_faces(self)
    
    def get_face_values(self):
        
        if self.face_values:
            return self.face_values
        else:
            pass
            #return interpolate_from_cells(self)
    
    def set_cell_values(self, data):
        
        nCells = self.get_number_of_cells()
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if len(data) == nCells:
                self.cell_values = data
            else:
                print("Data range different from number of cells")
                print("Cell values not set")
        
        elif isinstance(data, float) or isinstance(data, int):
            self.cell_values(np.array([data for i in range(nCells)]))      
    
    def set_face_values(self, data):
        
        nFaces = self.get_number_of_faces()
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if len(data) == nFaces:
                self.face_values = data
            else:
                print("Data range different from number of faces")
                print("Face values not set")
        
        elif isinstance(data, float) or isinstance(data, int):
            self.face_values(np.array([data for i in range(nFaces)])) 
    
    def set_initial_conditions(self, bc_name, bc_type, value):
        faces = self.get_faces()
        
        for i, face in enumerate(faces):
            
            if face.get_face_type() == bc_name:
                
                if bc_type.lower() == "dirichlet":
                    face.set_boundary_condition_type("dirichlet", value)
                    self.face_values[i] = value
                
                if bc_type.lower() == "neumann":
                    "NO TERMINADA"
                    face.set_boundary_condition_type("neumann", value)
                    self.face_values[i] = 0      
    
    def __add__(self, field2, time):
        pass
    
    def __sub__(self, field2, time):
        pass
    
    def __mul__(self, field2, time):
        pass
    
    def __truediv__(self, field2, time):
        pass
        


if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 4, yMax = 4, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([4,4], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)

    
    