"""
Author: Johnson
Time：2023-07-06 23:16
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import pymysql

from insertStuUi import *


class InsertWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = None
        self.ui = Ui_InsertWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.pushButton_sure.clicked.connect(self.insert_info)
        icon = QIcon("./icons/homeicon.png")
        self.setWindowIcon(icon)
        self.show()

    my_Signal = QtCore.pyqtSignal(str)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def insert_info(self):
        id = self.ui.lineEdit_id.text()
        name = self.ui.lineEdit_name.text()
        sex = self.ui.lineEdit_sex.text()
        age = self.ui.lineEdit_age.text()
        year = self.ui.lineEdit_year.text()
        stu_class = self.ui.lineEdit_class.text()
        if id == '' or name == '' or sex == '' or age == '' or year == '' or stu_class == '':
            QMessageBox.information(self, "提示", "数据不能为空")
        elif sex != 'male' and sex != 'female':
            QMessageBox.information(self, "提示", "注意性别修改")
        else:
            # if id=='' or 'name'=='' or sex=='' or age =='' or
            db = pymysql.connect(host='110.41.2.230',
                                 user='root',
                                 password='KrxkKrxk',
                                 database='database2',
                                 charset='utf8')
            cur = db.cursor()

            try:
                cur.execute(f"insert into students "
                            f"values ({int(id)} ,'{name}', '{sex}', {int(age)}, {int(year)}, '{stu_class}')")
                QMessageBox.information(self, "提示", "数据修改成功")
            except:
                QMessageBox.information(self, "提示", "修改失败")

            db.commit()
            db.close()
            cur.close()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = InsertWindow()
    sys.exit(app.exec_())
