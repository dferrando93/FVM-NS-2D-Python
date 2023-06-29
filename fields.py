"""
Field classes and utilities. 
- Classes defined:
    - Time()
    - Field(Mesh, Time)
    - Face_Field(Field)
    - Cell_Field(Field)
    - Scalar_Face_Field(Field)
    - Vector_Face_Field(Field)
    - Scalar_Cell_Field(Field)
    - Vector_Cell_Field(Field)
    
- Functions defined:
    - createMesh()
"""
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

import numpy as np
from mesh import Mesh
from mesh import create_mesh

class Time:
    
    """
    Time class. It creates two empty lists, one for time label and the other 
    for the data on that time
    """
    
    def __init__(self):
        self.time = []
        self.data = []
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        
        elif isinstance(key, str):
            return self.data[self.time.index(key)]
    
    def add_time(self, time, data):
        self.time.append(time)
        self.data.append(data)  
 
    
class Field(Mesh, Time):
    
    """
    Field class and its functions.
    
    field_name: name of the field
    mesh: Mesh class which the field is refered to
    dimensions: dimensions of the variable, just informative
    """
    
    def __init__(self, field_name, mesh, dimensions = None):
        Mesh.__init__(self,mesh.get_cells(),mesh.get_faces(),mesh.get_points())
        Time.__init__(self)
        
        self.name = field_name
       # self.type = "scalar"
        self.dimensions = dimensions
    
    def get_field_name(self):
        return self.name
    
    def get_field_type(self):
        return self.type
    
    def get_dimensions(self):
        return self.dimensions
    
    def add_new_time(self, time, data):
    
        if self.variable_type == "scalar":
            if isinstance(data, list) or isinstance(data, np.ndarray):
                self.add_time(time, np.array(data))
            
            elif isinstance(data, float) or isinstance(data, int):
                self.add_time(time, np.array([data for i in range(self.nData)]))
            
            else:
                self.add_time(time, np.array([data for i in range(self.nData)]))
                
        if self.variable_type == "vector":
            if isinstance(data[0], list) or isinstance(data[0], np.ndarray):
                self.add_time(time, np.array(data))
            
            elif isinstance(data[0], float) or isinstance(data[0], int):
                self.add_time(time, np.array([data for i in range(self.nData)]))
            
            else:
                self.add_time(time, np.array([data for i in range(self.nData)]))
    
    def __add__(self, field2, time):
        return self[time] + field2[time]
    
    def __sub__(self, field2, time):
        return self[time] - field2[time]
    
    def __mul__(self, field2, time):
        return self[time] * field2[time]
    
    def __truediv__(self, field2, time):
        return self[time] / field2[time]
    
class Face_Field(Field):
    
    """
    Face_Field class. The values are stored in the mesh faces
    
    time0 = label of the first time
    data0 = data of time0
    """
    
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        Field.__init__(self, field_name, mesh)
        self.nData = self.nFaces
        if data0:
            self.add_new_time(time0, data0)
            
    def __repr__(self):    
        text = "Face Field: {0} ({1})".format(self.name, self.variable_type)
        text += "\nTimes:" + ",".join([" {0:.2f}s".format(float(t)) for t in self.time])
        return text
    
    def set_initial_condition(self, bc_name, bc_type, value):
        
        faces = self.get_faces()
        data = self[0]
        for i, face in enumerate(faces):
            
            if face.get_face_type() == bc_name:
                
                if bc_type.lower() == "dirichlet":
                    face.set_boundary_condition_type("dirichlet", value)
                    data[i] = value
                
                if bc_type.lower() == "neumann":
                    face.set_boundary_condition_type("dirichlet", value)
                    data[i] = 0

    
class Cell_Field(Field):
    
    """
    Cell_Field class. The values are stored in the mesh cells
    
    time0 = label of the first time
    data0 = data of time0
    """
    
    
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        Field.__init__(self, field_name, mesh)
        self.nData = self.nCells
        if data0:
            self.add_new_time(time0, data0)
    
    def __repr__(self):    
        text = "Cell Field: {0} ({1})".format(self.name, self.variable_type)
        text += "\nTimes:" + ",".join([" {0:.2f}s".format(float(t)) for t in self.time])
        return text
    
    
def dot(self, field2, time):
    return np.array([np.dot(f1, f2) for f1, f2 in zip(self[time], field2[time])])


class Scalar_Face_Field(Face_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.variable_type = "scalar"
        self.field_type = "face_field"
        Face_Field.__init__(self, field_name, mesh, time0, data0)

class Vector_Face_Field(Face_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.variable_type = "vector"
        self.field_type = "face_field"
        Face_Field.__init__(self, field_name, mesh, time0, data0)

class Scalar_Cell_Field(Cell_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.field_type = "cell_field"
        self.variable_type = "scalar"
        Cell_Field.__init__(self, field_name, mesh, time0, data0)

class Vector_Cell_Field(Cell_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.variable_type = "vector"
        self.field_type = "cell_field"
        Cell_Field.__init__(self, field_name, mesh, time0, data0)


if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 4, yMax = 4, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([4,4], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    Uf = Vector_Face_Field("U", mesh, data0 = [2, 1])
    Uf.add_new_time("2", [1,0])
    Uf.set_initial_condition("Wall", [0, 0])
    Uf.set_initial_condition("Inlet", [3, 0])
    Uf.set_initial_condition("Outlet", [2, 1])
    Uf.set_initial_condition("Atmosphere", [0, 3])

    
    