import sys
import uuid
import datetime

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QInputDialog, QMessageBox

from Souvenir import Collectible
from validations import Validation


class Vintage_Tech_GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.build_ui()
        self.show()
        self.setFixedSize(920, 650)
        self._error_message = ""

    def build_ui(self):
        self.ui.date_dateman.setDate(QDate.currentDate())
        Collectible.populate_type_list()
        Collectible.populate_type_list_display()
        self.ui.cmb_typedisplay.addItems(Collectible.TYPE_LIST_DISPLAY)
        self.ui.cmb_type.addItems(Collectible.TYPE_LIST[1:len(Collectible.TYPE_LIST)])

        self.ui.tbl_show.setColumnCount(6)
        self.ui.tbl_show.setHorizontalHeaderLabels(
            ("Name", "Type", "Manufactured Date", "Added On", "Description", "ID"))
        self.ui.tbl_show.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_collectibles("All")
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_add.clicked.connect(self.add_collectible)
        self.ui.btn_delete.clicked.connect(self.delete_collectible)
        self.ui.btn_newtype.clicked.connect(self.show_new_type_dialog)
        self.ui.btn_newtype.setToolTip("Add a new type")
        self.ui.cmb_typedisplay.currentTextChanged.connect(self.load_collectibles)
        self.ui.tbl_show.itemChanged.connect(self.item_in_table_changed)
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
        uid = str(uuid.uuid4())
        name = self.ui.txt_name.text()
        c_type = self.ui.cmb_type.currentText()
        date_manufactured = self.ui.date_dateman.date().toPyDate()
        date_added = datetime.date.today()
        description = self.ui.txt_desc.toPlainText()

        Collectible(name, c_type, date_manufactured, date_added, description, uid)
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
                self.ui.tbl_show.setItem(row_pos, 5, QTableWidgetItem(c.uid))
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
        Collectible.populate_type_list()
        Collectible.populate_type_list_display()
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

    def item_in_table_changed(self, changed):
        # validate for blank values
        if not str(changed.text()).strip():
            msg_blank = QMessageBox()
            msg_blank.setIcon(QMessageBox.Critical)
            msg_blank.setText("New value cannot be blank!")
            msg_blank.setWindowTitle("Invalid Operation")
            msg_blank.setStandardButtons(QMessageBox.Ok)
            msg_blank.exec_()
            self.load_collectibles("All")
            return

        selected_row = self.ui.tbl_show.currentRow()
        selected_column = self.ui.tbl_show.currentColumn()

        # for all cases other than edit
        if selected_row == -1:
            return

        # validate UID
        if selected_column == 5:
            msg_id = QMessageBox()
            msg_id.setIcon(QMessageBox.Critical)
            msg_id.setText("ID cannot be edited!")
            msg_id.setWindowTitle("Invalid Operation")
            msg_id.setStandardButtons(QMessageBox.Ok)
            msg_id.exec_()
            self.load_collectibles("All")
            return

        # validate type
        if selected_column == 1:
            is_type_valid = self.__validate_type(str(changed.text()).strip())
            if not is_type_valid:
                msg_type = QMessageBox()
                msg_type.setIcon(QMessageBox.Critical)
                msg_type.setText("This type is not valid. Add new type to proceed.")
                msg_type.setWindowTitle("Invalid Operation")
                msg_type.setStandardButtons(QMessageBox.Ok)
                msg_type.exec_()
                self.load_collectibles("All")
                return


        # Validate date format and future date
        if selected_column == 2 or selected_column == 3:
            is_date_valid = self.__validate_date(str(changed.text()).strip())
            if not is_date_valid:
                msg_date = QMessageBox()
                msg_date.setIcon(QMessageBox.Critical)
                msg_date.setText("Wrong date format. Correct format (dd/mm/yyyy)")
                msg_date.setWindowTitle("Invalid Operation")
                msg_date.setStandardButtons(QMessageBox.Ok)
                msg_date.exec_()
                self.load_collectibles("All")
                return

            if datetime.datetime.strptime(str(changed.text()).strip(), "%d/%m/%Y").date() > datetime.date.today():
                msg_date = QMessageBox()
                msg_date.setIcon(QMessageBox.Critical)
                msg_date.setText("Enter valid date")
                msg_date.setWindowTitle("Invalid Operation")
                msg_date.setStandardButtons(QMessageBox.Ok)
                msg_date.exec_()
                self.load_collectibles("All")
                return

        # confirm edit
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Do you want to edit this item?")
        msg.setWindowTitle("Edit item")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        if ret == QMessageBox.No or ret == QMessageBox.Close:
            self.load_collectibles("All")
            return

        selected_id = self.ui.tbl_show.item(selected_row, 5).text()
        for idx, c in enumerate(Collectible.COLLECTIBLE_LIST):
            if c.uid == selected_id:
                c = self.__replace_item(c, selected_column, changed)
                Collectible.COLLECTIBLE_LIST[idx] = c
                break
        Collectible.save_to_file()

        Collectible.populate_type_list()
        Collectible.populate_type_list_display()
        self.ui.cmb_typedisplay.clear()
        self.ui.cmb_type.clear()
        self.ui.cmb_typedisplay.addItems(Collectible.TYPE_LIST_DISPLAY)
        self.ui.cmb_type.addItems(Collectible.TYPE_LIST[1:len(Collectible.TYPE_LIST)])


        self.load_collectibles("All")

    def __validate_date(self, changed_date):
        try:
            datetime.datetime.strptime(changed_date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def __validate_type(self, changed_type):
        return changed_type.lower() in (c.lower() for c in Collectible.TYPE_LIST)

    @staticmethod
    def __replace_item(selected_item, selected_column, new_item):
        if selected_column == 0:
            selected_item.name = str(new_item.text()).strip()
        elif selected_column == 1:
            selected_item.type = str(new_item.text()).strip().capitalize()
        elif selected_column == 2:
            selected_item.date_manufactured = str(new_item.text()).strip()
        elif selected_column == 3:
            selected_item.date_added = str(new_item.text()).strip()
        elif selected_column == 4:
            selected_item.description = str(new_item.text()).strip().capitalize()

        return selected_item


app = QApplication(sys.argv)
gui = Vintage_Tech_GUI()
gui.show()
sys.exit(app.exec_())
