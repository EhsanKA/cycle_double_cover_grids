
grid_lenght = 64

all_grids = []

class point:
    def __init__ (self,x,y):
        self.x = x
        self.y = y
        
    def is_equal(self,p):
        if self.x == p.x and self.y == p.y:
            return 1
        else:
            return 0

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
        self.is_in_cycle_border = False
        self.cycle_connectivity_num = 0

        self.is_yellow = False
        
        self.is_blue_1 = False
        self.is_blue_2 = False
        self.is_blue_3 = False
        self.is_blue_border = False
        
        self.is_magenta_1 = False
        self.is_magenta_2 = False
        self.is_magenta_3 = False
        
        self.is_in_q = False
        self.is_in_q_border = False
        self.is_corner = False
        self.has_circle = -1            ####### 0 is white  ###### 1 is black  ####### -1 is none
        self.is_red = False

        self.upper_grid = None
        self.downer_grid = None
        self.righter_grid = None
        self.lefter_grid = None

class board:
    def __init__(self, n, m):
        self.m = m
        self.n = n
        all_grids = [[grid(i,j) for i in range(m)] for j in range(n)]

        #####################   setting up down left right connection
        for i in range(m):
            for j in range(n):
                if i-1 >= 0:
                    all_grids[i][j].lefter_grid = all_grids[i-1][j]
                if i+1 <= m-1:
                    all_grids[i][j].righter_grid = all_grids[i+1][j]
                if j-1 >= 0:
                    all_grids[i][j].upper_grid = all_grids[i][j-1]
                if j+1 <= n-1:
                    all_grids[i][j].downer_grid = all_grids[i][j+1]

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


def find_cycle_borders(border_edges_list , m, n):
    border_grids_list = []
    # candidate_border_grids_list = []
    minx = m * grid_lenght
    miny = n * grid_lenght
    index = 0

    for edg in border_edges_list:
        minxe = min(edg.p1.x , edg.p2.x)
        if minx > minxe:
            minx = minxe
            minye = min(edg.p1.y, edg.p2.y)
            if miny < minye:
                miny = minye
                index = border_edges_list.index(edg)

    del border_edges_list[index]
    border_grids_list.append(all_grids[ int(minx / grid_lenght)][int(miny / grid_lenght)])
    edg0 = border_grids_list[0].e12
    edg = edg0
    while len(border_edges_list) != 0:
        i, j, next_edge = find_next_grid(border_edges_list, edg)
        border_grids_list.append(all_grids[i][j])
        border_edges_list.remove(edg)
        edg = next_edge
        d =0 
        print(d)
        d +=1

def find_next_grid(border_edges_list, edg):             #### edg.p1 -> edg.p2 show the direction of movement
    direction = get_direction(edg)
    next_edge = edg
    if direction == 1:
        for e in border_edges_list:
            if edg.p2.is_equal(e.p1):
                next_edge = e
            elif edg.p2.is_equal(e.p2):
                p = e.p1
                e.p1 = e.p2
                e.p2 = p
                next_edge = e
        next_dir = get_direction(next_edge)
        if next_dir == 1:
            i, j = get_grid_from_point(next_edge.p2)
            return i, j-1, next_edge
        elif next_dir == 2:
            i , j = get_grid_from_point(next_edge.p2)
            return i, j, next_edge
        elif next_dir == 4:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j-1, next_edge
    elif direction == 2:
        for e in border_edges_list:
            if edg.p2.is_equal(e.p1):
                next_edge = e
            elif edg.p2.is_equal(e.p2):
                p = e.p1
                e.p1 = e.p2
                e.p2 = p
                next_edge = e
        next_dir = get_direction(next_edge)
        if next_dir == 1:
            i, j = get_grid_from_point(next_edge.p2)
            return i, j-1, next_edge
        elif next_dir == 2:
            i, j = get_grid_from_point(next_edge.p2)
            return i, j, next_edge
        elif next_dir == 3:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j, next_edge
    elif direction == 3:
        for e in border_edges_list:
            if edg.p2.is_equal(e.p1):
                next_edge = e
            elif edg.p2.is_equal(e.p2):
                p = e.p1
                e.p1 = e.p2
                e.p2 = p
                next_edge = e
        next_dir = get_direction(next_edge)
        if next_dir == 2:
            i, j = get_grid_from_point(next_edge.p2)
            return i, j, next_edge
        elif next_dir == 3:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j, next_edge
        elif next_dir == 4:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j-1, next_edge
    elif direction == 4:
        for e in border_edges_list:
            if edg.p2.is_equal(e.p1):
                next_edge = e
            elif edg.p2.is_equal(e.p2):
                p = e.p1
                e.p1 = e.p2
                e.p2 = p
                next_edge = e
        next_dir = get_direction(next_edge)
        if next_dir == 1:
            i, j = get_grid_from_point(next_edge.p2)
            return i, j-1, next_edge
        elif next_dir == 3:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j, next_edge
        elif next_dir == 4:
            i, j = get_grid_from_point(next_edge.p2)
            return i-1, j-1, next_edge
            
def get_grid_from_point(p):
    return p.x / grid_lenght , p.y / grid_lenght


def get_direction(edg):
    direction = 0
    if edg.p1.x == edg.p2.x:
        if edg.p1.y > edg.p2.y:
            direction = 2
        else:
            direction = 4
    else:
        if edg.p1.x > edg.p2.x:
            direction = 1
        else:
            direction = 3
    return direction




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

border_edges_list = [edge(p7,p8), edge(p3,p4), edge(p1,p2), edge(p4,p5), edge(p16,p1), edge(p5,p6), edge(p3,p2), edge(p7,p6), edge(p14,p13), 
edge(p12,p13), edge(p9,p8), edge(p14,p15),edge(p9,p10), edge(p10,p11), edge(p16,p15), edge(p11,p12)]
