import sys
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from main_window import Ui_MainWindow
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.read_from_database()
        
        self.ui.btn_newtask.clicked.connect(self.new_task)

        QToolTip.setFont(QFont('Centaur', pointSize=12))
        
        # self.panel = QWidget()
        # self.ui.gl_tasks.setStyleSheet("background-color:black;")

    def new_task(self):
        new_title = self.ui.tb_new_task_title.text()
        new_description = self.ui.tb_new_task_description.toPlainText()
        Priority = int(not self.ui.cb_priority.isChecked())
        Date = self.ui.dateTimeEdit.dateTime().toString()
        feedback = self.db.add_new_task(new_title, new_description, Priority, Date)
        self.ui.tb_new_task_title.clear()
        self.ui.tb_new_task_description.clear()

        if feedback == True:
            self.update_tasks()

        else:
            msg_box = QMessageBox()
            msg_box.setText("you have problem")
            msg_box.exec()

    def done_tasks(self, id, checked):
        self.db.done_task(id, checked)
            
    def update_tasks(self,id = None):
        if id is not None:
            self.db.remove_task(id)
        children = []
        for i in range(self.ui.gl_tasks.count()):
            child = self.ui.gl_tasks.itemAt(i).widget()
            if child:
                children.append(child)
        for child in children:
            child.deleteLater()
        self.read_from_database()

    def add_task_to_grid(self,tasks,i,row):

        new_checkbox = QCheckBox()
        new_btn = QPushButton()
        new_checkbox.setText(tasks[i][1])
        new_checkbox.setFont(QFont('Centaur', pointSize=15))
        new_checkbox.setStyleSheet("background-color: red;")
        new_btn.setText('❌')
        new_btn.setMaximumWidth(50)
        new_checkbox.setChecked(tasks[i][3])
        if tasks[i][4] == 0:
            new_checkbox.setStyleSheet("background-color: pink; color: red")
        else:
            new_checkbox.setStyleSheet("background-color: rgb(75, 150, 0);; color: black")

        if tasks[i][5] == None:
            new_checkbox.setToolTip(tasks[i][2])
        else:
            new_checkbox.setToolTip(tasks[i][2]+ '\n\n' + str(tasks[i][5]))
        
        self.ui.gl_tasks.addWidget(new_checkbox, row, 0)
        self.ui.gl_tasks.addWidget(new_btn, row, 2)

        new_checkbox.toggled.connect(partial(self.done_tasks,tasks[i][0]))
        new_btn.clicked.connect(partial(self.update_tasks,tasks[i][0]))

    def read_from_database(self):
        tasks = self.db.get_tasks()

        index_doned = []
        row = 0
        for i in range(len(tasks)):
            if tasks[i][3] == 0:
                self.add_task_to_grid(tasks,i,row)
                row += 1
            else:
                index_doned.append(i)

        undone_tasks = len(tasks) - len(index_doned)
        for j in range(len(index_doned)):
            self.add_task_to_grid(tasks,index_doned[j],undone_tasks + j)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
