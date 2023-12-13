import time
# import subprocess
from typing import Union
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pyautogui
# from pprint import pprint
from linkedin_scraper import actions
from selenium.common.exceptions import TimeoutException

class VideoRecorder:
    def __init__(self, email, password, linkedin_email, linkedin_pass, file_name):
        self.email = email
        self.password = password
        self.linkedin_email = linkedin_email
        self.linkedin_pass = linkedin_pass
        self.driver = self.init_driver()
        self.x_axis = [114, 310, 540, 740, 970, 1200, 1400, 1650]
        self.file_name = file_name

    def init_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        driver = uc.Chrome(driver_executable_path="driver/chromedriver.exe", options=options)
        driver.execute_script("window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);")
        return driver

    def login_ahref(self):
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
        self.driver.get("https://app.ahrefs.com/user/login")
        time.sleep(40)

    def data_serializer(self, row) -> dict:
        return {
        "domain": {
            "url": "https://" + row['domain'] if not pd.isna(row['domain']) else "",
            "tabIndex": None,
            "x": None,
        },
        "ahrefs_bk": {
            "url": row['ahrefs url backlink'] if not pd.isna(row['ahrefs url backlink']) and "https" in row['ahrefs url backlink'] else "",
            "tabIndex": None,
            "x": None,
        },
        "ahrefs_kw": {
            "url": row['ahrefs url keyword'] if not pd.isna(row['ahrefs url keyword']) and "https" in row[
                'ahrefs url keyword'] else "",
            "tabIndex": None,
            "x": None,
        },
        "backlink1": {
            "url": row['backlink1'] if not pd.isna(row['backlink1']) and "https" in row['backlink1'] else "",
            "tabIndex": None,
            "x": None,
        },
        "backlink2": {
            "url": row['backlink2'] if not pd.isna(row['backlink2']) and "https" in row['backlink2'] else "",
            "tabIndex": None,
            "x": None,
        },
        "landing_page": {
            "url": row['landing page'] if not pd.isna(row['landing page']) and "https" in row['landing page'] else "",
            "tabIndex": None,
            "x": None,
        },
        "linkedin_1": {
            "url": row['linkedin 1st'] if not pd.isna(row['linkedin 1st']) and "https" in row['linkedin 1st'] else "",
            "tabIndex": None,
            "x": None,
        },
        "linkedin_2": {
            "url": row['linkedin 2nd'] if not pd.isna(row['linkedin 2nd']) and "https" in row['linkedin 2nd'] else "",
            "tabIndex": None,
            "x": None,
        }
    }

    def fill_x_axies(self, data: dict) -> dict:
        print(86)
        index = 0
        for key in data.keys():
            if data[key]['url'] != '':
                print("DATA KEY TAB INDEX ", data[key]['tabIndex'])
                data[key]['x'] = self.x_axis[data[key]['tabIndex']]
                index += 1
        return data

    def open_in_new_tab(self, url: str) -> Union[int, None]:
        try:
            self.driver.execute_script(f"window.open('about:blank', '_blank');")
            # print(97)
            # a = self.driver.tab_new(url)
            # print(23, a)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(url)
            return len(self.driver.window_handles) - 1
        except TimeoutException:
            self.driver.refresh()
            return len(self.driver.window_handles) - 1
        except Exception as e:
            print("EEEEEEEEEEEEEE", e)
            return None

    def open_windows(self, data: dict) -> dict:
        self.opened_tabs = []
        for key in data.keys():
            if data[key]['url'] != '':
                data[key]['tabIndex'] = self.open_in_new_tab(data[key]['url'])
                self.opened_tabs.append(data[key]['tabIndex'])
        return data

    def switch_to_tab_by_index(self, tab_index: int):
        self.driver.switch_to.window(self.driver.window_handles[tab_index])
    
    def play_scenar_saas(self, data: dict) -> bool:
        try:
            # saas scenar 2 mouse + 5 record + 55 scenar = 62 1:02
            #domain
            self.move_mouse(data['domain']['x'])
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            time.sleep(13)
            #ahref
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk']['x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(5)
            #backlink1
            if data['backlink1']['url'] != '' and data['backlink1']['tabIndex'] is not None and data['backlink1']['x'] is not None:
                self.move_mouse(data['backlink1']['x'])
                self.switch_to_tab_by_index(data['backlink1']['tabIndex'])
            time.sleep(4)
            #backlink2
            if data['backlink2']['url'] != '' and data['backlink2']['tabIndex'] is not None and data['backlink2']['x'] is not None:
                self.move_mouse(data['backlink2']['x'])
                self.switch_to_tab_by_index(data['backlink2']['tabIndex'])
            time.sleep(8)
            #domain
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk'][
                'x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(25)

            return True
        except:
            return False

    def play_scenar_pbn(self, data: dict) -> bool:
        try:
            # pbn scenar 2+5+52 = 0:59
            #domain
            self.move_mouse(data['domain']['x'])
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            time.sleep(8)
            #ahref
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk']['x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(3)
            #backlink1
            if data['backlink1']['url'] != '' and data['backlink1']['tabIndex'] is not None and data['backlink1']['x'] is not None:
                self.move_mouse(data['backlink1']['x'])
                self.switch_to_tab_by_index(data['backlink1']['tabIndex'])
            time.sleep(3)
            #backlink2
            if data['backlink2']['url'] != '' and data['backlink2']['tabIndex'] is not None and data['backlink2']['x'] is not None:
                self.move_mouse(data['backlink2']['x'])
                self.switch_to_tab_by_index(data['backlink2']['tabIndex'])
            time.sleep(7)
            #domain
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk'][
                'x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(31)

            return True
        except:
            return False

    def play_scenar_nb_30(self, data):
        try:
            
            """
                No Backlinks 10  1:24 79 play + 5 record + 1.2 rec = 84
            """
            #domain
            self.move_mouse(data['domain']['x'])
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            time.sleep(29)
            #ahref
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk']['x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(1)
            if data['ahrefs_kw']['url'] != '' and data['ahrefs_kw']['tabIndex'] is not None and data['ahrefs_kw'][
                'x'] is not None:
                self.move_mouse(data['ahrefs_kw']['x'])
                self.switch_to_tab_by_index(data['ahrefs_kw']['tabIndex'])
            time.sleep(47.8)
            return True
        except:
            return False

    def play_scenar_nb_20(self, data):
        try:
            
            """
                No Backlinks 20 65.8 scenar + 1.2 mouse + 5 record = 72 1:12
            """
            #domain
            self.move_mouse(data['domain']['x'])
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            time.sleep(11)
            #ahref
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk']['x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(14)
            if data['ahrefs_kw']['url'] != '' and data['ahrefs_kw']['tabIndex'] is not None and data['ahrefs_kw'][
                'x'] is not None:
                self.move_mouse(data['ahrefs_kw']['x'])
                self.switch_to_tab_by_index(data['ahrefs_kw']['tabIndex'])
            time.sleep(40.8)
            return True
        except:
            return False    

    def play_scenar_nb_10(self, data):
        try:
            """
                No Backlinks 30 1:10 63.8 + 5 + 1.2 = 70
            """
            #domain
            self.move_mouse(data['domain']['x'])
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            time.sleep(13)
            #ahref
            if data['ahrefs_bk']['url'] != '' and data['ahrefs_bk']['tabIndex'] is not None and data['ahrefs_bk']['x'] is not None:
                self.move_mouse(data['ahrefs_bk']['x'])
                self.switch_to_tab_by_index(data['ahrefs_bk']['tabIndex'])
            time.sleep(12)
            if data['ahrefs_kw']['url'] != '' and data['ahrefs_kw']['tabIndex'] is not None and data['ahrefs_kw'][
                'x'] is not None:
                self.move_mouse(data['ahrefs_kw']['x'])
                self.switch_to_tab_by_index(data['ahrefs_kw']['tabIndex'])
            time.sleep(38.8)  # 67 - 63.8
            return True
        except:
            return False

    def choose_scenar(self, data: dict, scenar: str) -> bool:
        if scenar == "saas":
            result = self.play_scenar_saas(data)
        elif scenar == "pbn":
            result = self.play_scenar_pbn(data)
        elif scenar == "30 backlinks":
            result = self.play_scenar_nb_30(data)
        elif scenar == "20 backlinks":
            result = self.play_scenar_nb_20(data)
        elif scenar == "10 backlinks":
            result = self.play_scenar_nb_10(data)
        else:
            result = False
        return result

    def close_tabs(self):
        while len(self.driver.window_handles) > 1:
            print("WINDOWS", len(self.driver.window_handles))
            try:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()
            except Exception as e:
                print(e)
                continue
            self.driver.switch_to.window(self.driver.window_handles[0])

    def browser_automation(self, data: dict, scenar: str) -> bool:
        # Implement the logic for browser automation
        try:
            self.close_tabs()
            self.driver.get("https://google.com")
            data = self.open_windows(data)
            data = self.fill_x_axies(data)
            print(data)
            self.switch_to_tab_by_index(data['domain']['tabIndex'])
            self.start_record_video()
            result = self.choose_scenar(data, scenar)
            self.stop_record_video()
            return result
        except Exception as e:
            print(e)
            self.close_tabs()
            return False

    def move_mouse(self, x: int):
        time.sleep(0.1)
        pyautogui.moveTo(x=x, y=22)
        time.sleep(0.3)

    def start_record_video(self):
        time.sleep(2)
        pyautogui.hotkey("winleft", "altleft", "r")
        time.sleep(3)
    
    def stop_record_video(self):
        time.sleep(2)
        pyautogui.hotkey("winleft", "altleft", "r")
        time.sleep(4)

    def run(self):
        self.login_ahref()
        time.sleep(10)
        actions.login(self.driver, self.linkedin_email, self.linkedin_pass)
        time.sleep(20)
        df = pd.read_csv(self.file_name)
        self.start_record_video()
        time.sleep(5)
        self.start_record_video()
        for index, row in df.iterrows():
            if row['Result'] not in ["True", True]:
                data = self.data_serializer(row)
                time.sleep(1)
                result = self.browser_automation(data, row['Scenar'].lower())
                df.at[index, 'Result'] = str(result)
                # Close the driver after processing all rows
                df.to_csv(self.file_name, index=False)
        self.driver.quit()
