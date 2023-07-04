from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QSize
from LoginUi import *
from InterfaceUi import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import webbrowser
import sys
import pymysql

# student_ID  name  set  entrance_age  entrance_year  class
# course_ID  name  teacher_ID  credit grade  canceled_year
# teacher_ID  name  course
user_now = ''  # 便于修改密码的账号识别


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = None
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置阴影
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtCore.Qt.black)  # 设置阴影颜色
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.pushButton_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))  # 切换登录页面
        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))  # 切换注册页面

        self.ui.pushButton_L_sure.setShortcut(QKeySequence("Return"))  # 绑定快捷键
        self.ui.pushButton_L_sure.clicked.connect(self.login_in)  # 绑定登录函数
        self.show()

    def login_in(self):
        account = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()
        account_list = []
        password_list = []

        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='database2',
                             charset='utf8')
        cur = db.cursor()

        cur.execute("select * from user")
        rows = cur.fetchall()
        for row in rows:
            account_list.append(row[0])
            password_list.append(row[1])
        print(account_list)
        print(password_list)
        db.commit()
        db.close()

        for i in range(len(account_list)):
            if len(account) == 0 or len(password) == 0:
                self.ui.stackedWidget.setCurrentIndex(1)
            elif account == account_list[i] and password == password_list[i]:
                global user_now
                user_now = account
                self.win = MainWindow()
                self.close()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.Move = True  # 鼠标按下时设置为移动状态
            self.Point = event.globalPos() - self.pos()  # 记录起始点坐标
            event.accept()  # # S

    def mouseMoveEvent(self, QMouseEvent):  # 移动时间
        if QtCore.Qt.LeftButton and self.Move:  # 切记这里的条件不能写死，只要判断move和鼠标执行即可！
            self.move(QMouseEvent.globalPos() - self.Point)  # 移动到鼠标到达的坐标点！
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 结束事件
        self.Move = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crow = 0
        self.ccol = 0

        self.stu_list = ['student_ID', 'name', 'sex', 'entrance_age', ' entrance_year', 'class']
        self.couchos_list = ['student_ID', 'teacher_ID', 'course_ID', 'chosen_year', 'score']
        self.model = QStandardItemModel()
        self.model_tea = QStandardItemModel()
        self.model_course = QStandardItemModel()
        self.model_couchos = QStandardItemModel()
        self.model_stats = QStandardItemModel()
        self.login = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        icon = QIcon("./icons/homeicon.png")
        self.setWindowIcon(icon)

        # self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.shadow.setOffset(0, 0)
        # self.shadow.setBlurRadius(10)
        # self.shadow.setColor(QtCore.Qt.black)
        # self.ui.frame_6.setGraphicsEffect(self.shadow)
        self.ui.pushButton_home.clicked.connect(self.go_home)
        self.ui.pushButton_web.clicked.connect(self.go_web)
        self.ui.pushButton_my.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_logout.clicked.connect(self.logout)
        self.ui.pushButton_M_sure.clicked.connect(self.change_password)

        self.ui.pushButton_stu_info.clicked.connect(self.go_stu_info)
        self.ui.pushButton_tea_info.clicked.connect(self.go_tea_info)
        self.ui.pushButton_course_info.clicked.connect(self.go_course_info)
        self.ui.pushButton_couchos_info.clicked.connect(self.go_couchos_info)
        self.ui.pushButton_stats_info.clicked.connect(self.go_stats_info)

        self.ui.pushButton_stu_qall.clicked.connect(self.show_stu_info)
        self.ui.pushButton_tea_qall.clicked.connect(self.show_tea_info)
        self.ui.pushButton_course_qall.clicked.connect(self.show_course_info)
        self.ui.pushButton_couchos_qall.clicked.connect(self.show_couchos_info)

        self.ui.pushButton_stu_q.clicked.connect(self.show_stu_q_info)
        self.ui.pushButton_tea_q.clicked.connect(self.show_tea_q_info)
        self.ui.pushButton_course_q.clicked.connect(self.show_course_q_info)
        # self.ui.pushButton_couchos_q.clicked.connect(self.show_couchos_q_info)

        self.ui.pushButton_stu_clear.clicked.connect(self.clear_stu_info)
        self.ui.pushButton_tea_clear.clicked.connect(self.clear_tea_info)
        self.ui.pushButton_course_clear.clicked.connect(self.clear_course_info)
        self.ui.pushButton_couchos_clear.clicked.connect(self.clear_couchos_info)

        self.ui.tableView_stu.setModel(self.model)
        self.ui.tableView_tea.setModel(self.model_tea)
        self.ui.tableView_course.setModel(self.model_course)
        self.ui.tableView_couchos.setModel(self.model_couchos)
        self.ui.tableView_stats.setModel(self.model_stats)

        self.ui.pushButton_stat_stu_avg.clicked.connect(self.stu_avg)
        self.ui.pushButton_stat_clear.clicked.connect(self.clear_stat)
        self.ui.pushButton_stat_course_avg.clicked.connect(self.course_avg)

        # 修改信息
        self.ui.pushButton_stu_modify.clicked.connect(self.modify_stu)
        self.ui.pushButton_couchos_modify.clicked.connect(self.modify_score)

        self.ui.tableView_stu.clicked.connect(self.show_stu_cell)
        self.ui.tableView_couchos.clicked.connect(self.show_couchos_cell)
        self.ui.tableView_stu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.label_role.setText(user_now)
        index = self.ui.stackedWidget.currentIndex()
        # if index == 0:
        #     icon = QIcon("./icons/dog.png")
        #     icon_none = QIcon()
        #     self.ui.pushButton_home.setIcon(icon)
        #     self.ui.pushButton_home.setIconSize(QSize(50, 40))
        #     self.ui.pushButton_web.setIcon(icon_none)

        self.ui.pushButton_stu_delete.clicked.connect(self.stu_delete)
        self.show()

    def go_home(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.change_icon()

    def change_icon(self):
        index = self.ui.stackedWidget.currentIndex()
        icon_none = QIcon()
        icon = QIcon("./icons/dog.png")
        if index == 0:
            self.ui.pushButton_home.setIcon(icon)
            self.ui.pushButton_home.setIconSize(QSize(50, 40))
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
        elif index == 1:
            pass
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon)
            self.ui.pushButton_stu_info.setIconSize(QSize(50, 40))
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
        elif index == 2:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon)
            self.ui.pushButton_web.setIconSize(QSize(50, 40))
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
            print("22222")
        elif index == 3:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon)
            self.ui.pushButton_my.setIconSize(QSize(50, 40))
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
        elif index == 4:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon)
            self.ui.pushButton_tea_info.setIconSize(QSize(50, 40))
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
        elif index == 5:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon)
            self.ui.pushButton_course_info.setIconSize(QSize(50, 40))
        elif index == 6:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon)
            self.ui.pushButton_couchos_info.setIconSize(QSize(50, 40))
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon_none)
            self.ui.pushButton_course_info.setIcon(icon_none)
        elif index == 7:
            self.ui.pushButton_home.setIcon(icon_none)
            self.ui.pushButton_web.setIcon(icon_none)
            self.ui.pushButton_my.setIcon(icon_none)
            self.ui.pushButton_stu_info.setIcon(icon_none)
            self.ui.pushButton_couchos_info.setIcon(icon_none)
            self.ui.pushButton_tea_info.setIcon(icon_none)
            self.ui.pushButton_stats_info.setIcon(icon)
            self.ui.pushButton_stats_info.setIconSize(QSize(50, 40))
            self.ui.pushButton_course_info.setIcon(icon_none)

    def stu_delete(self):
        if user_now != 'admin':
            QMessageBox.information(self, '提示', '无权限修改')
            return
        else:  # 更改数据
            # 获取学号
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()

            cur.execute(f"select * from students limit {self.crow},1")
            rows = cur.fetchone()
            data = rows[0]
            cur.execute(f"delete from students where student_ID = {data}")
            db.commit()
            cur.close()
            db.close()
            self.show_stu_info()


    def course_avg(self):
        model_ = self.model_stats
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='database2',
                             charset='utf8')
        cur = db.cursor()
        cur.execute("select courses.name, avg(score) from courses, course_choosing "
                    "where courses.course_ID = course_choosing.course_ID "
                    "GROUP BY courses.course_ID")
        rows = cur.fetchall()
        fields = cur.description
        ff = ['course_name', 'course_ID', 'avg_score']
        row_number = cur.rowcount
        col_number = len(rows[0])
        db.commit()
        cur.close()
        db.close()
        model_.setRowCount(row_number)
        model_.setColumnCount(col_number)

        for i in range(row_number):
            for j in range(col_number):
                temp_data = rows[i][j]
                data = QStandardItem(str(temp_data))
                data.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                model_.setItem(i, j, data)

    def clear_stat(self):
        self.model_stats.clear()

    def stu_avg(self):
        model_ = self.model_stats
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='database2',
                             charset='utf8')
        cur = db.cursor()
        cur.execute("select name, students.student_ID, AVG(score) from course_choosing, students "
                    "where course_choosing.student_ID = students.student_ID "
                    "GROUP BY students.student_ID")
        rows = cur.fetchall()
        fields = cur.description
        ff = ['stu_name', 'student_ID', 'avg_score']
        row_number = cur.rowcount
        col_number = len(rows[0])
        db.commit()
        cur.close()
        db.close()
        model_.setRowCount(row_number)
        model_.setColumnCount(col_number)

        for i in range(row_number):
            for j in range(col_number):
                temp_data = rows[i][j]
                data = QStandardItem(str(temp_data))
                data.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                model_.setItem(i, j, data)
        model_.setHorizontalHeaderLabels(ff)

    def logout(self):
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ''

    def go_web(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.pushButton_blbl.clicked.connect(lambda: webbrowser.open("bilibili.com"))
        self.ui.pushButton_csdn.clicked.connect(lambda: webbrowser.open("csdn.net"))
        self.ui.pushButton_apple.clicked.connect(lambda: webbrowser.open("apple.com.cn"))
        self.ui.pushButton_TV.clicked.connect(lambda: webbrowser.open("v.qq.com"))
        self.ui.pushButton_scut.clicked.connect(lambda: webbrowser.open("www.scut.edu.cn"))
        self.change_icon()

    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.Move = True  # 鼠标按下时设置为移动状态
            self.Point = event.globalPos() - self.pos()  # 记录起始点坐标
            event.accept()  # # S

    def mouseMoveEvent(self, QMouseEvent):  # 移动时间
        if QtCore.Qt.LeftButton and self.Move:  # 切记这里的条件不能写死，只要判断move和鼠标执行即可！
            self.move(QMouseEvent.globalPos() - self.Point)  # 移动到鼠标到达的坐标点！
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 结束事件
        self.Move = False

    # 改密码
    def change_password(self):
        new_password = self.ui.lineEdit_M_pass1.text()
        if len(self.ui.lineEdit_M_pass1.text()) == 0 or len(self.ui.lineEdit_M_pass2.text()) == 0:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        elif self.ui.lineEdit_M_pass1.text() == self.ui.lineEdit_M_pass2.text():
            db = pymysql.connect(host='localhost', user='root', password='root', database='database2', charset='utf8')
            cur = db.cursor()
            cur.execute(f"update user set password='{new_password}' where account = '{user_now}'")
            db.commit()
            db.close()
            self.ui.stackedWidget_2.setCurrentIndex(3)
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    # 学生信息查询全部
    def go_stu_info(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.change_icon()
        # self.temp_modify()

    def go_tea_info(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.change_icon()

    def go_course_info(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.change_icon()

    def go_couchos_info(self):
        self.ui.stackedWidget.setCurrentIndex(6)
        self.change_icon()

    def go_stats_info(self):
        self.ui.stackedWidget.setCurrentIndex(7)
        self.change_icon()

    def temp_modify(self):
        # student_ID  name  set  entrance_age  entrance_year  class
        # course_ID  name  teacher_ID  credit grade  canceled_year
        # teacher_ID  name  course
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='database2',
                             charset='utf8')
        cur = db.cursor()
        for i in range(20):
            cur.execute(f"insert into students values ({10021 + i},'张三',2,20,2024,'网工')")
            # insert into students values (10005,'李四2',2,21,2024,'网工')
        db.commit()
        cur.close()
        db.close()

    # 信息显示
    def show_info(self, query_table_name, tableview_):
        model_ = None
        if tableview_ == 'stu':
            model_ = self.model
        elif tableview_ == 'tea':
            model_ = self.model_tea
        elif tableview_ == 'course':
            model_ = self.model_course
        elif tableview_ == 'couchos':
            model_ = self.model_couchos

        db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='database2',
                             charset='utf8')
        cur = db.cursor()
        cur.execute(f"select * from {query_table_name}")
        rows = cur.fetchall()
        fields = cur.description
        ff = []
        for field in fields:
            ff.append(field[0])
        print(ff)
        row_number = cur.rowcount
        col_number = len(rows[0])
        db.commit()
        cur.close()
        db.close()
        model_.setRowCount(row_number)
        model_.setColumnCount(col_number)

        for i in range(row_number):
            for j in range(col_number):
                temp_data = rows[i][j]
                data = QStandardItem(str(temp_data))
                data.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                model_.setItem(i, j, data)

        model_.setHorizontalHeaderLabels(ff)
        #
        if tableview_ == 'stu':
            header = self.ui.tableView_stu.horizontalHeader()
            header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif tableview_ == 'tea':
            header = self.ui.tableView_tea.horizontalHeader()
            header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif tableview_ == 'course':
            header = self.ui.tableView_course.horizontalHeader()
            header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        elif tableview_ == 'couchos':
            header = self.ui.tableView_couchos.horizontalHeader()
            header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

    # 学生信息显示
    def show_stu_info(self):
        self.show_info(query_table_name='students', tableview_='stu')

    def show_tea_info(self):
        self.show_info(query_table_name='teachers', tableview_='tea')

    def show_course_info(self):
        self.show_info(query_table_name='courses', tableview_='course')

    def show_couchos_info(self):
        self.show_info(query_table_name='course_choosing', tableview_='couchos')

    # 根据姓名或学号查询学生信息
    def show_stu_q_info(self):
        stu_input = self.ui.lineEdit_stu.text().strip()
        find_flag = False
        if stu_input == '':
            QMessageBox.information(self, "提示", "请输入学号或姓名")
        else:
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()
            cur.execute("select student_ID, name from students")
            values = cur.fetchall()
            # print(values)
            student_id = []
            name = []
            for value in values:
                student_id.append(value[0])
                name.append(value[1])
            # print(type(student_id))
            # print(name)

            if '0' <= stu_input[0] <= '9':
                print(stu_input[0])
                temp = int(stu_input)
                for i in range(len(name)):
                    if (student_id[i] == int(stu_input)):
                        find_flag = True
                        cur.execute(f"select * from students  where student_ID = {student_id[i]}")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        self.model.setRowCount(row_number)
                        self.model.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                self.model.setItem(i, j, data)

                        self.model.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_stu.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                        self.ui.tableView_stu.show()

            else:
                print(stu_input[0])
                for i in range(len(name)):
                    if (name[i] == stu_input):
                        find_flag = True
                        cur.execute(f"select * from students  where name = '{name[i]}'")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        self.model.setRowCount(row_number)
                        self.model.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                self.model.setItem(i, j, data)

                        self.model.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_stu.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                        # self.model.item(0,2).setForeground(QBrush(QColor(0, 255, 255)))
                        self.ui.tableView_stu.show()
            if not find_flag:
                self.show_stu_info()
                QMessageBox.information(self, '提示', '无此学号或姓名对应的学生信息')

            db.commit()
            cur.close()
            db.close()

    def show_tea_q_info(self):
        tea_input = self.ui.lineEdit_tea.text().strip()
        model_ = self.model_tea
        if tea_input == '':
            QMessageBox.information(self, "提示", "请输入教工号或姓名")
        else:
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()
            cur.execute("select teacher_ID, name from teachers")
            values = cur.fetchall()
            # print(values)
            teacher_id = []
            name = []
            for value in values:
                teacher_id.append(value[0])
                name.append(value[1])
            # print(type(student_id))
            # print(name)
            find_flag = False
            if '0' <= tea_input[0] <= '9':
                print(tea_input[0])
                temp = int(tea_input)
                for i in range(len(name)):
                    if (teacher_id[i] == int(tea_input)):
                        find_flag = True
                        cur.execute(f"select * from teachers  where teacher_ID = {teacher_id[i]}")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        model_.setRowCount(row_number)
                        model_.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                model_.setItem(i, j, data)

                        model_.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_stu.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                        self.ui.tableView_tea.show()

            else:
                print(tea_input[0])
                for i in range(len(name)):
                    if (name[i] == tea_input):
                        find_flag = True
                        cur.execute(f"select * from teachers  where name = '{name[i]}'")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        model_.setRowCount(row_number)
                        model_.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                model_.setItem(i, j, data)

                        model_.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_stu.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                        # self.model.item(0,2).setForeground(QBrush(QColor(0, 255, 255)))
                        self.ui.tableView_tea.show()
            if not find_flag:
                self.show_tea_info()
                QMessageBox.information(self, "提示", "无此教工号或姓名对应的教师信息")

            db.commit()
            cur.close()
            db.close()

    def show_course_q_info(self):
        model_ = self.model_course
        input = self.ui.lineEdit_course.text().strip()
        find_flag = False
        if input == '':
            QMessageBox.information(self, "提示", "请输入课程ID")
        else:
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()
            cur.execute("select course_ID,name from courses")
            values = cur.fetchall()
            # print(values)
            course_ID = []
            name = []
            for value in values:
                course_ID.append(value[0])
                name.append(value[1])

            # print(type(student_id))
            # print(name)
            if '0' <= input[0] <= '9':
                print(input[0])
                temp = int(input)
                for i in range(len(course_ID)):
                    if (course_ID[i] == int(input)):
                        find_flag = True
                        cur.execute(f"select * from courses  where course_ID = {course_ID[i]}")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        model_.setRowCount(row_number)
                        model_.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                model_.setItem(i, j, data)

                        model_.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_course.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

            else:
                print(input[0])
                for i in range(len(name)):
                    if (name[i] == input):
                        find_flag = True
                        cur.execute(f"select * from courses  where name = '{name[i]}'")
                        rows = cur.fetchall()
                        print(rows)
                        fields = cur.description
                        ff = []
                        for field in fields:
                            ff.append(field[0])
                        print(ff)
                        row_number = cur.rowcount
                        col_number = len(rows[0])
                        model_.setRowCount(row_number)
                        model_.setColumnCount(col_number)
                        for i in range(row_number):
                            for j in range(col_number):
                                temp_data = rows[i][j]
                                data = QStandardItem(str(temp_data))
                                data.setTextAlignment(
                                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

                                model_.setItem(i, j, data)

                        model_.setHorizontalHeaderLabels(ff)
                        header = self.ui.tableView_stu.horizontalHeader()
                        header.setDefaultAlignment(
                            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                        # self.model.item(0,2).setForeground(QBrush(QColor(0, 255, 255)))

            if not find_flag:
                self.show_course_info()
                QMessageBox.information(self, '提示', '无此课程号对应的课程信息')

            db.commit()
            cur.close()
            db.close()

    # 清空
    def clear_stu_info(self):
        self.model.clear()

    def clear_tea_info(self):
        self.model_tea.clear()

    def clear_course_info(self):
        self.model_course.clear()

    def clear_couchos_info(self):
        self.model_couchos.clear()

    def show_stu_cell(self):
        row = self.ui.tableView_stu.currentIndex().row()
        column = self.ui.tableView_stu.currentIndex().column()
        print('({}, {})'.format(row, column))
        data = self.ui.tableView_stu.currentIndex().data()
        self.ui.lineEdit_stu_before.setText(data)
        self.crow = row
        self.ccol = column

    def show_couchos_cell(self):
        row = self.ui.tableView_couchos.currentIndex().row()
        column = self.ui.tableView_couchos.currentIndex().column()
        print('({}, {})'.format(row, column))
        data = self.ui.tableView_couchos.currentIndex().data()
        self.ui.lineEdit_couchos_before.setText(data)
        self.crow = row
        self.ccol = column

    def modify_stu(self):
        if user_now != 'admin':
            QMessageBox.information(self, '提示', '无权限修改')
            return
        text = self.ui.lineEdit_stu_after.text()
        if text == '':
            QMessageBox.information(self, '提示', '请输入修改后的信息（可设置为“空”）')
        else:  # 更改数据
            # 获取学号
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()

            cur.execute(f"select * from students limit {self.crow},1")
            rows = cur.fetchone()
            print(self.crow)
            print(rows)
            data = rows[0]
            print(data)
            if self.stu_list[self.ccol] != 'student_ID':
                try:
                    cur.execute(f"update students set {self.stu_list[self.ccol]} =  '{text}' where student_ID = {data}")
                    QMessageBox.information(self, '提示', '修改成功')
                except:
                    QMessageBox.information(self, '提示', '数据修改失败')
            else:
                QMessageBox.information(self, '提示', '不能修改学号')
            db.commit()
            cur.close()
            db.close()
            self.show_stu_info()


    def modify_score(self):
        if user_now == 'student' or user_now == 'admin':
            QMessageBox.information(self, '提示', '无权限修改')
            return
        text = self.ui.lineEdit_couchos_after.text()
        if text == '':
            QMessageBox.information(self, '提示', '请输入修改后的信息（可设置为“空”）')
        else:  # 更改数据
            # 获取成绩
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()

            cur.execute(f"select * from course_choosing limit {self.crow},1")
            rows = cur.fetchone()
            print(self.crow)
            print(rows)
            student_id = rows[0]
            course_id = rows[2]
            print(student_id)
            text = int(text)
            if self.couchos_list[self.ccol] != 'score':
                QMessageBox.information(self, '提示', '只能修改成绩')
            elif text < 0 or text > 100:
                QMessageBox.information(self, '提示', '成绩范围0~100')
            else:
                try:
                    cur.execute(f"update course_choosing set score = {text} "
                                f"where student_ID = {student_id} and course_ID = {course_id}")
                    QMessageBox.information(self, '提示', '修改成功')
                except:
                    QMessageBox.information(self, '提示', '数据修改失败')
            # else:
            #     QMessageBox.information(self, '提示', '不能修改学号')

            db.commit()
            cur.close()
            db.close()
            self.show_couchos_info()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())
