class My_Windows:
    def __init__(self):
        self.win_input = None
        self.win_menu = None
        self.win_result = None


class Country:
    def __init__(self, no):
        self.no = no  # 国家编号 index+1       #1
        self.score = 0  # 国家总分              #7
        self.man_score = 0  # 男团总分          #1
        self.woman_score = 0  # 女团总分        #6
        self.rank = []  # 每个项目的名次        #[5,0,0,2,3]


class Event:
    def __init__(self, no, top):
        self.no = no  # 项目编号 index+1          #1
        self.top = top  # 项目名次3/5             #5
        self.type = ""  # 男子man/女子项目woman   #'man'
        self.rank = []  # [1,2,3,4,5]


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()
