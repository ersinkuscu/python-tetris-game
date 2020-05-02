class Shape:
    def __init__(self):
        self.shapes = []
        self.shapes.append(self.set_t_shape())
        self.shapes.append(self.set_i_shape())
        self.shapes.append(self.set_l_shape())
        self.shapes.append(self.set_b_shape())
        self.shapes.append(self.set_z_shape())
        self.shapes.append(self.set_x_shape())
        
        self.shapes_len = []
        for i in range(len(self.shapes)):
            self.shapes_len.append(len(self.shapes[i]))
        
    def set_t_shape(self):
        shape = []
        shape.append([[0, 0], [0, 1], [0, 2], [-1, 1]])
        shape.append([[0, 0], [-1, 1], [0, 1], [1, 1]])
        shape.append([[0, 0], [0, 1], [0, 2], [1, 1]])
        shape.append([[0, 2], [-1, 1], [0, 1], [1, 1]])
        return shape
    
    def set_i_shape(self):
        shape = []
        shape.append([[0, 0], [1, 0], [2, 0], [3, 0]])
        shape.append([[1, 1], [1, 0], [1, -1], [1, -2]])
        return shape
    
    def set_l_shape(self):
        shape = []
        shape.append([[0, 0], [1, 0], [2, 0], [2, 1]])
        shape.append([[1, -1], [1, 0], [1, 1], [0, 1]])
        shape.append([[0, 0], [1, 0], [2, 0], [0, -1]])
        shape.append([[2, -1], [1, -1], [1, 0], [1, 1]])
        return shape
    
    def set_b_shape(self):
        shape = []
        shape.append([[0, 0], [0, 1], [1, 0], [1, 1]])
        return shape
    
    def set_z_shape(self):
        shape = []
        shape.append([[0, 0], [0, 1], [1, 1], [1, 2]])
        shape.append([[0, 1], [1, 1], [0, 2], [-1, 2]])
        return shape
    
    def set_x_shape(self):
        shape = []
        temp = []
        for x in range(18):
            temp.append([0, x])
        
        for x in range(18):
            temp.append([1, x])
        shape.append(temp)
        return shape
    
    def get_t_shape(self, ind: int):
        return self.shapes[0][ind]
    
    def get_i_shape(self, ind: int):
        return self.shapes[1][ind]
    
    def get_b_shape(self, ind: int):
        return self.shapes[2][ind]
    
    def get_l_shape(self, ind: int):
        return self.shapes[3][ind]
    
    def get_z_shape(self, ind: int):
        return self.shapes[4][ind]
    
    def get_shape(self, ind: int, sel: int):
        shape = self.shapes[ind][sel]
        length = self.shapes_len[ind]
        
        min_ver = [100, 100]
        max_ver = [0, 0]
        max_hor = [0, 0]
        for pos in shape:
            if min_ver[1] > pos[1]:
                min_ver = pos
            
            if max_ver[1] < pos[1]:
                max_ver = pos
            
            if max_hor[0] < pos[0]:
                max_hor = pos
        
        return {'shape': shape,
                'len': length,
                'min_ver': min_ver,
                'max_ver': max_ver,
                'max_hor': max_hor}
