import os

from interface import Interface
from config import config_obj
from excel import BulkData


if __name__ == "__main__":
    # Make a dir for bulk data
    if not os.path.exists(config_obj.BULK_DATA_PATH):
        os.makedirs(config_obj.BULK_DATA_PATH)
    if not os.path.exists(rf"{config_obj.BULK_DATA_PATH}/input.xlsx"):
        BulkData.init_input_file(rf"{config_obj.BULK_DATA_PATH}/input.xlsx")

    # Run interface
    gui_obj = Interface()
