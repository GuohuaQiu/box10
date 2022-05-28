
class Panel:
    colortype = (
    (40, 37), (40, 31), (40, 32), (40, 33), (40, 34), (40, 35), (42, 31), (43, 32), (44, 33), (45, 34), (46, 35))
    def __init__(self):
        self.data_h = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.data_v = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.data_m = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]


    def clear_v(self):
        for a in range(0,4):
            for b in range(0,5):
               self.data_v[a][b] = 0
    def clear_h(self):
        for a in range(0,5):
            for b in range(0,4):
               self.data_h[a][b] = 0
    def clear_m(self):
        for a in range(0,5):
            for b in range(0,5):
               self.data_m[a][b] = 0

    def clear(self):
        self.clear_h()
        self.clear_v()
        self.clear_m()

    def find_near_h(self,a,b):
        self.clear()
        self.data_h[a][b] = 1
        if (b-1) >= 0:
            self.data_h[a][b-1] = 1
        if (b+1) < 4:
            self.data_h[a][b+1] = 1
    
    
        if (a-1) >=0:
            self.data_v[a-1][b] = 1
            self.data_v[a-1][b+1] = 1
    
        if (a) < 4:
            self.data_v[a][b] = 1
            self.data_v[a][b+1] = 1
        self.print_game()
    @staticmethod
    def print_blank():
        print("\033[0;31;40m \033[0m", end = "")

    @staticmethod
    def print_light_v():
        print("\033[0;31;40m|\033[0m", end = "")

    @staticmethod
    def print_v():
        print("\033[0;32;40m|\033[0m", end = "")

    @staticmethod
    def print_light_h():
        print("\033[0;31;40m_\033[0m", end = "")

    @staticmethod
    def print_h():
        print("\033[0;32;40m_\033[0m", end = "")

    def clear0(self):
        self.data_h = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.data_v = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.data_m = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    @staticmethod
    def print_char(c,color):
        A = "\033[0;" + str(Panel.colortype[color][1]) + ";" + str(Panel.colortype[color][0]) + "m" + c + "\033[0m"
        print(A, end ="")


    def print_game(self):
        for h in range(0,5):
            for v in range(0,9):
                index_ = int(v/2)
                if v%2==1:
                    Panel.print_char('_',self.data_h[h][index_])
                else:
                    # print (h,index_)
                    if h == 0:
                        Panel.print_blank()
                    else:
                        Panel.print_char('|',self.data_v[h-1][index_])
            print(" ")
        for a in self.data_m:
            print(a)




    # def print_game(self):
    #     for h in range(0,5):
    #         for v in range(0,9):
    #             index_ = int(v/2)
    #             if v%2==1:
    #                 if self.data_h[h][index_] == 1:
    #                     Panel.print_light_h()
    #                 else:
    #                     Panel.print_h()
    #             else:
    #                 # print (h,index_)
    #                 if h == 0:
    #                     Panel.print_blank()
    #                 else:
    #                     # print(h-1,index_,self.data_v[h-1][index_])
    #                     if self.data_v[h-1][index_] == 1:
    #                         Panel.print_light_v()
    #                     else:
    #                         Panel.print_v()
    #         print(" ")
    #     for a in self.data_m:
    #         print(a)