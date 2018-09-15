
import pygame
import sys

grid_lenght = 48
w = 7
backgroud_color = (255,255,255)
rec_white, rec_black, rec_grey = (200, 200, 200), (0, 0, 0), (128, 128, 128)
rec_white_back = (230, 230, 230)
rec_blue = (0,0,255)
rec_red = (255,50,50)
rec_yellow = (255,255,0)
rec_magenta = (255,100,255)

screen = pygame.display.set_mode((900,900))
screen.fill(backgroud_color)


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_equal(self, p):
        if self.x == p.x and self.y == p.y:
            return 1
        else:
            return 0

    def print_point(self):
        print(self.x, self.y)

shift = point(50,50)
horizontal_start = point(shift.x + int((w+1)/2), shift.y + w)
vertical_start = point(shift.x + w, shift.y + int((w+1)/2))
all_grids = []

cir_white = 1
cir_black = 3

white = 0
black = 2
grey = 1



class edge:
    def __init__ (self, p1 , p2):
        self.p1 = p1
        self.p2 = p2
        self.c1 = (255,100,255)
        self.c2 = (255,100,255)


    def print_edge(self):
        print ((self.p1.x, self.p1.y) , (self.p2.x, self.p2.y))

    def draw(self, screen, width, color_vector):
        print("salam")
        
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

        self.base_color = 0            ######## 0 is white  ####### 1 is grey  ######## 2 is black
        self.visited = False            ####### this is for finding inner cells based on using             """"BFS""""
        self.is_in_cycle = False
        self.is_in_cycle_border = False
        self.is_e12_in_border = False
        self.is_e23_in_border = False
        self.is_e34_in_border = False
        self.is_e41_in_border = False
        ##               [black, red, yellow, blue, magenta]
        self.e12_color = [0    , 0  , 0     , 0   , 0]
        self.e23_color = [0, 0, 0, 0, 0]
        self.e34_color = [0, 0, 0, 0, 0]
        self.e41_color = [0, 0, 0, 0, 0]
        # self.cycle_connectivity_num = 0

        self.is_yellow = False
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
        self.has_circle = 0            ####### 0 is none  ###### 1 is white  ####### 3 is black
        self.is_red = False

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
        #############################

        # for j in range(m-1):
        #     for i in range(n-1):
        #         color = all_grids[j][i].base_color
        #         if color == 0:
        #             pygame.draw.line(screen, rec_white, [(grid_lenght+width) * j, (grid_lenght+width) * i] ,[(grid_lenght+width) * (j+1), (grid_lenght+width) * i] ,width)
        #         if color == 1:
        #             pygame.draw.line(screen, rec_grey, [(grid_lenght+width) * j, (grid_lenght+width) * i] ,[(grid_lenght+width) * (j+1), (grid_lenght+width) * i],width)
        #         if color == 2:
        #             pygame.draw.line(screen, rec_black, [(grid_lenght+width) * j, (grid_lenght+width) * i] ,[(grid_lenght+width) * (j+1), (grid_lenght+width) * i],width)
        #         pygame.display.update()
        #         pygame.time.delay(20)

        
def find_cycle_borders(all_grids, border_edges_list , m, n):
    border_grids_list = []
    miny = m
    
#     for u in range(10):
#         if u%2 == 1:
#             pygame.draw.line(screen, (255,0,0), [0,21+ 10*u], [0, 19 + 10*(u+1)], 10)
#         else:
#             pygame.draw.line(screen, (0,0,0), [0,21+ 10*u], [0, 19 + 10*(u+1)], 10)
#
# #    pygame.draw.line(screen, (255,0,0), [150,270], [403, 740], 10)
#     pygame.display.update()
#
#     for u in range(10):
#         if u%2 == 1:
#             pygame.draw.line(screen, (0,0,255), [4,121+ 10*u], [4, 119 + 10*(u+1)], 7)
#         else:
#             pygame.draw.line(screen, (0,0,0), [4,121+ 10*u], [4, 119 + 10*(u+1)], 7)
#
#     pygame.display.update()
#
#     for u in range(10):
#         if u%2 == 1:
#             pygame.draw.line(screen, (255,0,255), [480,21+ 10*u], [480, 19 + 10*(u+1)], 10)
#         else:
#             pygame.draw.line(screen, (255,0,255), [480,21+ 10*u], [480, 19 + 10*(u+1)], 10)
#
#     pygame.display.update()
#
#     pygame.draw.line(screen, (0,0,0), [490,121], [490, 19 + 200], 4)
#     pygame.display.update()
#     pygame.draw.line(screen, (0,0,255), [495,121], [495, 19 + 200], 4)
#     pygame.display.update()
#
#
#     pygame.draw.line(screen, (255,0,0), [490,221], [490, 19 + 250], 4)
#     pygame.display.update()
#     pygame.draw.line(screen, (200,200,200), [495,221], [495, 19 + 250], 4)
#     pygame.display.update()
#
    
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
    red_start_end = find_red_cells_start_end(border_edges_list, all_grids)
    red_cells = find_red_cells(red_start_end,all_grids, border_edges_list)
    update_red_edges_color(all_grids)

    for j in range(m):
        for i in range(n):
            print(i,j, all_grids[j][i].is_yellow)

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
            elif sdir == 2 and all_grids[y_cord - 1][x_cord].base_color == grey:
                all_grids[y_cord-1][x_cord].has_circle = cir_white
                all_grids[y_cord - 1][x_cord].is_yellow = True
                if all_grids[y_cord][x_cord].base_color == white:
                    all_grids[y_cord][x_cord].has_circle = cir_white
                    all_grids[y_cord][x_cord].is_yellow = True
                    all_grids[y_cord][x_cord + 1].has_circle = cir_white
                    all_grids[y_cord][x_cord + 1].is_yellow = True
                else:
                    all_grids[y_cord-1][x_cord-1].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                    all_grids[y_cord-2][x_cord-1].has_circle =cir_white
                    all_grids[y_cord - 2][x_cord - 1].is_yellow = True

            elif sdir == 4 and all_grids[y_cord][x_cord].base_color == grey:
                all_grids[y_cord][x_cord].has_circle = cir_black
                all_grids[y_cord][x_cord].is_yellow = True
                if all_grids[y_cord][x_cord - 1].base_color == black:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord][x_cord - 1].is_yellow = True
                    all_grids[y_cord + 1][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord + 1][x_cord - 1].is_yellow = True
                else:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord].is_yellow = True
                    all_grids[y_cord - 1][x_cord + 1].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord + 1].is_yellow = True

        if fdir == 2:
            if sdir == 1 and all_grids[y_cord][x_cord-1].base_color == grey:
                all_grids[y_cord][x_cord-1].has_circle = cir_black
                all_grids[y_cord][x_cord - 1].is_yellow = True
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord][x_cord].has_circle = cir_black
                    all_grids[y_cord][x_cord].is_yellow = True
                    all_grids[y_cord+1][x_cord].has_circle = cir_black
                    all_grids[y_cord + 1][x_cord].is_yellow = True
                else:
                    all_grids[y_cord-1][x_cord-1].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                    all_grids[y_cord-1][x_cord-2].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord - 2].is_yellow = True

            elif sdir == 2:
                continue
            elif sdir == 3 and all_grids[y_cord][x_cord].base_color == grey:
                all_grids[y_cord][x_cord - 1].has_circle = cir_white
                all_grids[y_cord][x_cord - 1].is_yellow = True
                if all_grids[y_cord][x_cord-1].base_color == white:
                    all_grids[y_cord][x_cord-1].has_circle = cir_white
                    all_grids[y_cord][x_cord - 1].is_yellow = True
                    all_grids[y_cord + 1][x_cord-1].has_circle = cir_white
                    all_grids[y_cord + 1][x_cord - 1].is_yellow = True
                else:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord].is_yellow = True
                    all_grids[y_cord - 1][x_cord + 1].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord + 1].is_yellow = True

        if fdir == 3:
            if sdir == 2 and all_grids[y_cord][x_cord].base_color == grey:
                all_grids[y_cord - 1][x_cord - 1].has_circle = cir_black
                all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                if all_grids[y_cord - 1][x_cord].base_color == black:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord].is_yellow = True
                    all_grids[y_cord - 2][x_cord].has_circle = cir_black
                    all_grids[y_cord - 2][x_cord].is_yellow = True
                else:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord][x_cord - 1].is_yellow = True
                    all_grids[y_cord][x_cord - 2].has_circle = cir_black
                    all_grids[y_cord][x_cord - 2].is_yellow = True

            elif sdir == 3:
                continue
            elif sdir == 4 and all_grids[y_cord][x_cord - 1].base_color == grey:
                all_grids[y_cord][x_cord - 1].has_circle = cir_white
                all_grids[y_cord][x_cord - 1].is_yellow = True
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord - 1][x_cord - 1].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                    all_grids[y_cord - 1][x_cord - 2].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord - 2].is_yellow = True
                else:
                    all_grids[y_cord][x_cord].has_circle = cir_white
                    all_grids[y_cord][x_cord].is_yellow = True
                    all_grids[y_cord + 1][x_cord].has_circle = cir_white
                    all_grids[y_cord + 1][x_cord].is_yellow = True

        if fdir == 4:
            if sdir == 1 and all_grids[y_cord][x_cord].base_color == grey:
                all_grids[y_cord - 1][x_cord - 1].has_circle = cir_white
                all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                if all_grids[y_cord][x_cord - 1].base_color == black:
                    all_grids[y_cord - 1][x_cord].has_circle = cir_white
                    all_grids[y_cord - 1][x_cord].is_yellow = True
                    all_grids[y_cord - 2][x_cord].has_circle = cir_white
                    all_grids[y_cord - 2][x_cord].is_yellow = True
                else:
                    all_grids[y_cord][x_cord - 1].has_circle = cir_white
                    all_grids[y_cord][x_cord - 1].is_yellow = True
                    all_grids[y_cord][x_cord - 2].has_circle = cir_white
                    all_grids[y_cord][x_cord - 2].is_yellow = True

            elif sdir == 3 and all_grids[y_cord - 1][x_cord].base_color == grey:
                all_grids[y_cord - 1][x_cord].has_circle = cir_black
                all_grids[y_cord - 1][x_cord].is_yellow = True
                if all_grids[y_cord][x_cord].base_color == black:
                    all_grids[y_cord][x_cord].has_circle = cir_black
                    all_grids[y_cord][x_cord].is_yellow = True
                    all_grids[y_cord][x_cord + 1].has_circle = cir_black
                    all_grids[y_cord][x_cord + 1].is_yellow = True
                else:
                    all_grids[y_cord - 1][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord - 1][x_cord - 1].is_yellow = True
                    all_grids[y_cord - 2][x_cord - 1].has_circle = cir_black
                    all_grids[y_cord - 2][x_cord - 1].is_yellow = True

            elif sdir == 4:
                continue

def coloring_90_deg(x_cord, y_cord, all_grids):
    #todo i can use this and next method for easy use in before method if fdir+1 == sdir call this and if fdir-1 == sdir call next method
    print("under construction")

def coloring_270_deg(x_cord, y_cord, all_grids):
    #todo use last todo for more information ... ...
    print("under construction")

def find_red_cells_start_end(border, all_grids):
    start_ends = [[None, None]]
    for i in range(0, len(border)-1):
        fdir = get_direction(border[i])             #first
        sdir = get_direction(border[i+1])           #second
        x_cord = border[i].p2.x
        y_cord = border[i].p2.y
        if fdir == 1:
            if sdir == 1:
                if all_grids[y_cord][x_cord].is_yellow == True and all_grids[y_cord - 1][x_cord].is_yellow == True:
                    b = [i+1, None]
                    start_ends.append(b)
                elif all_grids[y_cord - 1][x_cord - 1].is_yellow == True and all_grids[y_cord][x_cord - 1].is_yellow == True:
                    start_ends[-1][1] = i

        elif fdir == 2:
            if sdir == 2:
                if all_grids[y_cord][x_cord - 1].is_yellow == True and all_grids[y_cord][x_cord].is_yellow == True:
                    b = [i+1, None]
                    start_ends.append(b)
                elif all_grids[y_cord - 1][x_cord - 1].is_yellow == True and all_grids[y_cord - 1][x_cord].is_yellow == True:
                    start_ends[-1][1] = i

        elif fdir == 3:
            if sdir == 3:
                if all_grids[y_cord - 1][x_cord - 1].is_yellow == True and all_grids[y_cord][x_cord - 1].is_yellow == True:
                    b = [i + 1, None]
                    start_ends.append(b)
                elif all_grids[y_cord - 1][x_cord].is_yellow == True and all_grids[y_cord][x_cord].is_yellow == True:
                    start_ends[-1][1] = i
                else:
                    continue
        elif fdir == 4:
            if sdir == 4:
                if all_grids[y_cord][x_cord - 1].is_yellow == True and all_grids[y_cord][x_cord].is_yellow == True:
                    start_ends[-1][1] = i
                elif all_grids[y_cord - 1][x_cord - 1].is_yellow == True and all_grids[y_cord - 1][x_cord].is_yellow == True:
                    b = [i+1, None]
                    start_ends.append(b)

    if start_ends[0][1] is not None:
        start_ends[0][0] = start_ends[-1][0]
        return start_ends[:-1]
    else:
        return start_ends[1:]


def find_red_cells(start_ends, all_grids, border):
    grids = []
    for i in range(len(start_ends)):
        rng = 0
        if start_ends[i][1] - start_ends[i][0] + 1 < 0:
            rng = len(border)-(start_ends[i][0] - start_ends[i][1]) + 1
        else:
            rng = start_ends[i][1] - start_ends[i][0] + 1
        start = start_ends[i][0] -1
        for j in range(rng):
            start += 1
            if start == len(border):
                start = 0
            fdir = get_direction(border[start])
            after_start = start +1
            if after_start == len(border):
                after_start = 1
            sdir = get_direction(border[after_start])
            x_cord = border[start].p2.x
            y_cord = border[start].p2.y

            if fdir == 1:
                if sdir == 1:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])
                if sdir == 2:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
                if sdir == 4:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])
            if fdir == 2:
                if sdir == 1:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])
                if sdir == 2:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
                if sdir == 3:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
            if fdir == 3:
                if sdir == 2:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
                if sdir == 3:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
                if sdir == 4:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])
            if fdir == 4:
                if sdir == 1:
                    all_grids[y_cord][x_cord].is_red = True
                    grids.append(all_grids[y_cord][x_cord])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])
                if sdir == 3:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord][x_cord - 1])
                if sdir == 4:
                    all_grids[y_cord - 1][x_cord - 1].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord - 1])
                    all_grids[y_cord - 1][x_cord].is_red = True
                    grids.append(all_grids[y_cord - 1][x_cord])

    return grids




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



def community_of_grids(grids, type):
    edges = []
    if type == 1:                           ##### type 1 is red
        for g in grids:
            if g.upper_grid is not None:
                if g.upper_grid.is_red:
                    continue
                else:
                    edges.append(g.e12)
            if g.lefter_grid is not None:
                if g.lefter_grid.is_red:
                    continue
                else:
                    edges.append(g.e41)
            if g.downer_grid is not None:
                if g.downer_grid.is_red:
                    continue
                else:
                    edges.append(g.e34)
            if g.righter_grid is not None:
                if g.righter_grid.is_red:
                    continue
                else:
                    edges.append(g.e23)
        return edges
    if type == 2:                           ##### type 2 is yellow
        #todo
        print(" type 2 is yello")
    if type == 3:                           ##### type 3 is blue
        #todo
        print("type 3 is blue")
    if type == 4:                           ##### type 4 is magenta
        #todo
        print("type 4 is magenta")
        
        


def update_black_edges_color(all_grids):
    for j in range(m):
        for i in range(n):
            g = all_grids[j][i]
            if g.is_e12_in_border:
                g.e12.c1 = rec_black
                g.upper_grid.e34.c1 = rec_black
            if g.is_e23_in_border:
                g.e23.c1 = rec_black
                g.righter_grid.e41.c1 = rec_black
            if g.is_e34_in_border:
                g.e34.c1 = rec_black
                g.downer_grid.e12.c1 = rec_black
            if g.is_e41_in_border:
                g.e41.c1 = rec_black
                g.lefter_grid.e23.c1 = rec_black

def update_red_edges_color(all_grids):
    for j in range(m):
        for i in range(n):
            g = all_grids[j][i]
            if g.is_red == True:
                if g.upper_grid is not None and g.upper_grid.is_red == False:
                    g.e12.c1 = rec_red
                    g.upper_grid.e34.c1 = rec_red
                if g.righter_grid is not None and g.righter_grid.is_red == False:
                    g.e23.c1 = rec_red
                    g.righter_grid.e41.c1 = rec_red
                if g.downer_grid is not None and g.downer_grid.is_red == False:
                    g.e34.c1 = rec_red
                    g.downer_grid.e12.c1 = rec_red
                if g.lefter_grid is not None and g.lefter_grid.is_red == False:
                    g.e41.c1 = rec_red
                    g.lefter_grid.e23.c1 = rec_red

def update_yellow_edges_color(all_grids):
    for j in range(m):
        for i in range(n):
            g = all_grids[j][i]
            if g.is_yellow:
                                                            ####  red edge is never black so c1 = red
                if g.upper_grid.is_yellow== False:
                    g.e12.c2 = rec_yellow
                    g.upper_grid.e34.c2 = rec_yellow
                if g.righter_grid.is_yellow== False:
                    g.e23.c2 = rec_yellow
                    g.righter_grid.e41.c2 = rec_yellow
                if g.downer_grid.is_yellow == False:
                    g.e34.c2 = rec_yellow
                    g.downer_grid.e12.c2 = rec_yellow
                if g.lefter_grid is not None and g.lefter_grid.is_yellow== False:
                    g.e41.c2 = rec_yellow
                    g.lefter_grid.e23.c2 = rec_yellow


def rendering(all_grids, m , n):
    update_black_edges_color(all_grids)
    update_yellow_edges_color(all_grids)
    for j in range(m):
        for i in range(n):
            if i %2 ==1:
                if j%2 ==1:
                    pygame.draw.rect(screen, (200,200,200), [shift.x + i*(grid_lenght + w) + w, shift.y + j*(grid_lenght + w) + w, grid_lenght,grid_lenght])
                    pygame.display.update()
                    pygame.time.delay(20)
#                    print(i,j, all_grids[j][i].is_yellow)
                else:
                    pygame.draw.rect(screen, (225,225,225), [shift.x + i*(grid_lenght + w) + w, shift.y + j*(grid_lenght + w) + w, grid_lenght,grid_lenght])
                    pygame.display.update()
                    pygame.time.delay(20)
#                    print(i,j, all_grids[j][i].is_yellow)
            else:
                if j%2 ==1:
                    pygame.draw.rect(screen, (225,225,225), [shift.x + i*(grid_lenght + w) + w, shift.y + j*(grid_lenght + w) + w, grid_lenght,grid_lenght])
                    pygame.display.update()
                    pygame.time.delay(20)
#                    print(i,j, all_grids[j][i].is_yellow)
                else:
                    pygame.draw.rect(screen, (250,250,250), [shift.x + i*(grid_lenght + w) + w, shift.y + j*(grid_lenght + w) + w, grid_lenght,grid_lenght])
                    pygame.display.update()
                    pygame.time.delay(20)
#                    print(i,j, all_grids[j][i].is_yellow)
                    
    for j in range(m):
        for i in range(n):
            c1 = all_grids[j][i].e12.c1
            c2 = all_grids[j][i].e12.c2
            c3 = all_grids[j][i].e41.c1
            c4 = all_grids[j][i].e41.c2
            for u in range(4):
                if u%2 == 0:
                    x1 = vertical_start.x + i*(grid_lenght+w) +  int(grid_lenght/4)*u
                    y1 = vertical_start.y + j*(grid_lenght+w) -1
                    x2 = vertical_start.x + i*(grid_lenght+w) +  int(grid_lenght/4)*(u+1)
                    y2 = vertical_start.y + j*(grid_lenght+w) -1
                    pygame.draw.line(screen, c1, [x1, y1], [x2, y2], w)
                    pygame.display.update()
                    pygame.time.delay(20)

                else:
                    x1 = vertical_start.x + i*(grid_lenght+w) +  int(grid_lenght/4)*u
                    y1 = vertical_start.y + j*(grid_lenght+w) -1
                    x2 = vertical_start.x + i*(grid_lenght+w) +  int(grid_lenght/4)*(u+1)
                    y2 = vertical_start.y + j*(grid_lenght+w) -1
                    pygame.draw.line(screen, c2, [x1, y1], [x2, y2], w)
                    pygame.display.update()
                    pygame.time.delay(20)
                    
                if u%2 == 0:
                    x1 = horizontal_start.x + i*(grid_lenght+w) -1
                    y1 = horizontal_start.y + j*(grid_lenght+w) +int(grid_lenght/4)*u 
                    x2 = horizontal_start.x + i*(grid_lenght+w) -1
                    y2 = horizontal_start.y + j*(grid_lenght+w) +int(grid_lenght/4)*(u+1)
                    pygame.draw.line(screen, c3, [x1, y1], [x2, y2], w)
                    pygame.display.update()
                    pygame.time.delay(20)
                else:
                    x1 = horizontal_start.x + i*(grid_lenght+w) -1
                    y1 = horizontal_start.y + j*(grid_lenght+w) +int(grid_lenght/4)*u
                    x2 = horizontal_start.x + i*(grid_lenght+w) -1
                    y2 = horizontal_start.y + j*(grid_lenght+w) +int(grid_lenght/4)*(u+1)
                    pygame.draw.line(screen, c4, [x1, y1], [x2, y2], w)
                    pygame.display.update()
                    pygame.time.delay(20)
                                        
        

###### inputs
    
m = 14
n = 15
    
bord = board(m,n)

p1 = point(3,3)
p2 = point(4,3)
p3 = point(5,3)
p4 = point(6,3)
p5 = point(6,4)
p6 = point(6,5)
p7 = point(6,6)

p8  = point(7,6)
p9  = point(8,6)
p10 = point(9,6)
p11 = point(9,5)
p12 = point(9,4)
p13 = point(9,3)
p14 = point(10,3)

p15 = point(11,3)
p16 = point(12,3)
p17 = point(12,4)
p18 = point(12,5)
p19 = point(12,6)
p20 = point(12,7)
p21 = point(12,8)

p22 = point(11,8)
p23 = point(10,8)
p24 = point(9,8)
p25 = point(8,8)
p26 = point(8,9)
p27 = point(8,10)
p28 = point(8,11)

p29 = point(7,11)
p30 = point(6,11)
p31 = point(5,11)
p32 = point(4,11)
p33 = point(3,11)
p34 = point(3,10)
p35 = point(3,9)

p36 = point(3,8)
p37 = point(3,7)
p38 = point(3,6)
p39 = point(3,5)
p40 = point(3,4)

border_edges_list = [edge(p40,p1) ,edge(p1,p2) ,edge(p2,p3) ,edge(p3,p4) ,edge(p4,p5) ,edge(p5,p6) ,edge(p6,p7) ,edge(p7,p8) ,edge(p8,p9) ,edge(p9,p10) ,edge(p10,p11) ,edge(p11,p12) ,edge(p12,p13) ,edge(p13,p14) ,edge(p14,p15) ,edge(p15,p16) ,edge(p16,p17) ,edge(p17,p18) ,edge(p18,p19) ,edge(p19,p20) ,edge(p20,p21) ,edge(p21,p22) ,edge(p22,p23) ,edge(p23,p24) ,edge(p24,p25) ,edge(p25,p26) ,edge(p26,p27) ,edge(p27,p28) ,edge(p28,p29) ,edge(p29,p30) ,edge(p30,p31) ,edge(p31,p32) ,edge(p32,p33) ,edge(p33,p34) ,edge(p34,p35) ,edge(p35,p36) ,edge(p36,p37) ,edge(p37,p38) ,edge(p38,p39) ,edge(p39,p40)]

# for edg in border_edges_list:
#     print(edg.p1.x/grid_lenght, edg.p1.y/grid_lenght, edg.p2.x/grid_lenght, edg.p2.y/grid_lenght)
    
find_cycle_borders(all_grids, border_edges_list, m, n)
rendering(all_grids, m, n)




    
    
    
    
    
    