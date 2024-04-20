from browser import WhiteListBrowser
from browser import white_list_url
from interface import Interface


if __name__ == "__main__":
    white_list_obj = WhiteListBrowser(url=white_list_url)
    white_list_obj()

    gui_obj = Interface()
