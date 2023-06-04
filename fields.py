# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:40:13 2023

@author: diego
"""
import numpy as np
from mesh import Mesh
from mesh import create_mesh

class Time:
    
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
    
        if self.type == "scalar":
            if isinstance(data, list) or isinstance(data, np.ndarray):
                self.add_time(time, np.array(data))
            
            elif isinstance(data, float) or isinstance(data, int):
                self.add_time(time, np.array([data for i in range(self.nData)]))
            
            else:
                self.add_time(time, np.array([data for i in range(self.nData)]))
                
        if self.type == "vector":
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
    
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        Field.__init__(self, field_name, mesh)
        self.nData = self.nFaces
        if data0:
            self.add_new_time(time0, data0)
            
    def __repr__(self):    
        text = "Face Field: {0} ({1})".format(self.name, self.type)
        text += "\nTimes:" + ",".join([" {0:.2f}s".format(float(t)) for t in self.time])
        return text
    
    def set_initial_condition(self, bc_name, value):
        faces = self.get_faces()
        data = self[0]
        
        for i, d in enumerate(data):
            
            if faces[i].get_face_type() == bc_name:
                
                data[i] = value
    
class Cell_Field(Field):
    
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        Field.__init__(self, field_name, mesh)
        self.nData = self.nCells
        if data0:
            self.add_new_time(time0, data0)
    
    def __repr__(self):    
        text = "Cell Field: {0} ({1})".format(self.name, self.type)
        text += "\nTimes:" + ",".join([" {0:.2f}s".format(float(t)) for t in self.time])
        return text
    
def dot(self, field2, time):
    return np.array([np.dot(f1, f2) for f1, f2 in zip(self[time], field2[time])])


class Scalar_Face_Field(Face_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.type = "scalar"
        Face_Field.__init__(self, field_name, mesh, time0, data0)

class Vector_Face_Field(Face_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.type = "vector"
        Face_Field.__init__(self, field_name, mesh, time0, data0)

class Scalar_Cell_Field(Cell_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.type = "scalar"
        Cell_Field.__init__(self, field_name, mesh, time0, data0)

class Vector_Cell_Field(Cell_Field):
    def __init__(self, field_name, mesh, time0 = "0", data0 = None):
        self.type = "vector"
        Cell_Field.__init__(self, field_name, mesh, time0, data0)


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

    
    