from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QGraphicsPixmapItem, QGraphicsScene, QLabel
from PySide2.QtCore import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon, QPixmap, QImage
from def_Olympics import Country, Event, My_Windows,CommonHelper

# 全局变量
EVENT_SCORE_5 = [7, 5, 3, 2, 1]
EVENT_SCORE_3 = [5, 3, 2]
EVENT_LIST = []
COUNTRY_LIST = []


# 排序函数
# 1. 编号排序
def key_no(c):
    return c.no


# 2. 总分排序
def key_score(c):
    return c.score


# 3. 男团排序
def key_man(c):
    return c.man_score


# 4. 女团排序
def key_woman(c):
    return c.woman_score


# 计算国家类项目数据
def cal_score(var_country):
    index = 0
    for r in var_country.rank:
        if r == 0:
            index += 1
            continue
        if EVENT_LIST[index].type == 'man':  # 男子项目
            if EVENT_LIST[index].top == 3:
                var_country.man_score += EVENT_SCORE_3[r - 1]
            else:
                var_country.man_score += EVENT_SCORE_5[r - 1]
        else:  # 女子项目
            if EVENT_LIST[index].top == 3:
                var_country.woman_score += EVENT_SCORE_3[r - 1]
            else:
                var_country.woman_score += EVENT_SCORE_5[r - 1]
        index += 1
    var_country.score = var_country.man_score + var_country.woman_score


def cal_country():
    # 名次表
    for e in EVENT_LIST:
        for r in e.rank:
            COUNTRY_LIST[r - 1].rank[EVENT_LIST.index(e)] = e.rank.index(r) + 1
    for c in COUNTRY_LIST:
        cal_score(c)


# 输入窗口类
class Win_input:
    def __init__(self):
        self.ui = QUiLoader().load("ui/input.ui")
        self.ui.label.setPixmap(QPixmap("./image/baby.png"))
        # 提交数据处理函数
        self.ui.pushButton.clicked.connect(self.handle_data)

    def handle_data(self):  # 确认提交button后,处理数据,并判断其合法性
        country_num = self.ui.country_num.value()
        man_num = self.ui.man_num.value()
        woman_num = self.ui.woman_num.value()
        info = self.ui.plainTextEdit.toPlainText().splitlines()
        if country_num <= 0:
            QMessageBox.critical(self.ui, "错误", "参赛国家数应为正整数!")
            return
        if man_num < 0 or woman_num < 0 or man_num + woman_num == 0:
            QMessageBox.critical(self.ui, "错误", "项目数应为非负整数且男女项目总和应为正整数!")
            return
        if len(info) != man_num + woman_num:
            QMessageBox.critical(self.ui, "错误", "项目名次数据与项目数不匹配!")
            return
        index = 1
        for i in info:
            temp_list = i.strip().split()
            if len(temp_list) != 3 and len(temp_list) != 5:
                QMessageBox.critical(self.ui, "错误", "项目名次只能选取3或5!")
                return

            for t in temp_list:
                if t.strip():
                    try:
                        data = int(t)
                        if data < 1 or data > country_num:  # 不在范围内
                            QMessageBox.critical(self.ui, "错误", "名次中编号有误!")
                            return
                    except ValueError:  # 非整型数字
                        QMessageBox.critical(self.ui, "错误", "含有非整型数据!")
                        return
            # 建立项目列表
            new_event = Event(index, len(temp_list))  # 编号从1开始
            if index <= man_num:
                new_event.type = "man"
            else:
                new_event.type = "woman"
            new_event.rank = list(map(int, temp_list))
            EVENT_LIST.append(new_event)
            index += 1

        # 建立国家列表
        for i in range(country_num):
            new_country = Country(i + 1)
            new_country.rank = [0 for j in range(man_num + woman_num)]
            COUNTRY_LIST.append(new_country)
        cal_country()
        # 建立国家/项目列表完毕,展示菜单页
        QMessageBox.information(self.ui, "提交成功", "数据信息合法且成功提交!")
        my_windows.win_menu = Win_menu()
        my_windows.win_menu.ui.setStyleSheet(qssStyle)
        my_windows.win_menu.ui.show()

        self.ui.hide()  # hide保留原有内容


# 菜单窗口类
class Win_menu:
    def __init__(self):
        self.ui = QUiLoader().load("ui/menu.ui")
        self.ui.label.setPixmap(QPixmap("./image/medal.png"))
        self.ui.search_country.clicked.connect(self.search_country)
        self.ui.search_event.clicked.connect(self.search_event)
        self.ui.action_input.triggered.connect(self.open_input)
        self.ui.action_no.triggered.connect(self.sort_no)
        self.ui.action_score.triggered.connect(self.sort_score)
        self.ui.action_man.triggered.connect(self.sort_man)
        self.ui.action_woman.triggered.connect(self.sort_woman)

    def open_input(self):  # 重新输入
        my_windows.win_input.ui.setStyleSheet(qssStyle)
        my_windows.win_input.ui.show()
        self.ui.close()

    def search_country(self):
        country_no = self.ui.country_no.value()
        if country_no > len(COUNTRY_LIST) or country_no <= 0:
            QMessageBox.critical(self.ui, "范围错误", f"国家编号的范围应为[1~{len(COUNTRY_LIST)}]!")
            return
        my_windows.win_result = Win_result_country("查询", country_no)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()

    def search_event(self):
        event_no = self.ui.event_no.value()
        if event_no > len(EVENT_LIST) or event_no <= 0:
            QMessageBox.critical(self.ui, "范围错误", f"项目编号的范围应为[1~{len(EVENT_LIST)}]!")
            return
        my_windows.win_result = Win_result_event("查询", event_no)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()

    def sort_no(self):
        list_r = sorted(COUNTRY_LIST, key=key_no, reverse=False)
        my_windows.win_result = Win_result_normal("编号排序", list_r)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()

    def sort_score(self):
        list_r = sorted(COUNTRY_LIST, key=key_score, reverse=True)
        my_windows.win_result = Win_result_normal("总分排序", list_r)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()

    def sort_man(self):
        list_r = sorted(COUNTRY_LIST, key=key_man, reverse=True)
        my_windows.win_result = Win_result_normal("男团排序", list_r)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()

    def sort_woman(self):
        list_r = sorted(COUNTRY_LIST, key=key_woman, reverse=True)
        my_windows.win_result = Win_result_normal("女团排序", list_r)
        my_windows.win_result.ui.setStyleSheet(qssStyle)
        my_windows.win_result.ui.show()



# 结果窗口类:共计3种,1-常规,2-国家,3-项目
class Win_result_normal:
    def __init__(self, prompt, list_r):
        self.ui = QUiLoader().load("ui/result_normal.ui")
        self.ui.label_2.setPixmap(QPixmap("./image/circle.png"))
        self.ui.back_button.clicked.connect(self.back_to_menu)
        self.ui.label.setText(prompt + "结果：")
        row_num = len(list_r)
        self.ui.tableWidget.setRowCount(row_num)
        count = 0
        for it in list_r:
            item_list = [count + 1, it.no, it.score, it.man_score, it.woman_score]
            count_2 = 0
            for item_t in item_list:
                item = QTableWidgetItem(str(item_t))
                item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
                self.ui.tableWidget.setItem(count, count_2, item)
                count_2 += 1
            count += 1

    def back_to_menu(self):
        self.ui.tableWidget.clearContents()
        self.ui.close()


class Win_result_country:
    def __init__(self, prompt, country_no):
        self.ui = QUiLoader().load("ui/result_country.ui")
        self.ui.label_2.setPixmap(QPixmap("./image/circle.png"))
        self.ui.back_button.clicked.connect(self.back_to_menu)
        prompt = "国家" + str(country_no) + "的" + prompt
        self.ui.label.setText(prompt + "结果：")
        row_num = len(EVENT_LIST)
        self.ui.tableWidget.setRowCount(row_num)
        for i in range(row_num):
            item_0 = QTableWidgetItem(str(i + 1))
            dat = COUNTRY_LIST[country_no - 1].rank[i]
            if dat == 0:
                temp_s = "未取得名次"
            else:
                temp_s = str(dat)
            item_1 = QTableWidgetItem(temp_s)
            item_0.setFlags(Qt.ItemIsEnabled)
            item_1.setFlags(Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(i, 0, item_0)
            self.ui.tableWidget.setItem(i, 1, item_1)

    def back_to_menu(self):
        self.ui.tableWidget.clearContents()
        self.ui.close()


class Win_result_event:
    def __init__(self, prompt, event_no):
        self.ui = QUiLoader().load("ui/result_event.ui")
        self.ui.label_2.setPixmap(QPixmap("./image/circle.png"))
        self.ui.back_button.clicked.connect(self.back_to_menu)
        prompt = "项目" + str(event_no) + "的" + prompt
        self.ui.label.setText(prompt + "结果：")
        row_num = EVENT_LIST[event_no - 1].top
        self.ui.tableWidget.setRowCount(row_num)
        for i in range(row_num):
            item_0 = QTableWidgetItem(str(i + 1))
            item_0.setFlags(Qt.ItemIsEnabled)
            item_1 = QTableWidgetItem(str(EVENT_LIST[event_no - 1].rank[i]))
            item_1.setFlags(Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(i, 0, item_0)
            self.ui.tableWidget.setItem(i, 1, item_1)

    def back_to_menu(self):
        self.ui.tableWidget.clearContents()
        self.ui.close()


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])
app.setWindowIcon(QIcon('image/logo.png'))  # 主窗口图标
my_windows = My_Windows()
my_windows.win_input = Win_input()
styleFile = './style/Aqua.qss'
qssStyle = CommonHelper.readQss(styleFile)
my_windows.win_input.ui.setStyleSheet(qssStyle)
my_windows.win_input.ui.show()
app.exec_()
