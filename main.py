#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

data_h = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]]
data_v = [[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]]
data_m = [[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]]



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
    print("\033[0;31;40m \033[0m", end = "")
def print_light_v():
    print("\033[0;31;40m|\033[0m", end = "")

def print_v():
    print("\033[0;32;40m|\033[0m", end = "")

def print_light_h():
    print("\033[0;31;40m_\033[0m", end = "")

def print_h():
    print("\033[0;32;40m_\033[0m", end = "")

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
    def __init__(self, color,ph, pv, pm):
        self.can_mirror = 1
        self.can_rotate = 1
        self.color = color
        self.point_h = ph
        self.point_v = pv
        self.point_m = pm
        self.hblock = 0
        self.vblock = 0
        self.posx = 0
        self.posy = 0
        self.test_count = 0
        # 0 move right
        # 1 move left
        self.move_direct = 0

        self.cal_block()
        self.next = None
        self.prev = None

        self.angle = 0
        self.mirrored = 0
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
            if game.data_h[x[0]][x[1]] != 0:
                return False
        for x in self.point_v:
            if game.data_h[x[0]][x[1]] != 0:
                return False
        for x in self.point_h:
            # print("->",x)
            game.data_h[x[0]][x[1]] = self.color
        for x in self.point_v:
            game.data_v[x[0]][x[1]] = self.color
        return True
    def fill_panel(self, ph, pv, pm):
        for x in self.point_h:
            if ph[x[0]][x[1]] != 0:
                return False
        for x in self.point_v:
            if pv[x[0]][x[1]] != 0:
                return False
        for x in self.point_m:
            if pm[x[0]][x[1]] != 0:
                return False
                
        for x in self.point_h:
            ph[x[0]][x[1]] = self.color
        for x in self.point_v:
            pv[x[0]][x[1]] = self.color
        for x in self.point_m:
            pm[x[0]][x[1]] = self.color
        return True

    def clear_panel(self, ph, pv, pm):
        for x in self.point_h:
            ph[x[0]][x[1]] = 0
        for x in self.point_v:
            pv[x[0]][x[1]] = 0
        for x in self.point_m:
            pm[x[0]][x[1]] = 0

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
        newpm=[]
        for h  in self.point_h:
            # print("from h ", h[0],h[1])
            newpv.append([self.hblock -1 - h[1],h[0]])
            # print("to v ", self.hblock -1 - h[1],h[0])

        for v  in self.point_v:
            # print("from v ", v[0],v[1])
            newph.append([self.hblock - v[1],v[0]])
            # print("to h ", self.hblock - v[1],v[0])
        for v  in self.point_m:
            # print("from v ", v[0],v[1])
            newpm.append([self.hblock - v[1],v[0]])
            # print("to h ", self.hblock - v[1],v[0])

        self.point_h = newph
        self.point_v = newpv
        self.point_m = newpm

        self.angle +=1
        # print(self.point_h)
        # print(self.point_v)

        (self.hblock ,self.vblock) = (self.vblock ,self.hblock)
    def set_can_mirror(self, m):
        self.can_mirror = m
        # print("set can mirror:",self.can_mirror)
    def set_can_rotate(self, m):
        self.can_rotate = m
    def mirror(self):
        for h  in self.point_h:
            h[1] = self.hblock - 1 - h[1]

        for v  in self.point_v:
            v[1] = self.hblock - v[1]
        for v  in self.point_m:
            v[1] = self.hblock - v[1]
        self.mirrored = 1
        self.angle = 0
    
    def move_right(self):
        if((self.hblock + self.posx ) < 4):
            for h  in self.point_h:
                h[1] += 1
            for v  in self.point_v:
                v[1] += 1
            for v  in self.point_m:
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
            for v  in self.point_m:
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
            for v  in self.point_m:
                v[0] += 1
            self.posy += 1
            return True
        return False

    def reset(self):
        self.mirrored = 0 
        self.angle = 0
        self.move_head()       

    def move_head(self):
        if(self.posx >0):
            for h  in self.point_h:
                h[1] -= self.posx
            for v  in self.point_v:
                v[1] -= self.posx
            for v  in self.point_m:
                v[1] -= self.posx
            self.posx =0
        if(self.posy >0):
            for h  in self.point_h:
                h[0] -= self.posy
            for v  in self.point_v:
                v[0] -= self.posy
            for v  in self.point_m:
                v[0] -= self.posy
            self.posy =0
        self.move_direct = 0
    

    def move_next_in_one_direct(self):
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
    def move_next(self):
        if self.move_next_in_one_direct():
            return True
        if self.can_rotate == 0:
            return False
        if self.angle >= 3:
            # print("can mirror:",self.can_mirror)
            if self.mirrored == 0 and self.can_mirror:
                self.move_head()
                # self.print_game()
                self.mirror()
                return True  
            return False
        self.move_head()
        self.dclock90()
        
        return True

        
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
        self.reset()
        count = 0
        while True:
            self.print_game()
            if self.move_next():
                count += 1
                print(count,self.mirrored,self.angle,self.move_direct)
                continue
            else:
                break

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
        self.data_m = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

        self.godown = 1
        self.head = None
        self.work_cube = None


        self.colortype = ((40,37),(40,31),(40,32),(40,33),(40,34),(40,35),(42,31),(43,32),(44,33),(45,34),(46,35))
        self.allcube = []
        # L
        self.allcube.append(Zube(1,[[0,0],[0,1],[0,2]],[[0,0]],[[0,1],[0,2]]))
        # T
        self.allcube.append(Zube(2,[[0,0],[0,1],[0,2]],[[0,1]],[[0,1],[0,2]]))
        # X
        self.allcube.append(Zube(3,[[1,0],[1,1]],[[0,1],[1,1]],[[1,1]]))
        self.allcube[2].set_can_mirror(0)
        self.allcube[2].set_can_rotate(0)
        # U
        self.allcube.append(Zube(4,[[1,0],[1,1]],[[0,0],[0,2]],[[0,1]]))
        self.allcube[3].set_can_mirror(0)
        # F
        self.allcube.append(Zube(5,[[1,0],[1,1]],[[0,0],[0,1]],[[1,1]]))
        # 4
        self.allcube.append(Zube(6,[[0,0],[1,0],[1,1]],[[0,1]],[[1,1]]))
        # W
        self.allcube.append(Zube(7,[[1,0],[0,1]],[[0,1],[1,0]],[[1,1]]))
        self.allcube[6].set_can_mirror(0)
        # t
        self.allcube.append(Zube(8,[[1,0],[1,1]],[[0,1],[1,0]],[[1,1]]))
        # ?
        self.allcube.append(Zube(9,[[0,0],[1,0]],[[1,0],[0,1]],[]))
        # l
        self.allcube.append(Zube(10,[[2,0]],[[0,0],[1,0],[1,1]],[[1,0]]))
    def play(self, to_locate):

        start_time = time.time()

        playing_data_h = (self.data_h)
        playing_data_v = (self.data_v)        
        playing_data_m = (self.data_m)        


        self.head = None

        base = None
        for i in to_locate:
            if self.head is None:
                self.head = self.allcube[i]
                base = self.head
            else:
                base.next = self.allcube[i]
                self.allcube[i].prev = base
                base = self.allcube[i]
        while True:
            base.print_game()
            base = base.prev
            if base is None:
                break

        self.print_game()

        self.godown = 1
        self.work_cube = self.head
        print("Start playing...")

        max = 0

        count = 0

        while True:
            if self.godown == 0:
                self.work_cube.clear_panel(playing_data_h,playing_data_v,playing_data_m)
                # print(self.work_cube.color, "clear panel.")
                count -= 1
                if self.work_cube.move_next() == False:
                    # print(self.work_cube.color, "no place to locate...")
                    self.work_cube = self.work_cube.prev
                    if (self.work_cube is None):
                        print("all is tried. Error")
                        return
                    continue                   

            while True:
                if self.work_cube.fill_panel(playing_data_h,playing_data_v,playing_data_m):
                    # print(self.work_cube.color, "fill panel.")
                    if self.work_cube.next is None:
                        print("Success")
                        self.print_game()
                        end_time = time.time()    
                        print("Total time:",end_time-start_time)
                        return
                    self.work_cube = self.work_cube.next
                    self.work_cube.reset()
                    self.godown = 1
                    count += 1
                    if (count>max):
                        max = count
                        self.print_game()
                    break
                  
                else:
                    if self.work_cube.move_next():
                        # print(self.work_cube.color, self.work_cube.mirrored, self.work_cube.angle ,"move next.")
                        continue
                    else:
                        self.work_cube.move_head()
                        print(self.work_cube.color, "no place to locate.")
                        self.work_cube = self.work_cube.prev
                        if (self.work_cube is None):
                            print("Error")
                            return
                        self.godown = 0
                        break

     


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

    # def test(self):
    #     for cube in allcube:
    #         self.clear0()
    #         cube.fill_game(self)
    #         self.print_game()
    
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
    def test_10(self):
        self.allcube[0].dclock90()
        self.allcube[1].mirror()
        # self.allcube[2].move_right()
        self.allcube[3].move_down()
        self.allcube[3].move_down()
        self.allcube[3].move_down()

        self.allcube[7].dclock90()
        self.allcube[7].dclock90()
        self.allcube[7].dclock90()

        self.allcube[7].move_down()
        self.allcube[7].move_down()

        self.allcube[8].dclock90()
        self.allcube[8].dclock90()
        self.allcube[8].dclock90()
        self.allcube[8].move_down()
        self.allcube[8].move_down()
        self.allcube[8].move_right()

        playing_data_h = (self.data_h)
        playing_data_v = (self.data_v)        
        playing_data_m = (self.data_m)        

        self.allcube[0].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[1].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[2].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[3].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[7].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[8].fill_panel(playing_data_h,playing_data_v,playing_data_m)

        self.play([4,5,6,9])
        self.print_game()
    def test_24(self):
        self.allcube[3].dclock90()
        self.allcube[3].dclock90()
        self.allcube[2].move_right()
        self.allcube[2].move_down()
        playing_data_h = (self.data_h)
        playing_data_v = (self.data_v)        
        playing_data_m = (self.data_m)        
        self.allcube[2].fill_panel(playing_data_h,playing_data_v,playing_data_m)
        self.allcube[3].fill_panel(playing_data_h,playing_data_v,playing_data_m)


        
        self.play([0,7,8,9,1,4,5,6])
        self.print_game()



if __name__ == '__main__':

    g = Game()
    g.test_10()

     
    # g.allcube[6].test_all_possible()




