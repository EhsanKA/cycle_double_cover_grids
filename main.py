
grid_lenght = 64

all_grids = []
cir_white = 1
cir_black = 2
white = 0
black = 2
gray = 1

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
        self.is_e12_in_border = False
        self.is_e23_in_border = False
        self.is_e34_in_border = False
        self.is_e41_in_border = False
        # self.cycle_connectivity_num = 0

        # self.is_yellow = False
        #
        # self.is_blue_1 = False
        # self.is_blue_2 = False
        # self.is_blue_3 = False
        # self.is_blue_border = False
        #
        # self.is_magenta_1 = False
        # self.is_magenta_2 = False
        # self.is_magenta_3 = False
        #
        # self.is_in_q = False
        # self.is_in_q_border = False
        # self.is_corner = False
        self.has_circle = 0            ####### 0 is none  ###### 1 is white  ####### 2 is black
        # self.is_red = False

        self.upper_grid = None
        self.downer_grid = None
        self.righter_grid = None
        self.lefter_grid = None

class board:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        for j in range(m):
            all_grids.append([])
            for i in range(n):
                all_grids[j].append(grid(i,j))
        #####################   setting up down left right connection
        for j in range(m):
            for i in range(n):
                if i-1 >= 0:
                    all_grids[j][i].lefter_grid = all_grids[j][i-1]
                if i+1 <= n-1:
                    all_grids[j][i].righter_grid = all_grids[j][i+1]
                if j-1 >= 0:
                    all_grids[j][i].upper_grid = all_grids[j-1][i]
                if j+1 <= m-1:
                    all_grids[j][i].downer_grid = all_grids[j+1][i]

        ####################### coloring the base 
        for j in range(m):
            for i in range(n):
                if i %2 ==1:
                    if j%2 ==1:
                        all_grids[j][i].base_color = 2
                    else:
                        all_grids[j][i].base_color = 1
                else:
                    if j%2 ==1:
                        all_grids[j][i].base_color = 1
                    else:
                        all_grids[j][i].base_color = 0


def find_cycle_borders(all_grids, border_edges_list , m, n):
    border_grids_list = []
    miny = m
    
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

    border_grids_list.append(all_grids[min(e.p1.y, e.p2.y)][min(e.p1.x,e.p2.x)])
    border_edges_list.remove(e)

    # print(border_grids_list[0].x, border_grids_list[0].y)
    edg0 = border_grids_list[0].e12
    tmp_border_edges_list = edge_ordering(edg0, border_edges_list)
    border_edges_list = tmp_border_edges_list
    border_grids = border_cells(border_edges_list, all_grids)
    inner_cells(border_grids_list[0])
    find_circles(border_edges_list, all_grids)


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
            t, u = border[i].p2.y -1, border[i].p2.x
            if all_grids[t][u].is_in_cycle_border:
                all_grids[t][u].is_e34_in_border = True
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])
                all_grids[t][u].is_e34_in_border = True

        elif get_direction(border[i]) == 2:
            t, u = border[i].p2.y, border[i].p2.x
            if all_grids[t][u].is_in_cycle_border:
                all_grids[t][u].is_e41_in_border = True
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])
                all_grids[t][u].is_e41_in_border = True

        elif get_direction(border[i]) == 3:
            t, u = border[i].p2.y, border[i].p2.x-1
            if all_grids[t][u].is_in_cycle_border:
                all_grids[t][u].is_e12_in_border = True
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])
                all_grids[t][u].is_e12_in_border = True

        elif get_direction(border[i]) == 4:
            t, u = border[i].p2.y-1, border[i].p2.x-1
            if all_grids[t][u].is_in_cycle_border:
                all_grids[t][u].is_e23_in_border = True
                continue
            else:
                all_grids[t][u].is_in_cycle_border = True
                border_grids.append(all_grids[t][u])
                all_grids[t][u].is_e23_in_border = True
    return  border_grids

    # first find one of inner cells , for example downer cell of up left cell! after that we use bfs and implement it in this method using this link "https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/"
    #  and adding 4 neighbours (up, down, left, right)   is_visited !! and checking none of them is .is_in_border== true! :)

def inner_cells(cell):
    q = []
    q.append(cell)
    cell.visited = True
    cell.is_in_cycle = True
    while len(q) > 0:
        add_neighbours(q[0], q)
        q.pop(0)


def add_neighbours(cell, q):
    if cell.upper_grid.visited == False and cell.is_e12_in_border== False:
        q.append(cell.upper_grid)
        cell.upper_grid.is_in_cycle = True
        cell.upper_grid.visited = True

    if cell.downer_grid.visited == False and cell.is_e34_in_border== False:
        q.append(cell.downer_grid)
        cell.downer_grid.is_in_cycle = True
        cell.downer_grid.visited = True

    if cell.righter_grid.visited == False and cell.is_e23_in_border== False:
        q.append(cell.righter_grid)
        cell.righter_grid.is_in_cycle = True
        cell.righter_grid.visited = True

    if cell.lefter_grid.visited == False and cell.is_e41_in_border== False:
        q.append(cell.lefter_grid)
        cell.lefter_grid.is_in_cycle = True
        cell.lefter_grid.visited = True


def find_circles(border, all_grids):
                                                                        #niaz nist dasti bashe range( -1, len(border)) okeye: border[n-1] -> border[0] dasti barresi shavad
    for i in range(-1, len(border)-1):
        fdir = get_direction(border[i])             #first
        sdir = get_direction(border[i+1])           #second
        x_cord = border[i].p2.x
        y_cord = border[i].p2.y

        if fdir == 1:
            if sdir == 1:
                continue
            elif sdir == 2 and all_grids[y_cord - 1][x_cord].base_color == gray:
                all_grids[y_cord-1][x_cord].has_circle = cir_white
                if all_grids[y_cord][x_cord].base_color == white:
                    all_grids[y_cord][x_cord].has_circle = cir_white
                    all_grids[y_cord][x_cord + 1].has_circle = cir_white
                else:
                    all_grids[y_cord-1][x_cord-1].has_circle = cir_white
                    all_grids[y_cord-2][x_cord-1].has_circle =cir_white

            elif sdir == 4 and all_grids[y_cord][x_cord].base_color == gray:
                all_grids[y_cord][x_cord].has_circle = cir_black
                if all_grids[y_cord][x_cord - 1].base_color == black:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord + 1][x_cord - 1].has_circle = cir_black
                else:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord + 1].has_circle = cir_black

        if fdir == 2:
            if sdir == 1 and all_grids[y_cord][x_cord-1].base_color == gray:
                all_grids[y_cord][x_cord-1].has_circle = cir_black
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord][x_cord].has_circle = cir_black
                    all_grids[y_cord+1][x_cord].has_circle = cir_black
                else:
                    all_grids[y_cord-1][x_cord-1].has_circle = cir_black
                    all_grids[y_cord-1][x_cord-2].has_circle = cir_black

            elif sdir == 2:
                continue
            elif sdir == 3 and all_grids[y_cord][x_cord].base_color == gray:
                all_grids[y_cord][x_cord - 1].has_circle = cir_white
                if all_grids[y_cord][x_cord-1].base_color == white:
                    all_grids[y_cord][x_cord-1].has_circle = cir_white
                    all_grids[y_cord + 1][x_cord-1].has_circle = cir_white
                else:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord + 1].has_circle = cir_white

        if fdir == 3:
            if sdir == 2 and all_grids[y_cord][x_cord].base_color == gray:
                all_grids[y_cord - 1][x_cord - 1].has_circle = cir_black
                if all_grids[y_cord - 1][x_cord].base_color == black:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_black
                    all_grids[y_cord - 2][x_cord].has_circle = cir_black
                else:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord][x_cord - 2].has_circle = cir_black

            elif sdir == 3:
                continue
            elif sdir == 4 and all_grids[y_cord][x_cord - 1].base_color == gray:
                all_grids[y_cord][x_cord - 1].has_circle = cir_white
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord - 1][x_cord - 1].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord - 2].has_circle = cir_white
                else:
                    all_grids[y_cord][x_cord].has_circle = cir_white
                    all_grids[y_cord + 1][x_cord].has_circle = cir_white

        if fdir == 4:
            if sdir == 1 and all_grids[y_cord][x_cord].base_color == gray:
                all_grids[y_cord - 1][x_cord - 1].has_circle = cir_white
                if all_grids[y_cord][x_cord - 1].base_color == black:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_white
                    all_grids[y_cord - 2][x_cord].has_circle = cir_white
                else:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_white
                    all_grids[y_cord][x_cord - 2].has_circle = cir_white

            elif sdir == 3 and all_grids[y_cord - 1][x_cord].base_color == gray:
                all_grids[y_cord - 1][x_cord].has_circle = cir_black
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord][x_cord].has_circle = cir_black
                    all_grids[y_cord][x_cord + 1].has_circle = cir_black
                else:
                    all_grids[y_cord - 1][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord - 2][x_cord - 1].has_circle = cir_black

            elif sdir == 4:
                continue




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
    
m = 10
n = 11
    
bord = board(m,n)

p1 = point(1,1)
p2 = point(2,1)
p3 = point(3,1)
p4 = point(4,1)
p5 = point(4,2)
p6 = point(4,3)
p7 = point(4,4)
p8 = point(5,4)
p9 = point(6,4)
p10 = point(7,4)
p11 = point(7,3)
p12 = point(7,2)
p13 = point(7,1)
p14 = point(8,1)
p15 = point(9,1)
p16 = point(10,1)
p17 = point(10,2)
p18 = point(10,3)
p19 = point(10,4)
p20 = point(10,5)
p21 = point(10,6)
p22 = point(9,6)
p23 = point(8,6)
p24 = point(7,6)
p25 = point(6,6)
p26 = point(6,7)
p27 = point(6,8)
p28 = point(6,9)
p29 = point(5,9)
p30 = point(4,9)
p31 = point(3,9)
p32 = point(2,9)
p33 = point(1,9)
p34 = point(1,8)
p35 = point(1,7)
p36 = point(1,6)
p37 = point(1,5)
p38 = point(1,4)
p39 = point(1,3)
p40 = point(1,2)

border_edges_list = [edge(p40,p1) ,edge(p1,p2) ,edge(p2,p3) ,edge(p3,p4) ,edge(p4,p5) ,edge(p5,p6) ,edge(p6,p7) ,edge(p7,p8) ,edge(p8,p9) ,edge(p9,p10) ,edge(p10,p11) ,edge(p11,p12) ,edge(p12,p13) ,edge(p13,p14) ,edge(p14,p15) ,edge(p15,p16) ,edge(p16,p17) ,edge(p17,p18) ,edge(p18,p19) ,edge(p19,p20) ,edge(p20,p21) ,edge(p21,p22) ,edge(p22,p23) ,edge(p23,p24) ,edge(p24,p25) ,edge(p25,p26) ,edge(p26,p27) ,edge(p27,p28) ,edge(p28,p29) ,edge(p29,p30) ,edge(p30,p31) ,edge(p31,p32) ,edge(p32,p33) ,edge(p33,p34) ,edge(p34,p35) ,edge(p35,p36) ,edge(p36,p37) ,edge(p37,p38) ,edge(p38,p39) ,edge(p39,p40)]

# for edg in border_edges_list:
#     print(edg.p1.x/grid_lenght, edg.p1.y/grid_lenght, edg.p2.x/grid_lenght, edg.p2.y/grid_lenght)
    
find_cycle_borders(all_grids, border_edges_list, m, n)