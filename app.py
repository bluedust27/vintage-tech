import sys
from datetime import date, datetime

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.uic.properties import QtWidgets, QtGui

from Souvenir import Collectible
from validations import Validation


class Vintage_Tech_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.build_ui()
        self.show()
        self.setFixedSize(620, 650)
        self._error_message = ""

    def build_ui(self):
        self.ui.date_dateman.setDate(QDate.currentDate())
        Collectible.populate_typelist()
        Collectible.populate_typelist_display()
        self.ui.cmb_typedisplay.addItems(Collectible.TYPE_LIST_DISPLAY)
        self.ui.cmb_type.addItems(Collectible.TYPE_LIST[1:len(Collectible.TYPE_LIST)])

        self.ui.tbl_show.setColumnCount(5)
        self.ui.tbl_show.setHorizontalHeaderLabels(("Name", "Type", "Manufactured Date", "Added On", "Description"))
        self.ui.tbl_show.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_collectibles("All")
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_add.clicked.connect(self.add_collectible)
        self.ui.btn_delete.clicked.connect(self.delete_collectible)
        self.ui.btn_newtype.clicked.connect(self.show_new_type_dialog)
        self.ui.btn_newtype.setToolTip("Add a new type")
        self.ui.btn_edit.clicked.connect(self.edit_collectible)
        self.ui.cmb_typedisplay.currentTextChanged.connect(self.load_collectibles)
        self.ui.btn_exit.clicked.connect(self.close)

    def clear_form(self):
        self.ui.txt_name.clear()
        self.ui.date_dateman.setDate(QDate.currentDate())
        self.ui.txt_desc.clear()
        self.ui.cmb_type.setCurrentIndex(0)

    def add_collectible(self):
        v = Validation(self.ui)
        if not v.validate_input():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(Validation.ERROR_MESSAGE)
            msg.setWindowTitle("Error in Entry")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            Validation.ERROR_MESSAGE = ""
            return
        name = self.ui.txt_name.text()
        c_type = self.ui.cmb_type.currentText()
        date_manufactured = self.ui.date_dateman.date().toPyDate()
        date_added = date.today()
        description = self.ui.txt_desc.toPlainText()

        Collectible(name, c_type, date_manufactured, date_added, description)
        Collectible.save_to_file()
        self.load_collectibles("All")
        self.clear_form()

    def load_collectibles(self, selected_type):
        for i in reversed(range(self.ui.tbl_show.rowCount())):
            self.ui.tbl_show.removeRow(i)
        Collectible.load_from_file()
        row_pos = 0
        for c in Collectible.COLLECTIBLE_LIST:
            if c.type == selected_type or selected_type == "All":
                self.ui.tbl_show.insertRow(row_pos)
                self.ui.tbl_show.setItem(row_pos, 0, QTableWidgetItem(c.name))
                self.ui.tbl_show.setItem(row_pos, 1, QTableWidgetItem(c.type))
                self.ui.tbl_show.setItem(row_pos, 2, QTableWidgetItem(c.date_manufactured.strftime("%d/%m/%Y")))
                self.ui.tbl_show.setItem(row_pos, 3, QTableWidgetItem(c.date_added.strftime("%d/%m/%Y")))
                self.ui.tbl_show.setItem(row_pos, 4, QTableWidgetItem(c.description))
                row_pos += 1

    def delete_collectible(self):
        rows = sorted(set(index.row() for index in self.ui.tbl_show.selectedIndexes()))

        if len(rows) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please choose an item to delete.")
            msg.setWindowTitle("No Item Selected")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        ask = QMessageBox()
        ask.setIcon(QMessageBox.Question)
        ask.setText("Are you sure you want to delete this item?")
        ask.setWindowTitle("Delete")
        ask.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ask.activateWindow()
        ret_val = ask.exec_()

        if ret_val == QMessageBox.No:
            return

        for row in rows:
            Collectible.COLLECTIBLE_LIST.pop(row)

        Collectible.save_to_file()
        Collectible.populate_typelist()
        Collectible.populate_typelist_display()
        self.ui.cmb_typedisplay.clear()
        self.ui.cmb_type.clear()
        self.ui.cmb_typedisplay.addItems(Collectible.TYPE_LIST_DISPLAY)
        self.ui.cmb_type.addItems(Collectible.TYPE_LIST[1:len(Collectible.TYPE_LIST)])
        self.load_collectibles("All")


    def show_new_type_dialog(self):
        new_type, ok = QInputDialog.getText(self, "New Type", "Enter new type:")

        if ok and new_type:
            is_target_in_list = new_type.lower() in (c.lower() for c in Collectible.TYPE_LIST)

            if is_target_in_list:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Type: {0} already exists!".format(new_type.capitalize()))
                msg.setWindowTitle("Duplicate item")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

            if not is_target_in_list:
                new_type = new_type.capitalize()
                Collectible.TYPE_LIST.append(new_type)
                self.ui.cmb_type.addItem(new_type)
                self.ui.cmb_typedisplay.addItem(new_type)
                self.ui.cmb_type.setCurrentText(new_type)

    def edit_collectible(self):
        selected_row = str(self.ui.tbl_show.currentIndex().row())
        v = QMessageBox()
        v.setText(selected_row)
        v.exec_()
        self.ui.tbl_show.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # todo: logic for edit button


app = QApplication(sys.argv)
gui = Vintage_Tech_GUI()
gui.show()
sys.exit(app.exec_())
