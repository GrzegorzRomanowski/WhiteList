import time
from typing import Dict, Union
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as DWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Hardcoded constants
WHITE_LIST_URL = r"https://www.podatki.gov.pl/wykaz-podatnikow-vat-wyszukiwarka"
WAIT_TIME = 2


class Browser:
    def __init__(self, url: str):
        """ Creates a Chrome browser object.
        :param url: url of main page as string
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
        # self.options.add_argument("--headless")  # in background
        self.options.add_experimental_option('detach', True)


class WhiteListBrowser(Browser):
    URL = WHITE_LIST_URL

    def __call__(self):
        """ Launches all methods mostly for debugging purposes.
        :return:
        """
        self.select_validation_method(2)
        self.input_number("5932167267")
        self.type_date("22-04-2024")
        self.submit_button()
        print(self.get_results())

    def select_validation_method(self, via: int):
        """ Select method of validation on webpage.
        :param via: 1-bank account; 2-NIP; 3-REGON
        :return:
        """
        via_xpath = fr'//*[@id="wyszukiwarka"]/div[1]/div[1]/fieldset[{via}]/label/span'
        try:
            DWait(self.driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, via_xpath)))
        except TimeoutException:
            raise TimeoutException("Timeout reached while selecting method of validation.")
        self.driver.find_element(By.XPATH, via_xpath).click()

    def input_number(self, number: str):
        """ Input a number in searching input field on webpage.
        :param number: number as a numeric string
        :return:
        """
        input_number_xpath = r'//*[@id="inputType"]'
        try:
            DWait(self.driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, input_number_xpath)))
        except TimeoutException:
            raise TimeoutException("Timeout reached while typing a number.")
        self.driver.find_element(By.XPATH, input_number_xpath).clear()
        self.driver.find_element(By.XPATH, input_number_xpath).send_keys(number)

    def type_date(self, date_str: str):
        """ Select the checkbox 'Zmień datę' and type a new one.
        :param date_str: new date to be typed
        :return:
        """
        # Click checkbox
        self.driver.find_element(By.XPATH, r'//*[@id="submit"]/div[2]/div[3]/div[2]/div[2]/div/div/label').click()
        # Wait for input activation
        try:
            DWait(self.driver, WAIT_TIME).until(ec.element_to_be_clickable((By.XPATH, r'//*[@id="inputType3"]')))
        except TimeoutException:
            raise TimeoutException("Timeout reached while typing date.")
        # Perform keys actions (simple clear and send keys didn't work because of active calendar)
        date_input_element = self.driver.find_element(By.XPATH, r'//*[@id="inputType3"]')
        actions = ActionChains(self.driver)
        actions.move_to_element(date_input_element).click()
        actions.send_keys(Keys.BACKSPACE * 10)
        actions.send_keys(date_str)
        actions.perform()
        # Click on the other input above, only for the calendar to disappear.
        self.driver.find_element(By.XPATH, r'//*[@id="inputType"]').click()

    def submit_button(self):
        """ Click submit button on webpage. On first run button has id="sendTwo", on next run id="sendOne".
        :return:
        """
        try:
            one = DWait(self.driver, WAIT_TIME).until(ec.element_to_be_clickable((By.XPATH, r'//*[@id="sendOne"]')))
            one.click()
        except TimeoutException:
            two = DWait(self.driver, WAIT_TIME).until(ec.element_to_be_clickable((By.XPATH, r'//*[@id="sendTwo"]')))
            two.click()

    def get_results(self) -> Dict[str, Union[str, list]]:
        """ Scrapes all required data from the webpage.
        :return: dict with results or errors
        """
        results: Dict[str, Union[str, list]] = defaultdict(list)
        # Check if error on webpage is displayed.
        DWait(self.driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, r'//*[@id="errorBox"]')))
        error_box_visible = self.driver.find_element(By.XPATH, r'//*[@id="errorBox"]').is_displayed()

        if error_box_visible:  # get error message to results
            error_xpath = r'//*[@id="errorBox"]/div/div[1]/h4'
            error_msg = self.driver.find_element(By.XPATH, error_xpath).get_property("innerText")
            results["error"] = error_msg
        else:  # get all data
            try:
                # main info
                info_xpath = r'//*[@id="tableOne"]/div[1]/div/h4'
                DWait(self.driver, WAIT_TIME).until(ec.presence_of_element_located((By.XPATH, info_xpath)))
                results["info"] = self.driver.find_element(By.XPATH, info_xpath).get_property("innerText")
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
            except (NoSuchElementException, TimeoutException):
                results["error"] = "Scraping error"
        return results


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    white_list_obj = WhiteListBrowser(url=WHITE_LIST_URL)
    white_list_obj()
    time.sleep(5)
    white_list_obj.driver.quit()
