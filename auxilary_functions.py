def distance_between_points(p1, p2):
    x1 = p1.get_x()
    y1 = p1.get_y()
    x2 = p2.get_x()
    y2 = p2.get_y()
    return ((x2-x1)**2+(y2-y1)**2)**0.5
    
def surface_triangle(p1, p2 ,p3):
    x1 = p1.get_x()
    y1 = p1.get_y()
    x2 = p2.get_x()
    y2 = p2.get_y()
    x3 = p3.get_x()
    y3 = p3.get_y()

    return abs((x1*y2+x2*y3+x3*y1-y1*x2-y2*x3-y3*x1)/2)

def mag(v):
    return (v[0]**2+v[1]**2)**0.5