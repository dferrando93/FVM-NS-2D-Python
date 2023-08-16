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


if __name__ == "__main__":
    pass
    