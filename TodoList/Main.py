import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QListWidgetItem, QDesktopWidget
from PyQt5.QtCore import QSize, Qt, QPoint


class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        font = QFont('Times New Roman')
        font.setBold(True)

        # with open('style.css', 'r') as f:
        #     self.setStyleSheet(f.read())

        self.setWindowOpacity(0.7)
        self.setWindowTitle('Todo List')
        self.setFont(QFont('Times New Roman'))
        self.setWindowIcon(QIcon('../ico.jpg'))

        desktop_rect = QApplication.desktop().availableGeometry()
        frame_rect = self.frameGeometry()
        new_x = desktop_rect.width() - frame_rect.width() - 20
        new_y = 20
        new_pos = desktop_rect.topLeft() + QPoint(new_x, new_y)
        self.move(new_pos)

        self.setFixedSize(300, 500)

        self.todo_list = QListWidget()
        self.add_edit = QLineEdit()
        self.add_button = QPushButton('Add')
        self.clear_button = QPushButton('Clear')

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.add_edit)
        hbox.addWidget(self.add_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.todo_list)
        vbox.addWidget(self.clear_button)

        self.setLayout(vbox)

        self.add_button.setObjectName("btn-4")

        self.add_edit.returnPressed.connect(self.addTodo)
        self.add_button.clicked.connect(self.addTodo)
        self.clear_button.clicked.connect(self.clearTodo)

        self.loadTodos()

        self.add_button.setFont(font)
        self.clear_button.setFont(font)

        self.todo_list.itemClicked.connect(self.todoItemClicked)
        self.todo_list.itemDoubleClicked.connect(self.editTodo)
        self.todo_list.itemChanged.connect(self.updateTodo)

        self.setupTodoList()

    def setupTodoList(self):
        self.todo_list.setSelectionMode(QListWidget.SingleSelection)
        self.todo_list.setIconSize(QSize(40, 40))
        self.todo_list.itemClicked.connect(self.todoItemClicked)

    def todoItemClicked(self, item):
        if item.checkState() == Qt.Checked:
            row = self.todo_list.row(item)
            if row != -1:
                self.todo_list.takeItem(row)
                self.saveTodos()

    def editTodo(self, item):
        self.todo_list.editItem(item)

    def addTodo(self):
        todo_text = self.add_edit.text().strip()
        if todo_text:
            item = QListWidgetItem(todo_text, self.todo_list)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(Qt.Unchecked)
            self.add_edit.clear()
            self.saveTodos()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a todo item.')

    def completeTodo(self, item):
        self.todo_list.takeItem(self.todo_list.row(item))
        self.saveTodos()

    def clearTodo(self):
        self.todo_list.clear()
        self.saveTodos()

    def saveTodos(self):
        with open('data.txt', 'w') as f:
            for index in range(self.todo_list.count()):
                f.write(self.todo_list.item(index).text() + '\n')

    def loadTodos(self):
        try:
            with open('data.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    item = QListWidgetItem(line.strip(), self.todo_list)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
                    item.setCheckState(Qt.Unchecked)
        except FileNotFoundError:
            pass

    def updateTodo(self, item):
        if item.text().strip() == "":
            row = self.todo_list.row(item)
            if row != -1:
                self.todo_list.takeItem(row)
                self.saveTodos()
            return

        self.saveTodos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);")  # 设置窗口背景半透明度
    todo_app.show()
    sys.exit(app.exec_())
