"""
Axilary functions that are used in any part of the code

- Functions defined:
    - distance_between_points()
    -surface_triangle()
    -mag():
"""


def distance_between_points(p1, p2):
    
    """
    Given 2 points objets it returns the distance between them
    """
    
    x1 = p1.get_x()
    y1 = p1.get_y()
    x2 = p2.get_x()
    y2 = p2.get_y()
    return ((x2-x1)**2+(y2-y1)**2)**0.5
    
def surface_triangle(p1, p2 ,p3):
    
    """
    Given 3 point objets it returns the surface of the formed triangle
    """
    
    x1 = p1.get_x()
    y1 = p1.get_y()
    x2 = p2.get_x()
    y2 = p2.get_y()
    x3 = p3.get_x()
    y3 = p3.get_y()

    return abs((x1*y2+x2*y3+x3*y1-y1*x2-y2*x3-y3*x1)/2)

def mag(v):
    
    """
    Returns the magnitude of a vector
    """
    
    return (v[0]**2+v[1]**2)**0.5