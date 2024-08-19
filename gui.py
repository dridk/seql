from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys

from seql import duckdb


class Editor(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.setObjectName("main")
        self.a_edit = QPlainTextEdit()
        self.b_edit = QPlainTextEdit()
        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(self.a_edit)
        splitter.addWidget(self.b_edit)
        self.vbox.addWidget(splitter)

        self.a_edit.textChanged.connect(self.on_changed)

        self.show_valid(True)

    def on_changed(self):

        try:
            txt = duckdb.transpile(self.a_edit.toPlainText())
            self.b_edit.setPlainText(txt)
            self.show_valid(True)
        except Exception as e:
            self.b_edit.setPlainText(str(e))
            self.show_valid(False)

    def show_valid(self, valid: bool = True):
        color = "green" if valid else "red"
        self.setStyleSheet(f"QFrame#main{{border: 2px solid {color}}}")


app = QApplication(sys.argv)


w = Editor()
w.show()

app.exec()
