#!/usr/bin/python
# -*- coding: utf-8 -*-



data_h = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]]
data_v = [[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]]



def clear_v():
    for a in range(0,4):
        for b in range(0,5):
            data_v[a][b] = 0
def clear_h():
    for a in range(0,5):
        for b in range(0,4):
            data_h[a][b] = 0

def clear():
    clear_h()
    clear_v()

def find_near_h(a,b):
    clear()
    data_h[a][b] = 1
    if (b-1) >= 0:
        data_h[a][b-1] = 1
    if (b+1) < 4:
        data_h[a][b+1] = 1


    if (a-1) >=0:
        data_v[a-1][b] = 1
        data_v[a-1][b+1] = 1

    if (a) < 4:
        data_v[a][b] = 1
        data_v[a][b+1] = 1
    print_game()


# def print():
#     u,v = edge

def print_blank():
    print("\033[0;31;40m \033[0m", end ="")
def print_light_v():
    print("\033[0;31;40m|\033[0m", end ="")

def print_v():
    print("\033[0;32;40m|\033[0m", end ="")

def print_light_h():
    print("\033[0;31;40m_\033[0m", end ="")

def print_h():
    print("\033[0;32;40m_\033[0m", end ="")

def print_game():
    for h in range(0,5):
        for v in range(0,9):
            index_ = int(v/2)
            if v%2==1:
                if data_h[h][index_] == 1:
                    print_light_h()
                else:
                    print_h()
            else:
                # print (h,index_)
                if h == 0:
                    print_blank()
                else:
                    # print(h-1,index_,data_v[h-1][index_])
                    if data_v[h-1][index_] == 1:
                        print_light_v()
                    else:
                        print_v()
        print(" ")



class Zube:
    #例如empCount就是类变量
    def __init__(self, color,ph, pv):
        self.color = color
        self.point_v = []
        self.point_h = []
        self.hblock = 0
        self.vblock = 0
        self.posx = 0
        self.posy = 0
        self.test_count = 0
        # 0 move right
        # 1 move left
        self.move_direct = 0

        # self.hblock = line
        # self.vblock = col
        self.point_h = ph
        self.point_v = pv
        self.cal_block()
        self.next = -1
    def print_game(self):
        clear()
        for x in self.point_h:
            # print("->",x)
            data_h[x[0]][x[1]] = 1
        for x in self.point_v:
            data_v[x[0]][x[1]] = 1
        print_game()
    def fill_game(self, game):
        for x in self.point_h:
            # print("->",x)
            game.data_h[x[0]][x[1]] = self.color
        for x in self.point_v:
            game.data_v[x[0]][x[1]] = self.color

    def cal_block(self):
        x = 0
        for h in self.point_h:
            x = max(x, h[1])
        self.hblock = x + 1
        x = 0
        for h in self.point_v:
            x = max(h[0], x)
        self.vblock = x + 1

    def dclock90(self):
        newpv=[]
        newph=[]
        for h  in self.point_h:
            # print("from h ", h[0],h[1])
            newpv.append([self.hblock -1 - h[1],h[0]])
            # print("to v ", self.hblock -1 - h[1],h[0])

        for v  in self.point_v:
            # print("from v ", v[0],v[1])
            newph.append([self.hblock - v[1],v[0]])
            # print("to h ", self.hblock - v[1],v[0])
        # print(newph)
        # print(newpv)
        self.point_h = newph
        self.point_v = newpv
        # print(self.point_h)
        # print(self.point_v)

        (self.hblock ,self.vblock) = (self.vblock ,self.hblock)
    def mirror(self):
        for h  in self.point_h:
            h[1] = self.hblock - 1 - h[1]

        for v  in self.point_v:
            v[1] = self.hblock - v[1]
    
    def move_right(self):
        if((self.hblock + self.posx ) < 4):
            for h  in self.point_h:
                h[1] += 1
            for v  in self.point_v:
                v[1] += 1
            self.posx += 1
            return True
        return False

    def move_left(self):
        if self.posx >0:
            for h  in self.point_h:
                h[1] -= 1
            for v  in self.point_v:
                v[1] -= 1
            self.posx -= 1
            return True
        return False


    def move_down(self):
        if((self.vblock + self.posy ) < 4):
            for h  in self.point_h:
                h[0] += 1
            for v  in self.point_v:
                v[0] += 1
            self.posy += 1
            return True
        return False

    def move_head(self):
        if(self.posx >0):
            for h  in self.point_h:
                h[1] -= self.posx
            for v  in self.point_v:
                v[1] -= self.posx
            self.posx =0
        if(self.posy >0):
            for h  in self.point_h:
                h[0] -= self.posy
            for v  in self.point_v:
                v[0] -= self.posy
            self.posy =0
        self.move_direct = 0

    def move_next(self):
        if(self.move_direct == 0):
            if self.move_right():
                return True
            if(self.move_down()):
                self.move_direct = 1
                return True
            return False
        else:
            if(self.move_left()):
                return True
            if(self.move_down()):
                self.move_direct = 0
                return True
            return False
        
    def move_all(self):
        for i in range(0,4):
            ret = True
            while ret:
                print(self.test_count)
                self.test_count+=1
                self.print_game()
                ret = self.move_next()
            self.move_head()
            self.dclock90()

    def test_all_possible(self):
        self.move_all()
        print("mirror")

        self.mirror()
        self.move_all()
        # for i in range(0,4):
        #     ret = True
        #     while ret:
        #         self.print_game()
        #         ret = self.move_next()
        #     self.dclock90()




        # print(self.hblock ,self.vblock)
    def testRotate(self):
        self.print_game()
        self.dclock90()
        self.print_game()
        self.dclock90()
        self.print_game()
        self.dclock90()
        self.print_game()

        c.mirror()
        c.print_game()
        self.dclock90()
        self.print_game()
        self.dclock90()
        self.print_game()
        self.dclock90()
        self.print_game()

class Game:
    def __init__(self):
        self.data_h = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.data_v = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]


        self.colortype = ((40,37),(40,31),(40,32),(40,33),(40,34),(40,35),(45,31),(45,32),(45,33),(45,34),(45,35))
        self.allcube = []
        # L
        self.allcube.append(Zube(1,[[0,0],[0,1],[0,2]],[[0,0]]))
        # T
        self.allcube.append(Zube(2,[[0,0],[0,1],[0,2]],[[0,1]]))
        # X
        self.allcube.append(Zube(3,[[1,0],[1,1]],[[0,1],[1,1]]))
        # U
        self.allcube.append(Zube(4,[[1,0],[1,1]],[[0,0],[0,2]]))
        # F
        self.allcube.append(Zube(5,[[1,0],[1,1]],[[0,0],[0,1]]))
        # 4
        self.allcube.append(Zube(6,[[0,0],[1,0],[1,1]],[[0,1]]))
        # W
        self.allcube.append(Zube(7,[[1,0],[0,1]],[[0,1],[1,0]]))
        # t
        self.allcube.append(Zube(8,[[1,0],[1,1]],[[0,1],[1,0]]))
        # ?
        self.allcube.append(Zube(9,[[0,0],[1,0]],[[1,0],[0,1]]))
        # l
        self.allcube.append(Zube(10,[[2,0]],[[0,0],[1,0],[1,1]]))
    def play(self):
        playing_data_h = copy.deepcopy(self.data_h)
        playing_data_v = copy.deepcopy(self.data_v)
        allcube[0].fill_game(self)


    def fillin(self, cube):
        cube.fill_game(self)


    def clear(self):
        for x in self.data_h:
            for y in x:
                y = 0
        for x in self.data_v:
            for y in x:
                y = 0
    def clear0(self):
        self.data_h = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.data_v = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    
    def print_char(self,c,color):
        A = "\033[0;" + str(self.colortype[color][1]) + ";" + str(self.colortype[color][0]) + "m" + c + "\033[0m"
        print(A, end ="")

    def test(self):
        for cube in allcube:
            self.clear0()
            cube.fill_game(self)
            self.print_game()
    
    def print_game(self):
        for h in range(0,5):
            for v in range(0,9):
                index_ = int(v/2)
                if v%2==1:
                    self.print_char('_',self.data_h[h][index_])
                else:
                    # print (h,index_)
                    if h == 0:
                        print_blank()
                    else:
                        self.print_char('|',self.data_v[h-1][index_])
            print(" ")


if __name__ == '__main__':

    allcube = []
    # L
    allcube.append(Zube(1,[[0,0],[0,1],[0,2]],[[0,0]]))
    # T
    allcube.append(Zube(2,[[0,0],[0,1],[0,2]],[[0,1]]))
    # X
    allcube.append(Zube(3,[[1,0],[1,1]],[[0,1],[1,1]]))
    # U
    allcube.append(Zube(4,[[1,0],[1,1]],[[0,0],[0,2]]))
    # F
    allcube.append(Zube(5,[[1,0],[1,1]],[[0,0],[0,1]]))
    # 4
    allcube.append(Zube(6,[[0,0],[1,0],[1,1]],[[0,1]]))
    # W
    allcube.append(Zube(7,[[1,0],[0,1]],[[0,1],[1,0]]))
    # t
    allcube.append(Zube(8,[[1,0],[1,1]],[[0,1],[1,0]]))
    # ?
    allcube.append(Zube(9,[[0,0],[1,0]],[[1,0],[0,1]]))
    # l
    allcube.append(Zube(10,[[2,0]],[[0,0],[1,0],[1,1]]))
     
    # for c in allcube:
    #     c.print_game()
    
    # A = "\033[0;"
    # B = ";40mM\033[0m"
    # for i in range(30,38):
    #     C = str(i)
    #     D = "SS" + A + C + B
    #     print(D)
    # g = Game()
    # g.test()

    allcube[9].test_all_possible()



