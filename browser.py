import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import Dict, Union, Literal
from collections import defaultdict

# Hardcoded variables
white_list_url = r"https://www.podatki.gov.pl/wykaz-podatnikow-vat-wyszukiwarka"


class Browser:
    def __init__(self, url: str) -> None:
        """ Creates a Chrome browser object.
        :param url:-> url of main page as string
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
        """ Launches all methods mostly for debugging purposes.
        :return:
        """
        self.select_validation_method(2)
        self.input_number("5932167267")
        self.submit_button()
        print(self.get_results())

    def select_validation_method(self, via: Literal[1, 2, 3]):
        """ Select method of validation on webpage.
        :param via:-> 1-bank account; 2-NIP; 3-REGON
        :return:
        """
        time.sleep(1)
        via_xpath = fr'//*[@id="wyszukiwarka"]/div[1]/div[1]/fieldset[{via}]/label/span'
        self.driver.find_element(By.XPATH, via_xpath).click()

    def input_number(self, number: str):
        """ Input a number in searching input field on webpage.
        :param number:-> number as a numeric string
        :return:
        """
        time.sleep(1)
        self.driver.find_element(By.XPATH, r'//*[@id="inputType"]').clear()
        self.driver.find_element(By.XPATH, r'//*[@id="inputType"]').send_keys(number)

    def submit_button(self):
        """ Click submit button on webpage.
        :return:
        """
        time.sleep(1)
        self.driver.find_element(By.XPATH, r'//*[@id="sendTwo"]').click()

    def get_results(self) -> dict:
        """ Scrapes all required data from the webpage.
        :return:-> dict with results or errors
        """
        results: Dict[str, Union[str, list]] = defaultdict(list)
        time.sleep(1)
        # check if error on webpage is displayed
        error_box_visible = self.driver.find_element(By.XPATH, r'//*[@id="errorBox"]').is_displayed()
        if error_box_visible:  # get error message to results
            error_xpath = r'//*[@id="errorBox"]/div/div[1]/h4'
            error_msg = self.driver.find_element(By.XPATH, error_xpath).get_property("innerText")
            results["error"] = error_msg
        else:  # get all data
            try:
                # nip and regon scraping
                nip_xpath = r'//*[@id="akmf-nip"]/tbody/tr/td[2]'
                results["nip"] = self.driver.find_element(By.XPATH, nip_xpath).get_property("innerText")
                regon_xpath = r'//*[@id="akmf-regon"]/tbody/tr/td[2]'
                results["regon"] = self.driver.find_element(By.XPATH, regon_xpath).get_property("innerText")

                # bank accounts scraping (could be many)
                bank_xpath = "//*[starts-with(@id, 'akmf-residenceAddress-row-')]"
                bank_accounts_paths = self.driver.find_elements(By.XPATH, bank_xpath)
                for row, _ in enumerate(bank_accounts_paths):
                    current_xpath = f'//*[@id="akmf-residenceAddress-row-{row}"]'
                    results["bank"].append(self.driver.find_element(By.XPATH, current_xpath).get_property("innerText"))
            except Exception:
                results["error"] = "Scraping error"
        return results


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    white_list_obj = WhiteListBrowser(url=white_list_url)
    white_list_obj()
    time.sleep(2)
    white_list_obj.driver.quit()
