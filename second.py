#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from zube import Zube
from panel import Panel

class Game:
    def __init__(self):
        self.panel = Panel()
        self.head = None

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

    def clear_this_color(self, head):
        cube = head.next
        while cube is not None:
            cube.untouch(head)
            cube = cube.next

    @staticmethod
    def log_on():
        return False


    def mark_this_color(self, head):
        cube = head.next
        # mark all status according to head position.
        while cube is not None:
            if cube.touch(head) == False:
                return False
            cube = cube.next
        return True



    def play(self, to_locate):

        start_time = time.time()

        self.head = None

        base = None
        print("Start listing...")
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
        print("Start enuming...")
        base = self.head
        while True:
            base.print_game()
            base.find_all_status(self.panel)
            print("all status ", base.color, len(base.allstatus[base.color]))
            base = base.next
            if base is None:
                break
        # return

        self.panel.print_game()

        print("Start playing...")
        # return

        # max = 0
        # count = 0

        # 0 prev one
        # 1 next one
        # 2 mark sub
        # 3 clear sub
        # 4 take
        # 5 up to this , sub fail

        flag = 4
        success = False
        work_cube = self.head

        while flag != -1:
            if flag == 0:
                if work_cube.prev:
                    work_cube = work_cube.prev
                    work_cube.fail_head()
                    if Game.log_on():
                        print("flag->4 up to prev ok to take ",work_cube.color)
                    flag = 4
                else:
                    print("all is tried. Error")
                    break
            elif flag == 4:
                self.clear_this_color(work_cube)
                if work_cube.take():
                    if Game.log_on():
                        print("flag->2 ",work_cube.color, " take success ",work_cube.status.id,",to mark sub", )

                    flag = 2
                else:
                    if Game.log_on():
                        print("flag->0 ", work_cube.color, " take fail restore failed and move to up")
                    work_cube.restore_failed()

                    flag = 0
            elif flag == 1:
                if work_cube.next:
                    work_cube = work_cube.next
                    if Game.log_on():
                        print("flag->4 down to next ok ,to take ",work_cube.color)
                    flag = 4
                else:
                    if Game.log_on():
                        print("sucess all is marked. ",work_cube.color)
                    success = True
                    break
            elif flag == 2:
                if self.mark_this_color(work_cube):
                    if Game.log_on():
                        print("flag->1 mark success , goto next color ",work_cube.color)
                    flag = 1
                else:
                    work_cube.fail_head()
                    if Game.log_on():
                        print("flag->4 mark fail ",work_cube.color)
                    flag = 4


        print("test:")
        self.panel.print_game()
        if success:
            work_cube = self.head
            if self.head is None:
                print("error !")
            while work_cube is not None:
                work_cube.fill_panel(self.panel)
                print("add color",work_cube.color,"pos", work_cube.status.id)
                work_cube.print_game()
                self.panel.print_game()
                work_cube = work_cube.next
            print("final:")
            self.panel.print_game()
            print("Total time:", time.time() - start_time)
            return


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



        # self.play([0,7,8,9,1,4,5,6])
        self.play([0,1,4,5,6,7,8,9])
        self.panel.print_game()
    def test_24_x(self):
        self.allcube[3].dclock90()
        self.allcube[3].dclock90()
        self.allcube[2].move_right()
        self.allcube[2].move_down()
        self.allcube[0].move_right()
        self.allcube[0].move_down()

        self.allcube[5].dclock90()
        self.allcube[5].dclock90()
        self.allcube[5].dclock90()
        self.allcube[5].move_right()
        self.allcube[5].move_right()
        self.allcube[5].move_right()
        self.allcube[5].move_down()

        self.allcube[4].dclock90()
        self.allcube[4].dclock90()
        self.allcube[4].move_right()
        self.allcube[4].move_right()


        # self.allcube[1].dclock90()
        # self.allcube[1].move_down()
        #
        # self.allcube[1].fill_panel(self.panel)
        self.allcube[0].fill_panel(self.panel)
        self.allcube[2].fill_panel(self.panel)
        self.allcube[3].fill_panel(self.panel)
        self.allcube[4].fill_panel(self.panel)
        self.allcube[5].fill_panel(self.panel)



        # self.play([0,7,8,9,1,4,5,6])
        self.play([1,6,7,8,9])
        self.panel.print_game()



if __name__ == '__main__':



    g = Game()
    g.test_24()




    # g.allcube[5].test_all_possible()




