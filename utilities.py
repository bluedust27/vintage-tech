import datetime

from PyQt5.QtWidgets import QMessageBox

from Souvenir import Collectible


class Utilities:
    @staticmethod
    def msg_box_blank_input():
        msg_blank = QMessageBox()
        msg_blank.setIcon(QMessageBox.Critical)
        msg_blank.setText("No blank values allowed!")
        msg_blank.setWindowTitle("Invalid Operation")
        msg_blank.setStandardButtons(QMessageBox.Ok)
        msg_blank.exec_()

    @staticmethod
    def msg_box_uid():
        msg_id = QMessageBox()
        msg_id.setIcon(QMessageBox.Critical)
        msg_id.setText("ID cannot be edited!")
        msg_id.setWindowTitle("Invalid Operation")
        msg_id.setStandardButtons(QMessageBox.Ok)
        msg_id.exec_()

    @staticmethod
    def msg_box_type():
        msg_type = QMessageBox()
        msg_type.setIcon(QMessageBox.Critical)
        msg_type.setText("This type is not valid. Add new type to proceed.")
        msg_type.setWindowTitle("Invalid Operation")
        msg_type.setStandardButtons(QMessageBox.Ok)
        msg_type.exec_()

    @staticmethod
    def msg_box_date_format():
        msg_date = QMessageBox()
        msg_date.setIcon(QMessageBox.Critical)
        msg_date.setText("Wrong date format. Correct format (dd/mm/yyyy)")
        msg_date.setWindowTitle("Invalid Operation")
        msg_date.setStandardButtons(QMessageBox.Ok)
        msg_date.exec_()

    @staticmethod
    def msg_box_date_future():
        msg_date = QMessageBox()
        msg_date.setIcon(QMessageBox.Critical)
        msg_date.setText("Enter valid date")
        msg_date.setWindowTitle("Invalid Operation")
        msg_date.setStandardButtons(QMessageBox.Ok)
        msg_date.exec_()

    @staticmethod
    def validate_date(changed_date):
        try:
            datetime.datetime.strptime(changed_date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_type(changed_type):
        return changed_type.lower() in (c.lower() for c in Collectible.TYPE_LIST)

    @staticmethod
    # todo: convert format of date
    def replace_item(selected_item, selected_column, new_item):
        if selected_column == 0:
            selected_item.name = str(new_item.text()).strip()
        elif selected_column == 1:
            selected_item.type = str(new_item.text()).strip().capitalize()
        elif selected_column == 2:
            selected_item.date_manufactured = datetime.datetime.strptime(str(new_item.text()).strip(), "%d/%m/%Y").date()
        elif selected_column == 3:
            selected_item.date_added = datetime.datetime.strptime(str(new_item.text()).strip(), "%d/%m/%Y").date()
        elif selected_column == 4:
            selected_item.description = str(new_item.text()).strip().capitalize()

        return selected_item
