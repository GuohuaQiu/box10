
from panel import Panel

from zube_status import ZubeStatus

class Zube:
    def __init__(self, color,ph, pv, pm):
        self.can_mirror = 1
        self.can_rotate = 1
        self.color = color
        self.status = ZubeStatus(ph,pv,pm)
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

        self.allstatus = {color:[]}
    @staticmethod
    def log_on():
        return False

    def find_all_status(self, panel):
        self.dump_all_status("before find_all_status")
        self.reset()
        count = 0
        ret = True
        while ret:
            self.status.id += 1
            if self.fill_panel(panel):
                self.allstatus[self.color].append(ZubeStatus.copy(self.status))
                # panel.print_game()
                count += 1
                # print ("show " ,count)
                self.clear_panel(panel)
            ret = self.move_next()

        print("color", self.color, "has",count,"candicate")
        self.dump_all_status("end find_all_status")

    def fail_head(self):
        self.dump_all_status("before fail head")

        if len(self.allstatus[self.color]) == 0:
            print("error 234623")
            return
        # else:
        #     print (self.allstatus[self.color])
        if self.allstatus.get(0) is None:
            self.allstatus[0] = [self.status]
        else:
            self.allstatus[0].append(self.status)
        self.allstatus[self.color].pop(0)

        self.dump_all_status("end fail head")

    def take(self):
        if len(self.allstatus[self.color]) > 0:
            self.status = self.allstatus[self.color][0]
            if Zube.log_on():
                print(self.color," take ",self.status.id)
            return True
        return False
    def restore_failed(self):
        self.dump_all_status("before restore_failed")
        if self.allstatus.get(0):
            self.allstatus[self.color]  += self.allstatus[0]
            self.allstatus[0] = []
        self.dump_all_status("end restore_failed")

    def dump_all_status(self,str):
        if Zube.log_on() == False:
            return
        print(str)
        print("zube:", self.color, "{",end ="")


        for x in self.allstatus.items():
            print(" color:",x[0],"count",len(x[1]),"[",end ="")
            for s in x[1]:
                print(s.id,",",end ="")
            print("]", end ="")

        print ("}")
    # return if self.allstatus[self.color] is None
    def touch(self, c):
        self.dump_all_status("before touch")

        self.allstatus[c.color] = []
        count = 0
        for status in self.allstatus[self.color]:
            if status.overlap(c.status):
                self.allstatus[c.color].append(status)
                count+=1
        if Zube.log_on():
            print("There are overlaps ",count,"between",c.color,self.color)
        for status in self.allstatus[c.color]:
            self.allstatus[self.color].remove(status)

        self.dump_all_status("end touch")
        if len(self.allstatus[self.color]) == 0:
            return False
        return True

    # return if self.allstatus[self.color] is None
    def untouch(self, c):
        self.dump_all_status("before untouch")
        if Zube.log_on():
            print(self.color,"<-clear", c.color)
        if self.allstatus.get(c.color) is None:
            return True
        self.allstatus[self.color] = self.allstatus[self.color] + self.allstatus[c.color]
        self.allstatus[c.color] = []
        self.dump_all_status("end untouch")

        return True




    def print_game(self):
        panel = Panel()
        panel.clear()
        self.fill_panel(panel)

        panel.print_game()

    def fill_panel(self, panel):
        ph = panel.data_h
        pv = panel.data_v
        pm = panel.data_m
        for x in self.status.point_h:
            if ph[x[0]][x[1]] != 0:
                # print("e:",x[0],x[1],"->",ph[x[0]][x[1]])
                return False
        for x in self.status.point_v:
            if pv[x[0]][x[1]] != 0:
                # print("ve:",x[0],x[1],"->",pv[x[0]][x[1]])
                return False
        for x in self.status.point_m:
            if pm[x[0]][x[1]] != 0:
                # print("me:",x[0],x[1],"->",pm[x[0]][x[1]])
                return False

        for x in self.status.point_h:
            ph[x[0]][x[1]] = self.color
        for x in self.status.point_v:
            pv[x[0]][x[1]] = self.color
        for x in self.status.point_m:
            pm[x[0]][x[1]] = self.color
        return True

    def clear_panel(self, panel):
        ph = panel.data_h
        pv = panel.data_v
        pm = panel.data_m
        for x in self.status.point_h:
            ph[x[0]][x[1]] = 0
        for x in self.status.point_v:
            pv[x[0]][x[1]] = 0
        for x in self.status.point_m:
            pm[x[0]][x[1]] = 0

    def cal_block(self):
        x = 0
        for h in self.status.point_h:
            x = max(x, h[1])
        self.hblock = x + 1
        x = 0
        for h in self.status.point_v:
            x = max(h[0], x)
        self.vblock = x + 1

    def dclock90(self):
        newpv=[]
        newph=[]
        newpm=[]
        for h  in self.status.point_h:
            # print("from h ", h[0],h[1])
            newpv.append([self.hblock -1 - h[1],h[0]])
            # print("to v ", self.hblock -1 - h[1],h[0])

        for v  in self.status.point_v:
            # print("from v ", v[0],v[1])
            newph.append([self.hblock - v[1],v[0]])
            # print("to h ", self.hblock - v[1],v[0])
        for v  in self.status.point_m:
            # print("from v ", v[0],v[1])
            newpm.append([self.hblock - v[1],v[0]])
            # print("to h ", self.hblock - v[1],v[0])

        self.status.point_h = newph
        self.status.point_v = newpv
        self.status.point_m = newpm

        self.angle +=1
        # print(self.status.point_h)
        # print(self.status.point_v)

        (self.hblock ,self.vblock) = (self.vblock ,self.hblock)
    def set_can_mirror(self, m):
        self.can_mirror = m
        # print("set can mirror:",self.can_mirror)
    def set_can_rotate(self, m):
        self.can_rotate = m
    def mirror(self):
        for h  in self.status.point_h:
            h[1] = self.hblock - 1 - h[1]

        for v  in self.status.point_v:
            v[1] = self.hblock - v[1]
        for v  in self.status.point_m:
            v[1] = self.hblock - v[1]
        self.mirrored = 1
        self.angle = 0

    def move_right(self):
        if((self.hblock + self.posx ) < 4):
            for h  in self.status.point_h:
                h[1] += 1
            for v  in self.status.point_v:
                v[1] += 1
            for v  in self.status.point_m:
                v[1] += 1
            self.posx += 1
            return True
        return False

    def move_left(self):
        if self.posx >0:
            for h  in self.status.point_h:
                h[1] -= 1
            for v  in self.status.point_v:
                v[1] -= 1
            for v  in self.status.point_m:
                v[1] -= 1
            self.posx -= 1
            return True
        return False


    def move_down(self):
        if((self.vblock + self.posy ) < 4):
            for h  in self.status.point_h:
                h[0] += 1
            for v  in self.status.point_v:
                v[0] += 1
            for v  in self.status.point_m:
                v[0] += 1
            self.posy += 1
            return True
        return False

    def reset(self):
        self.mirrored = 0
        self.angle = 0
        self.move_head()
        self.status.id = 0

    def move_head(self):
        if(self.posx >0):
            for h  in self.status.point_h:
                h[1] -= self.posx
            for v  in self.status.point_v:
                v[1] -= self.posx
            for v  in self.status.point_m:
                v[1] -= self.posx
            self.posx =0
        if(self.posy >0):
            for h  in self.status.point_h:
                h[0] -= self.posy
            for v  in self.status.point_v:
                v[0] -= self.posy
            for v  in self.status.point_m:
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