
grid_lenght = 64

all_grids = []

class point:
    def __init__ (self,x,y):
        self.x = x
        self.y = y

class edge:
    def __init__ (self, p1 , p2):
        self.p1 = p1
        self.p2 = p2

class grid:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

        self.p1 = point( x     * grid_lenght, y     * grid_lenght)
        self.p2 = point( (x+1) * grid_lenght, y     * grid_lenght)
        self.p3 = point( (x+1) * grid_lenght, (y+1) * grid_lenght)
        self.p4 = point( x     * grid_lenght, (y+1) * grid_lenght)
        self.e12 = edge(p1, p2)
        self.e23 = edge(p2, p3)
        self.e34 = edge(p3, p4)
        self.e41 = edge(p4, p1)

        self.base_color = 0            ######## 0 is white  ####### 1 is gray  ######## 2 is black
        self.is_in_cycle = False

        self.is_yellow = False
        
        self.is_blue_1 = False
        self.is_blue_2 = False
        self.is_blue_3 = False
        
        self.is_magenta_1 = False
        self.is_magenta_2 = False
        self.is_magenta_3 = False
        
        self.is_in_q = False
        self.is_corner = False
        self.has_circle = -1            ####### 0 is white  ###### 1 is black  ####### -1 is none
        self.is_red = False

class board:
    def __init__(self, n, m):
        self.m = m
        self.n = n
        all_grids = [[grid(i,j) for i in range(m)] for j in range(n)]

        ####################### coloring the base 
        for i in range(m):
            for j in range(n):
                if i %2 ==1:
                    if j%2 ==1:
                        all_grids[i][j].base_color = 2
                    else:
                        all_grids[i][j].base_color = 1
                else:
                    if j%2 ==1:
                        all_grids[i][j].base_color = 1
                    else:
                        all_grids[i][j].base_color = 0








###### inputs
p1 = point(1,0)
p2 = point(2,0)
p3 = point(2,1)
p4 = point(3,1)
p5 = point(3,2)
p6 = point(3,3)
p7 = point(2,3)
p8 = point(2,2)
p9 = point(1,2)
p10 = point(1,3)
p11 = point(1,4)
p12 = point(0,4)
p13 = point(0,3)
p14 = point(0,2)
p15 = point(0,1)
p16 = point(1,1)

border_list = [edge(p7,p8), edge(p3,p4), edge(p1,p2), edge(p4,p5), edge(p16,p1), edge(p5,p6), edge(p3,p2), edge(p7,p6), edge(p14,p13), 
edge(p12,p13), edge(p9,p8), edge(p14,p15),edge(p9,p10), edge(p10,p11), edge(p16,p15), edge(p11,p12)]
