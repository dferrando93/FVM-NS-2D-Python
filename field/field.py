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
from mesh import Mesh, create_mesh
import numpy as np


    
class Field(Mesh):
    
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
    
    def get_field_name(self):
        return self.name
    
    def get_dimensions(self):
        return self.dimensions
       
    def get_mesh(self):
        return self.mesh
    
           
    def set_values(self, data, number_of_elements):
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if len(data) == number_of_elements:
                self.values = np.array(data).astype(float)
            else:
                print("Data range different from number of cells")
                print("Cell values not set")
        
        elif isinstance(data, float) or isinstance(data, int):
            self.values = np.array([float(data) for i in range(number_of_elements)])     
    
    def __str__(self):
        if self.dimensions:
            return "Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Field {0}".format(self.name)
   
    def __repr__(self):
        if self.dimensions:
            return "Field {0} [{1}]".format(self.name, self.dimensions)
        else:
            return "Field {0}".format(self.name)
        
    
    


if __name__ == "__main__":
    
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 3, yMax = 3, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,3], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([3, 3], [0,3], "Outlet")
    mesh.create_boundary_condition([0,3], [3,3], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    T = Field("T", mesh, dimensions = "K")
    print(T)

    