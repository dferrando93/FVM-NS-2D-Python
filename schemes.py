# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:25:58 2023

@author: diego
"""
import numpy as np
from fields import *
from auxilary_functions import *

class Equation:
    
    def __init__(self):
        pass

def gradient():
    pass

def divergence():
    pass

def get_normal_vector(cell, face):
    cell_center = cell.get_center()
    face_center = face.get_center()
    
    normal_vector = np.array((face_center - cell_center).get_coordinates())
    normal_vector /= mag(normal_vector)

    for i, v in enumerate(normal_vector):
        if abs(v) < 0.01:
            normal_vector[i] = 0
        elif abs(v) > 0.99:
            normal_vector[i] = 1
    
    return normal_vector

def upwind(phi, cell_number, time):
    
    face_list = phi.get_faces()
    cell = phi.get_cells()[cell_number]
    cell_face_labels = cell.get_face_labels()
    cell_faces = cell.get_faces()
    

    normal_vectors = [get_normal_vector(cell, face) for face in cell_faces]

    data = phi[time]
    data = [data[int(f)] for f in cell_face_labels]
    phi = [np.dot(d, n) for d, n in zip(data, normal_vectors)]
    
    q = [data[i] for i, f in enumerate(cell_faces) if f.get_face_type() != "internal"]
    #d = [data[i] for i, f in enumerate(cell_faces) if f.get_face_type() == "internal"]
    
    print(q, d)
    
    


def linear():
    pass


if __name__ == "__main__":
    
    mesh = create_mesh(xMin = 0, yMin = 0, xMax = 4, yMax = 4, nx = 3, ny = 3)
    mesh.create_boundary_condition([0,10], [0,0], "Wall")
    mesh.create_boundary_condition([0,0], [0,10], "Inlet")
    mesh.create_boundary_condition([4,4], [0,10], "Outlet")
    mesh.create_boundary_condition([0,10], [4,4], "Atmosphere")
    mesh.visualize_mesh(show_points = False, show_faces=True)
    
    Uf = Vector_Face_Field("U", mesh, data0 = [2, 1])
    Uf.set_initial_condition("Wall", [0, 0])
    Uf.set_initial_condition("Inlet", [3, 0])
    Uf.set_initial_condition("Outlet", [2, 1])
    Uf.set_initial_condition("Atmosphere", [0, 3])

    upwind(Uf, 4, 0)