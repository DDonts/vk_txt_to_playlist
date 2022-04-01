import os
import time
import configparser
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


cfg = configparser.ConfigParser()
path = 'config.cfg'
cfg.read(path)

FILE_NAME = cfg['CONFIG']['FILE_NAME']
USERNAME = cfg['CONFIG']['USERNAME']
PASSWORD = cfg['CONFIG']['PASSWORD']


class Process:
    def __init__(self, file_name):
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/93.0.4577.63 Safari/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.browser = webdriver.Chrome('chromedriver', options=options)

        self.url = 'https://vk.com/'
        self.username = USERNAME
        self.password = PASSWORD
        self.timeout = timedelta(seconds=30)
        self.song_list = []
        self.file_name = file_name
        self.counter = 0

    def main(self):
        self.get_song_list()
        self.login()
        self.go_to_music()
        self.new_playlist()
        self.add_songs()

    def get_song_list(self):
        file_path = os.path.join(os.path.join(os.path.join
                                              (os.environ['USERPROFILE']), 'Desktop'), f'{self.file_name}.txt')

        with open(file_path, encoding='utf-8') as f:
            for i in f:
                self.song_list.append(i)

        self.song_list.reverse()
        print(f'Found {len(self.song_list)} songs!')

    def login(self):
        self.browser.get(self.url)

        start_login_button = '//*[@id="index_login"]/div/form/button[1]'
        start_login_button_element = self.__find_element(xpath=start_login_button)
        start_login_button_element.click()

        username_input = "//input[@name='login']"
        username_input_element = self.__find_element(xpath=username_input)
        username_input_element.send_keys(self.username)

        username_login_button = "//button[@type='submit']"
        username_login_button_element = self.__find_element(xpath=username_login_button)
        username_login_button_element.click()

        password_input = "//input[@name='password']"
        password_input_element = self.__find_element(password_input, timeout=20)
        password_input_element.send_keys(self.password)

        password_login_button = "//button[@type='submit']"
        password_login_button_element = self.__find_element(xpath=password_login_button)
        password_login_button_element.click()

    def go_to_music(self):
        music_button = '//*[@id="l_aud"]'
        music_button_element = self.__find_element(music_button)
        music_button_element.click()

    def new_playlist(self):
        playlist_button = "//a[@href='/audios264764427?section=all']"
        playlist_button_element = self.__find_element(playlist_button)
        playlist_button_element.click()

        playlist_button = '//*[@id="content"]/div/div[3]/div[1]/h2/ul/button[2]'
        playlist_button_element = self.__find_element(playlist_button)
        playlist_button_element.click()

        playlist_name = "//input[@id='ape_pl_name']"
        playlist_name_element = self.__find_element(playlist_name)
        playlist_name_element.send_keys(self.file_name)

        save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
        save_playlist_element = self.__find_element(save_playlist)
        save_playlist_element.click()

    def add_songs(self):

        for song in self.song_list:

            playlist = "//div[@class='audio_pl__actions_btn audio_pl__actions_edit']"
            playlist_element = self.__find_element(playlist)
            try:
                playlist_element.click()
            except:
                time.sleep(3)
                playlist_element.click()

            song_search = '//input[@id="ape_edit_playlist_search"]'
            song_search_element = self.__find_element(xpath=song_search)
            song_search_element.send_keys(song)

            try:
                found_song_list = '//*[@id="box_layer"]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]'
                found_song_list_element = self.__find_element(found_song_list)
                found_song_list_element.click()
                self.counter += 1
                print(f'Added {self.counter}-th song')
            except:
                print(f'Can\'n add {song}')
                self.song_list.remove(song)

            song_search_element.clear()

            save_playlist = "//button[@class='FlatButton FlatButton--primary FlatButton--size-m']"
            save_playlist_element = self.__find_element(save_playlist)
            save_playlist_element.click()

        print(f'\n\n____Added {len(self.song_list)} songs!!____')
        self.browser.quit()

    def __find_element(self, xpath: str, timeout: int = 5) -> WebElement or None:
        try:
            element = WebDriverWait(self.browser, timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            return None


if __name__ == '__main__':
    process = Process(FILE_NAME)
    process.main()
