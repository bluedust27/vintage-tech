from datetime import date
from typing import List


class Validation:
    ERROR_MESSAGE = ""

    def __init__(self, ui):
        self.ui = ui

    def validate_input(self):
        all_validations: List[bool] = [Validation.__validate_missing_inputs(self.ui), Validation.__validate_manufactured_date(self.ui)]
        is_valid = any(validation is False for validation in all_validations)
        return not is_valid

    def __validate_missing_inputs(self):
        is_valid = True
        if not self.ui.txt_name.text():
            Validation.ERROR_MESSAGE += "Name missing.\n"
            is_valid = False
        if not self.ui.cmb_type.currentText():
            Validation.ERROR_MESSAGE += "Type missing.\n"
            is_valid = False
        if not self.ui.cmb_type.currentText():
            Validation.ERROR_MESSAGE += "Type missing.\n"
            is_valid = False
        if not self.ui.txt_desc.toPlainText():
            Validation.ERROR_MESSAGE += "Description missing.\n"
            is_valid = False
        return is_valid

    def __validate_manufactured_date(self):
        is_valid = True
        if self.ui.date_dateman.date().toPyDate() > date.today():
            Validation.ERROR_MESSAGE += "Enter Valid Manufacturing Date"
            is_valid = False
        return is_valid
