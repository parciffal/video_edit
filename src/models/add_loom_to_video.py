import time
# import subprocess
from typing import Union
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pyautogui
# from pprint import pprint
from linkedin_scraper import actions


class MergeVideos:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = self.init_driver()
        self.x_axis = [114, 310, 540, 740, 970, 1200, 1400, 1650]

    def init_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        driver = uc.Chrome(driver_executable_path="driver/chromedriver.exe", options=options)
        driver.execute_script("window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);")
        return driver

    
    def login_canva(self):
        self.driver.get("https://mail.google.com/")
        input_login = self.driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        input_login.send_keys(self.email)
        _next = self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
        _next.click()
        time.sleep(15)
        input_password = self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        input_password.send_keys(self.password)
        _next = self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
        _next.click()
        time.sleep(60)
        self.driver.get("https://www.canva.com/en_gb/login/")
        time.sleep(40)

    def upload_file(self, file_name):
        file_path = 'C:/Users/User/Videos/Captures'
        for i in range(0, 5):
            pyautogui.press("tab")
        pyautogui.press("enter")
        # need to paste file_path with pyautogui
        pyautogui.press("enter")
        for i in range(0, 5):
            pyautogui.press("tab")


    def run(self):
        self.login_canva()
        time.sleep(20)
        uploads_button = '//*[@id=":r1l:"]'
        self.driver.find_element(By.XPATH, uploads_button).click()
        time.sleep(3)
        upl_botton = '//*[@id=":r1m:"]/div/div/div/div[1]/div/div/div[1]/div[2]/div/div/div/div/button'
        self.driver.find_element(By.XPATH, upl_botton).click()
        # 5 tab enter paste "C:\Users\User\Videos\Captures" enter 5xTab paste filename 2xTab enter