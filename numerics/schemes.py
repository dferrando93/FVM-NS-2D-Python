"""
Modificaciones a hacer:
    - Acabar clase Equation.
    
    - Crear funciones para cada scheme, conveccion, difusion, temporal, 
      gradiente.
      
     - Tener en cuenta el tipo de condicion de contorno de los fields
"""

import sys
sys.path.append("../") 
sys.path.append("../functions/")
sys.path.append("../mesh") 
sys.path.append("../field") 
import numpy as np
from fields import *
from auxilary_functions import *


class Equation:
    
    def __init__(self, A, q):
        self.A = A
        self.q = q
    
    def solve():
        pass

def get_normal_vector(cell, face):
    ## CORREGIR LA FUNCION
    
    cell_center = cell.get_center()
    face_center = face.get_center()
 
    normal_vector = np.array((face_center - cell_center).get_coordinates())
    normal_vector /= mag(normal_vector)
    return normal_vector


def get_neighbor(face, cell):
    neighbor = face.get_owner_cell()
    for c in neighbor:
        if c != cell.get_label():
            return c

def interpolate_cell(Uf_rho, cell, time, interpolation):
    
    cell_face_labels = cell.get_face_labels()
    cell_faces = cell.get_faces()
    
    normal_vectors = [get_normal_vector(cell, face) for face in cell_faces]
    phi = Uf_rho[time]
    phi = [phi[int(l)] for l in cell_face_labels]
    
    phi = [np.dot(u, n) for u, n in zip (phi, normal_vectors)]
    A = np.zeros(Uf_rho.get_number_of_cells())
    q = np.zeros(Uf_rho.get_number_of_cells())
    
    for i, f in enumerate(cell_faces):
        
        if f.get_face_type() == "internal":
            neighbor = get_neighbor(f, cell)
    
            if interpolation.lower() == "upwind":
                if phi[i] >= 0:
                    label = int(cell.get_label())
                elif phi[i] < 0:
                    label = int(neighbor)
                A[label] += phi[i]
               
            elif interpolation.lower() == "linear":
                cell_distance = distance_between_points(cell.get_center(), f.get_center())
                neighbor_cell = Uf_rho.get_cells()[neighbor]
                neighbor_distance = distance_between_points(neighbor_cell.get_center(), f.get_center())
          
            
                A[int(cell.get_label())] += phi[i] * cell_distance
                A[int(neighbor_cell.get_label())] += phi[i] *neighbor_distance
                
        else:
            q[int(cell.get_label())] += phi[i]
    
    return A, q
        
def interpolate_convection(Uf_rho, time, interpolation):

    A = np.zeros((Uf_rho.get_number_of_cells(), Uf_rho.get_number_of_cells()))
    q = np.zeros(Uf_rho.get_number_of_cells())
    
    for cell in Uf_rho.get_cells():
        label = int(cell.get_label())
        A_cell, q_cell = interpolate_cell(Uf_rho, cell, time, interpolation)
        A[label] = A_cell
        q += q_cell
    
    return Equation(A, q)

# Revisar
def cell_gradient(field, cell, time):
    field = field[time]
    faces = cell.get_faces()
    face_centers = [f.get_center() for f in faces]
    cell_center = cell.get_center()
    center_distance = [distance_between_points(cell_center, face_center)
                       for face_center in face_centers]
    
    total_distance = sum(center_distance)
    grad = sum([field[int(f.get_label())] * d / total_distance for f, d in
                    zip(faces, center_distance)])
    
    return grad

def gradient(field, time):
    if field.field_type == "face_field":
        new_field = np.array([cell_gradient(field, cell, time) for cell
                              in field.get_cells()])
        
   
        if field.variable_type == "scalar":
            return Scalar_Cell_Field("grad({0})".format(field.get_field_name()),
                                     field, time0 = time, data0 = new_field)
        elif field.variable_type == "vector":
            return Vector_Cell_Field("grad({0})".format(field.get_field_name()),
                                     field, time0 = time, data0 = new_field)
        
    elif field.variable_type == "vector_field":
        pass
    
def delta_time_euler(field0, deltaT, equation):
    
    A = -1*equation.A * deltaT
    q = field0 + equation.q
    return Equation(A, q)

if __name__ == "__main__":
    
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 10, yMax = 1, nx = 10, ny = 1)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([10, 10], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    T = Field("T", mesh)
    T.set_cell_values([0,1,1,0,0,0,0,0,0,0])
    #T.interpolate_from_cells()
    
    T.set_initial_condition("Wall", "neumann", 0)
    T.set_initial_condition("Inlet", "neumann",0)
    T.set_initial_condition("Outlet", "neumann",0)
    T.set_initial_condition("Atmosphere", "neumann",0)

    U = Field("U", mesh)
    U.set_cell_values(1)
    U.set_initial_condition("Wall", "neumann", 0)
    U.set_initial_condition("Inlet", "neumann",0)
    U.set_initial_condition("Outlet", "neumann",0)
    U.set_initial_condition("Atmosphere", "neumann",0)
    
    eq = interpolate_convection()