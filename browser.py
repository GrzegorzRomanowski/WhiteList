import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import Dict, Union
from collections import defaultdict

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
        self.click_via_account_number(2)  # 1 lub 2, lub 3
        self.input_number("5932167267")
        self.submit_button()
        self.get_results()

    def click_via_account_number(self, via_number: int):
        time.sleep(1)
        via_xpath = fr'//*[@id="wyszukiwarka"]/div[1]/div[1]/fieldset[{via_number}]/label/span'
        self.driver.find_element(By.XPATH, via_xpath).click()

    def input_number(self, number: str):
        time.sleep(1)
        self.driver.find_element(By.XPATH, r'//*[@id="inputType"]').clear()
        self.driver.find_element(By.XPATH, r'//*[@id="inputType"]').send_keys(number)

    def submit_button(self):
        time.sleep(1)
        self.driver.find_element(By.XPATH, r'//*[@id="sendTwo"]').click()

    def get_results(self):
        results: Dict[str, Union[str, list]] = defaultdict(list)
        time.sleep(1)
        error_box_visible = self.driver.find_element(By.XPATH, r'//*[@id="errorBox"]').is_displayed()
        if error_box_visible:
            error_xpath = r'//*[@id="errorBox"]/div/div[1]/h4'
            error_msg = self.driver.find_element(By.XPATH, error_xpath).get_property("innerText")
            results["error"] = error_msg
        else:
            try:
                nip_xpath = r'//*[@id="akmf-nip"]/tbody/tr/td[2]'
                results["nip"] = self.driver.find_element(By.XPATH, nip_xpath).get_property("innerText")
                regon_xpath = r'//*[@id="akmf-regon"]/tbody/tr/td[2]'
                results["regon"] = self.driver.find_element(By.XPATH, regon_xpath).get_property("innerText")

                bank_xpath = "//*[starts-with(@id, 'akmf-residenceAddress-row-')]"
                bank_accounts_paths = self.driver.find_elements(By.XPATH, bank_xpath)
                for row, _ in enumerate(bank_accounts_paths):
                    current_xpath = f'//*[@id="akmf-residenceAddress-row-{row}"]'
                    results["bank"].append(self.driver.find_element(By.XPATH, current_xpath).get_property("innerText"))
            except:
                print("scraping error")
        print(results)
        return results


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    white_list_obj = WhiteListBrowser(url=white_list_url)
    white_list_obj()
    # time.sleep(3)
    # white_list_obj.driver.quit()
