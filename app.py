import sys
from datetime import date

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QInputDialog
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
        Collectible.populate_type()
        self.ui.cmb_type.addItems(Collectible.TYPE_LIST)
        self.ui.cmb_typedisplay.addItems(Collectible.TYPE_LIST)

        self.ui.tbl_show.setColumnCount(5)
        self.ui.tbl_show.setHorizontalHeaderLabels(("Sr. No.", "Name", "Manufactured Date", "Added On", "Description"))
        self.ui.tbl_show.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_add.clicked.connect(self.add_collectible)
        self.ui.btn_delete.clicked.connect(self.delete_collectible)
        self.ui.btn_newtype.clicked.connect(self.show_new_type_dialog)

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
        self.load_collectibles()
        self.clear_form()

    def load_collectibles(self):
        for i in reversed(range(self.ui.tbl_show.rowCount())):
            self.ui.tbl_show.removeRow(i)

        row_pos = 0
        for c in Collectible.COLLECTIBLE_LIST:
            self.ui.tbl_show.insertRow(row_pos)
            self.ui.tbl_show.setItem(row_pos, 1, QTableWidgetItem(c.name))
            row_pos += 1

    def delete_collectible(self):
        rows = sorted(set(index.row() for index in self.ui.tbl_show.selectedIndexes()))

        for row in rows:
            Collectible.COLLECTIBLE_LIST.pop(row)

        self.load_collectibles()

    def show_new_type_dialog(self):
        text, ok = QInputDialog.getText(self, "Adding New Type", "Enter type:")
        if ok and text:
            self.ui.cmb_type.addItem(text)
            self.ui.cmb_typedisplay.addItem(text)

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
