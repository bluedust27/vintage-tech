import sys
from datetime import date

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from Souvenir import Collectible


# todo: load types from json
#

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.build_ui()
        self.show()
        self._error_message = ""

    def build_ui(self):
        self.ui.lbl_datenow.setText(QDate.currentDate().toString('dd/MM/yyyy'))
        self.ui.date_dateman.setDate(QDate.currentDate())
        self.ui.cmb_type.addItems(["All", "Computer", "Mobile"])
        self.ui.cmb_typedisplay.addItems(["All", "Computer", "Mobile"])

        self.ui.tbl_show.setColumnCount(5)
        self.ui.tbl_show.setHorizontalHeaderLabels(("Sr. No.", "Name", "Manufactured Date", "Added On", "Description"))
        self.ui.tbl_show.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_add.clicked.connect(self.add_collectible)

    def clear_form(self):
        self.ui.txt_name.clear()
        self.ui.date_dateman.setDate(QDate.currentDate())
        self.ui.txt_desc.clear()

    def add_collectible(self):
        name = self.ui.txt_name.text()
        c_type = self.ui.cmb_type.currentText()
        date_manufactured = self.ui.date_dateman.date().toPyDate()
        date_added = date.today()
        description = self.ui.txt_desc.toPlainText()

        Collectible(name, c_type, date_manufactured, date_added, description)
        self.load_collectible()

    def load_collectible(self):

        for i in reversed(range(self.ui.tbl_show.rowCount())):
            self.ui.tbl_show.removeRow(i)

        row_pos = 0
        for c in Collectible.COLLECTIBLE_LIST:
            self.ui.tbl_show.insertRow(row_pos)
            self.ui.tbl_show.setItem(row_pos, 1, QTableWidgetItem(c.name))
            row_pos += 1




app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
