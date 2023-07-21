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
from mesh import Mesh, create_mesh
from auxilary_functions import *

    
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
        self.cell_values = np.array([0 for i in range(self.get_number_of_cells())])
        self.face_values = np.array([0 for i in range(self.get_number_of_faces())])
    
    def get_field_name(self):
        return self.name
    
    def get_dimensions(self):
        return self.dimensions
    
    def get_cell_values(self):
        return self.cell_values
    
    def get_face_values(self):
        return self.face_values
    
    def get_mesh(self):
        return self.mesh
    
    def set_cell_values(self, data):
        
        nCells = self.get_number_of_cells()
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if len(data) == nCells:
                self.cell_values = np.array(data)
            else:
                print("Data range different from number of cells")
                print("Cell values not set")
        
        elif isinstance(data, float) or isinstance(data, int):
            self.cell_values = np.array([data for i in range(nCells)])      
    
    def set_face_values(self, data):
        
        nFaces = self.get_number_of_faces()
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if len(data) == nFaces:
                self.face_values = np.array(data)
            else:
                print("Data range different from number of faces")
                print("Face values not set")
        
        elif isinstance(data, float) or isinstance(data, int):
            self.face_values(np.array([data for i in range(nFaces)])) 
    
    def set_initial_condition(self, bc_name, bc_type, value):
        faces = self.get_faces()
        
        for i, face in enumerate(faces):
            
            if face.get_face_type() == bc_name:
                
                if bc_type.lower() == "dirichlet":
                    face.set_boundary_condition_type("dirichlet", value)
                    self.face_values[i] = value
                
                if bc_type.lower() == "neumann":
                    "NO TERMINADA"
                    face.set_boundary_condition_type("neumann", value)
                    cell = face.get_owner_cell()
                    self.face_values[i] = self.cell_values[cell]
                    
    def interpolate_from_cells(self):
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
                
                self.face_values[f.get_label()] = face_value
                
    def interpolate_from_faces(self):
        faces = self.get_faces()
        cells = self.get_cells()
       
        for c in cells:
            cell_faces_labels = c.get_face_labels()
            face_centers = [faces[l].get_center() for l in cell_faces_labels]
            face_values = [self.face_values[l] for l in cell_faces_labels]
            cell_value = linear_cell_interpolation(c, face_centers, face_values)
            
            self.cell_values[c.get_label()] = cell_value
                

def linear_interpolation(p0, p1, p2, v1, v2):
    delta_x1 = distance_between_points(p0, p1)
    delta_x2 = distance_between_points(p0, p2)
    delta_xt = delta_x1 + delta_x2
    return (v1 * delta_x1 + v2 * delta_x2)/delta_xt

def linear_cell_interpolation(cell, face_centers, face_values):
    cell_center = cell.get_center()
    cell_value = 0
    distance_to_cell = [distance_between_points(cell_center, fc) for
                        fc in face_centers]
    
    total_distance = sum(distance_to_cell)
    
    for i, fv in enumerate(face_values):
        cell_value += fv * distance_to_cell[i] / total_distance
    
    return cell_value


def check_field_lenghts(f1, f2):
    if f1.get_number_of_cells() == f2.get_number_of_cells():
        pass
    else: 
        exception = "Field: {0} and field {1} do not have the same number of cells"
        exception = exception.format(f1.get_field_name(), f2.get_field_name())
        
        raise Exception(exception)  

def field_operation(f1, f2, new_name, operation, field_type = "cells"):
    
    check_field_lenghts(f1, f2)
    
    def choose_operation(data1, data2):
        if operation == "+":
            return data1 + data2
        elif operation == "-":
            return data1 - data2
        elif operation == "*":
            return data1 * data2
        elif operation == "/":
            return data1 / data2

    mesh = f1.get_mesh()
    new_field = Field(new_name, mesh)
    
    if field_type == "cells":
        f1_data = f1.get_cell_values()
        f2_data = f2.get_cell_values()
        data = choose_operation(f1_data, f2_data)
        new_field.set_cell_values(data)
        
    elif field_type== "faces":
        f1_data = f1.get_face_values()
        f2_data = f2.get_face_values()
        data = choose_operation(f1_data, f2_data)
        new_field.set_face_values(data)
        
    return new_field




if __name__ == "__main__":
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 10, yMax = 1, nx = 10, ny = 1)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([10, 10], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    T = Field("T", mesh)
    T.set_cell_values([0,1,1,0,0,0,0,0,0])
    T.interpolate_from_cells()
    
    """
    Ux = Field("U", mesh)
    Ux.set_cell_values([2,4,6,2,4,6,2,4,6])
    Ux.interpolate_from_cells()
    
    U2 = Field("U2", mesh)
    U2.set_cell_values([2,5,0,1,4,8,3,4,5])
    
    U3 = field_operation(Ux, U2, "U_new", "+",field_type = "faces")
    U3.interpolate_from_faces()
    print(U3.get_cell_values())
    """
    