#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from zube import Zube
from panel import Panel

class Game:
    def __init__(self):
        self.panel = Panel()
        self.godown = 1
        self.head = None
        self.work_cube = None

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
        self.allcube.append(Zube(4,[[1,0],[1,1]],[[0,0],[0,2]],[[1,1]]))
        self.allcube[3].set_can_mirror(0)
        # F
        self.allcube.append(Zube(5,[[1,0],[1,1]],[[0,0],[0,1]],[[1,1]]))
        # 4
        self.allcube.append(Zube(6,[[0,0],[1,0],[1,1]],[[0,1]],[[1,1]]))
        # W
        self.allcube.append(Zube(7,[[1,0],[0,1]],[[0,1],[1,0]],[]))
        self.allcube[6].set_can_mirror(0)
        # t
        self.allcube.append(Zube(8,[[1,0],[1,1]],[[0,1],[1,0]],[[1,1]]))
        # ?
        self.allcube.append(Zube(9,[[0,0],[1,0]],[[1,0],[0,1]],[]))
        # l
        self.allcube.append(Zube(10,[[2,0]],[[0,0],[1,0],[1,1]],[[1,0]]))

    @staticmethod
    def log_on():
        return False

    def play(self, to_locate):

        start_time = time.time()

        self.head = None

        base = None
        for i in to_locate:
            if self.head is None:
                self.head = self.allcube[i]
                base = self.head
                base.prev = None
            else:
                base.next = self.allcube[i]
                self.allcube[i].prev = base
                base = self.allcube[i]
        base.next = None
        while True:
            base.print_game()
            base = base.prev
            if base is None:
                break

        self.panel.print_game()

        self.godown = 1
        self.work_cube = self.head
        print("Start playing...")

        max = 0

        count = 0

        while True:
            if self.godown == 0:
                self.work_cube.clear_panel(self.panel)
                if Game.log_on():
                    print(self.work_cube.color, "clear panel.")
                count -= 1
                if self.work_cube.move_next() == False:
                    if Game.log_on():
                        print(self.work_cube.color, "no place to locate...")
                    temp = self.work_cube
                    self.work_cube = self.work_cube.prev
                    if (self.work_cube is None):
                        print("this is last tried.")
                        temp.panel.print_game()
                        print("this is head.")
                        print("all is tried. Error")
                        return
                    continue

            while True:
                if self.work_cube.fill_panel(self.panel):
                    if Game.log_on():
                        print(self.work_cube.color, "fill panel.")
                    if self.work_cube.next is None:
                        print("Success")
                        self.panel.print_game()
                        end_time = time.time()
                        print("Total time:",end_time-start_time)
                        return
                    self.work_cube = self.work_cube.next
                    self.work_cube.reset()
                    self.godown = 1
                    count += 1
                    if (count>max):
                        max = count
                        self.panel.print_game()
                    break

                else:
                    if self.work_cube.move_next():
                        # print(self.work_cube.color, self.work_cube.mirrored, self.work_cube.angle ,"move next.")
                        continue
                    else:
                        self.work_cube.move_head()

                        if Game.log_on():
                            print(self.work_cube.color, "no place to locate.")
                        self.work_cube = self.work_cube.prev
                        if (self.work_cube is None):
                            print("Error")
                            return
                        self.godown = 0
                        break



    def test_10(self):
        self.allcube[0].dclock90()
        self.allcube[1].mirror()
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

        self.allcube[0].fill_panel(self.panel)
        self.allcube[1].fill_panel(self.panel)
        self.allcube[2].fill_panel(self.panel)
        self.allcube[3].fill_panel(self.panel)
        self.allcube[7].fill_panel(self.panel)
        self.allcube[8].fill_panel(self.panel)
        print("Test:")
        self.panel.print_game()
        # return

        self.play([4,5,6,9])
        self.panel.print_game()
    def test_24(self):
        self.allcube[3].dclock90()
        self.allcube[3].dclock90()
        self.allcube[2].move_right()
        self.allcube[2].move_down()

        self.allcube[2].fill_panel(self.panel)
        self.allcube[3].fill_panel(self.panel)



        self.play([0,7,8,9,1,4,5,6])
        self.panel.print_game()



if __name__ == '__main__':

    g = Game()
    g.test_24()


    # g.allcube[6].test_all_possible()




