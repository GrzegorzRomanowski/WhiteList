import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Hardcoded variables
white_list_url = r"https://www.podatki.gov.pl/wykaz-podatnikow-vat-wyszukiwarka"


class Browser:
    def __init__(self, url: str) -> None:
        """ Creates a Chrome browser object.
        :param url: - url of main page as string
        """
        self.URL = url
        self.options = Options()
        self.chrome_options()
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.URL)

    def chrome_options(self):
        """ Setting chrome options such as maximizing the window, not closing the window after script completion, etc.
        :return:
        """
        self.options.add_argument("--start-maximized")  # alternatively > self.driver.maximize_window()
        self.options.add_experimental_option('detach', True)


class WhiteListBrowser(Browser):
    URL = white_list_url

    def __call__(self):
        self.login()

    def login(self):
        self.driver.find_element(By.XPATH, r'//*[@id="UINFO"]').clear()
        self.driver.find_element(By.XPATH, r'//*[@id="UINFO"]').send_keys("example")
        self.driver.find_element(By.XPATH, r'//*[@id="PINFO"]').clear()
        self.driver.find_element(By.XPATH, r'//*[@id="PINFO"]').send_keys("example")
        self.driver.find_element(By.XPATH, r'//*[@id="buttonBar"]/div/div/div[2]/span').click()


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    white_list_obj = WhiteListBrowser(url=white_list_url)
    # white_list_obj()
    time.sleep(3)
    white_list_obj.driver.quit()
