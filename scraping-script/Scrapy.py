from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# from util import *
import time
import re
import datetime
import shutil
import os
import codecs

# import yaml
import json
import codecs
import pymysql
from multiprocessing import Pool

# import os

# duplicate errorを非表示にする
from warnings import filterwarnings

filterwarnings("ignore", category=pymysql.Warning)


def is_int(s):
    try:
        int(s)
    except:
        return False
    return True


def open_json(filename):
    with open(filename, "r") as f:
        yaml_data = json.load(f)
        return yaml_data


def get_config():
    config = open_json("config.json")
    return config


def create_connection():
    db_config = get_config()["db"]

    connection = pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        db=db_config["db"],
        charset=db_config["charset"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


def close_connection(connection=None):
    if not connection:
        return
    else:
        connection.commit()
        connection.close()


# class User:
#     def __init__(self, id, follower_total, url, profile_icon):
#         self.id = id
#         self.follower_total = follower_total
#         self.url = url
#         self.profile_icon = profile_icon


class Subscriber:
    def __init__(self, id, url, icon):
        self.id = id
        self.url = url
        self.icon = icon


class OnePageScrapy:
    def __init__(self, id, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        )
        self.driver = webdriver.Chrome(
            options=options, executable_path="./chromedriver"
        )
        self.id = id
        self.url = url
        self.follower_count = 0
        self.re_access_count = 0
        self.is_reaccess = False

        # self.subscribers = []

    # def __del__(self):
    #     self.disconnect()

    def connect(self):
        self.driver.get(self.url)
        time.sleep(0.2)
        self.driver.get(self.driver.current_url + "about")

    def disconnect(self):
        self.driver.quit()

    def fetch(self):
        conn = create_connection()
        with conn.cursor() as cursor:
            try:
                # time.sleep(0.1)
                self.connect()
                self.follower_count = self.driver.find_element_by_class_name(
                    "about-subscription-count"
                ).text
                self.follower_count = self.follower_count.replace("人", "").replace(
                    " people", ""
                )

                print(self.follower_count)

                bio = self.driver.find_element_by_xpath(
                    '//*[@id="box2-inner"]/div[1]/div[2]/div[1]'
                ).text
                print(bio)

                if is_int(self.follower_count) and int(self.follower_count) > 0:
                    cursor.execute(
                        "UPDATE users SET follower_total = %s WHERE id = %s",
                        (int(self.follower_count), self.id),
                    )

                cursor.execute(
                    "UPDATE users SET bio = %s WHERE id = %s", (bio, self.id)
                )

                # グラフを1/1スケールにする
                if (
                    self.is_reaccess == False
                    and self.re_access_count == 0
                    and is_int(self.follower_count)
                    and int(self.follower_count) >= 100
                ):
                    self.re_access_count = int(int(self.follower_count) / 100) - 1

                print(self.re_access_count)
                subscribers = self.driver.find_elements_by_class_name("subscriber")

                for subscriber in subscribers:
                    subscriber_profile = subscriber.find_element_by_tag_name("img")
                    id = subscriber_profile.get_attribute("title")
                    url = subscriber.get_attribute("href")
                    icon = subscriber_profile.get_attribute("src")
                    print(id, url, icon)

                    cursor.execute(
                        "INSERT IGNORE INTO users (id, url, icon) VALUES (%s, %s, %s);",
                        (id, url, icon),
                    )
                    cursor.execute(
                        "INSERT IGNORE INTO follows (follow_by, follow_to) VALUES (%s, %s)",
                        (id, self.id),
                    )

                cursor.execute("UPDATE users SET checked = 1 WHERE id = %s", (self.id))
            except NoSuchElementException:
                cursor.execute("UPDATE users SET checked = 1 WHERE id = %s", (self.id))

        close_connection(conn)

        if self.re_access_count > 0:
            self.re_access_count = self.re_access_count - 1
            self.is_reaccess = True
            self.fetch()

        self.disconnect()


if __name__ == "__main__":
    t1 = time.time()
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, url FROM users WHERE checked = 0 LIMIT 100")
        no_check_users = cursor.fetchall()

        def search(no_check_user):
            scrapy = OnePageScrapy(no_check_user["id"], no_check_user["url"])
            scrapy.fetch()

        with Pool(processes=3) as pool:
            pool.map(search, no_check_users)
        # for no_check_user in no_check_users:
        #     scrapy = OnePageScrapy(no_check_user['id'], no_check_user['url'])
        #     scrapy.fetch()

    close_connection(conn)

    # 処理後の時刻
    t2 = time.time()

    # 経過時間を表示
    elapsed_time = t2 - t1
    print(f"経過時間：{elapsed_time}")
