
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
    def print_point(self):
        print(self.x, self.y)

class edge:
    def __init__ (self, p1 , p2):
        self.p1 = p1
        self.p2 = p2
        
    def print_edge(self):
        print ((self.p1.x, self.p1.y) , (self.p2.x, self.p2.y))

class grid:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

        self.p1 = point( x  , y  )
        self.p2 = point( x+1, y  )
        self.p3 = point( x+1, y+1)
        self.p4 = point( x  , y+1)
        self.e12 = edge(self.p1, self.p2)
        self.e23 = edge(self.p2, self.p3)
        self.e34 = edge(self.p3, self.p4)
        self.e41 = edge(self.p4, self.p1)

        self.base_color = 0            ######## 0 is white  ####### 1 is gray  ######## 2 is black
        self.visited = False            ####### this is for finding inner cells based on using             """"BFS""""
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
        for i in range(n):
            all_grids.append([])
            for j in range(m):
                all_grids[i].append(grid(i,j))
        #####################   setting up down left right connection
        for i in range(n):
            for j in range(m):
                if i-1 >= 0:
                    all_grids[i][j].lefter_grid = all_grids[i-1][j]
                if i+1 <= n-1:
                    all_grids[i][j].righter_grid = all_grids[i+1][j]
                if j-1 >= 0:
                    all_grids[i][j].upper_grid = all_grids[i][j-1]
                if j+1 <= m-1:
                    all_grids[i][j].downer_grid = all_grids[i][j+1]

        ####################### coloring the base 
        for i in range(n):
            for j in range(m):
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


def find_cycle_borders(all_grids, border_edges_list , m, n):
    border_grids_list = []
    miny = n
    
    e = border_edges_list[0]
    minimal_list = []
    for edg in border_edges_list:
        minye = min(edg.p1.y, edg.p2.y)
        if miny > minye:
            miny = minye
            minimal_list = []
            minimal_list.append(edg)
        elif miny == minye:
            minimal_list.append(edg)
    
    del_list = []
    for edg in minimal_list:
        if edg.p1.y != edg.p2.y:
            del_list.append(edg)
    for k in range(len(del_list)):
        minimal_list.remove(del_list[k])
    e = minimal_list[0]
    for edg in minimal_list:
        if min(e.p1.x , e.p2.x) > min(edg.p1.x, edg.p2.x):
            e = edg

    border_grids_list.append(all_grids[ min(e.p1.x,e.p2.x)][min(e.p1.y, e.p2.y) ])
    border_edges_list.remove(e)

    print(border_grids_list[0].x, border_grids_list[0].y)
    edg0 = border_grids_list[0].e12
    border_edges_list = edge_ordering(edg0, border_edges_list)
    border_grids = border_cells(border_edges_list, all_grids)


#     edg = edg0
#     d = 0
#     i, j = 0, 0
#     while len(border_edges_list) > d:
#         i, j, next_edge = find_next_grid(border_edges_list, edg)
#         print("i", i, "j", j)
#         if border_grids_list.count(all_grids[i][j]) == 0:
#             border_grids_list.append(all_grids[int(i)][int(j)])
# #        print(border_grids_list[-1].x, border_grids_list[-1].y)
# #        border_edges_list.remove(edg)
#         edg = next_edge
#         print(len(border_grids_list))
#         d +=1

def edge_ordering(edge0, border):    #assomption is edge up left 3 type of direction
    correct_border = []
    correct_border.append(edge0)
    while 0 < len(border):
        p2 = edge0.p2
        for e in border:
            if p2.is_equal(e.p1):
                edge0 = e
                border.remove(e)
                correct_border.append(edge0)
                break
            elif p2.is_equal(e.p2):
                p = e.p1
                e.p1 = e.p2
                e.p2 = p
                edge0 = e
                border.remove(e)
                correct_border.append(edge0)
                break
    return correct_border

############ farz mikonim ke fasele ha ra'ayat shode!!
def border_cells(border, all_grids):
    border_grids = []
    for i in range(len(border)):

        if get_direction(border[i]) == 1:
            t, u = border[i].p2.x, border[i].p2.y -1
            if all_grids[t][u].is_in_cycle_border:
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])

        elif get_direction(border[i]) == 2:
            t, u = border[i].p2.x, border[i].p2.y
            if all_grids[t][u].is_in_cycle_border:
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])

        elif get_direction(border[i]) == 3:
            t, u = border[i].p2.x-1, border[i].p2.y
            if all_grids[t][u].is_in_cycle_border:
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])

        elif get_direction(border[i]) == 4:
            t, u = border[i].p2.x-1, border[i].p2.y-1
            if all_grids[t][u].is_in_cycle_border:
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])
    return  border_grids

    #todo first find one of inner cells , for example downer cell of up left cell! after that we use bfs and implement it in this method using this link "https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/"
    #todo  and adding 4 neighbours (up, down, left, right)   is_visited !! and checking none of them is .is_in_border== true! :)

def inner_cells(border_cells, cell, all_grids):



# def find_next_grid(border_edges_list, edg):             #### edg.p1 -> edg.p2 show the direction of movement
#     handy_border_edges_list = border_edges_list
#     direction = get_direction(edg)
#     print(direction)
#     next_edge = edg
#     if direction == 1:
#         for e in border_edges_list:
#             if edg.p2.is_equal(e.p1):
#                 next_edge = e
#                 break
#             elif edg.p2.is_equal(e.p2):
#                 p = e.p1
#                 e.p1 = e.p2
#                 e.p2 = p
#                 next_edge = e
#                 break
#         next_dir = get_direction(next_edge)
#         if next_dir == 1:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i, j-1, next_edge
#         elif next_dir == 2:
#             i , j = get_grid_from_point(next_edge.p2)
#             return i, j, next_edge
#         elif next_dir == 4:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j-1, next_edge
#     elif direction == 2:
#         for e in border_edges_list:
#             if edg.p2.is_equal(e.p1):
#                 next_edge = e
#                 break
#             elif edg.p2.is_equal(e.p2):
#                 p = e.p1
#                 e.p1 = e.p2
#                 e.p2 = p
#                 next_edge = e
#                 break
#         next_dir = get_direction(next_edge)
#         if next_dir == 1:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i, j-1, next_edge
#         elif next_dir == 2:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i, j, next_edge
#         elif next_dir == 3:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j, next_edge
#     elif direction == 3:
#         for e in border_edges_list:
#             if edg.p2.is_equal(e.p1):
#                 next_edge = e
#                 break
#             elif edg.p2.is_equal(e.p2):
#                 p = e.p1
#                 e.p1 = e.p2
#                 e.p2 = p
#                 next_edge = e
#                 break
#         next_dir = get_direction(next_edge)
#
#         print(next_dir, "nextdir")
#         if next_dir == 2:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i, j, next_edge
#         elif next_dir == 3:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j, next_edge
#         elif next_dir == 4:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j-1, next_edge
#     elif direction == 4:
#         for e in border_edges_list:
#             if edg.p2.is_equal(e.p1):
#                 next_edge = e
#                 break
#             elif edg.p2.is_equal(e.p2):
#                 p = e.p1
#                 e.p1 = e.p2
#                 e.p2 = p
#                 next_edge = e
#                 break
#         next_dir = get_direction(next_edge)
#         if next_dir == 1:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i, j-1, next_edge
#         elif next_dir == 3:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j, next_edge
#         elif next_dir == 4:
#             i, j = get_grid_from_point(next_edge.p2)
#             return i-1, j-1, next_edge
            
def get_grid_from_point(p):
    return p.x, p.y


def get_direction(edg):
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
    
m = 3
n = 4
    
bord = board(6,5)

p1 = point(2,1)
p2 = point(3,1)
p3 = point(3,2)
p4 = point(4,2)
p5 = point(4,3)
p6 = point(4,4)
p7 = point(3,4)
p8 = point(3,3)
p9 = point(2,3)
p10 = point(2,4)
p11 = point(2,5)
p12 = point(1,5)
p13 = point(1,4)
p14 = point(1,3)
p15 = point(1,2)
p16 = point(2,2)

border_edges_list = [edge(p7,p8), edge(p3,p4), edge(p1,p2), edge(p4,p5), edge(p16,p1), edge(p5,p6), edge(p3,p2), edge(p7,p6), edge(p14,p13), 
edge(p12,p13), edge(p9,p8), edge(p14,p15),edge(p9,p10), edge(p10,p11), edge(p16,p15), edge(p11,p12)]

# for edg in border_edges_list:
#     print(edg.p1.x/grid_lenght, edg.p1.y/grid_lenght, edg.p2.x/grid_lenght, edg.p2.y/grid_lenght)
    
find_cycle_borders(all_grids, border_edges_list, m, n)