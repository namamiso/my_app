from pystray import Icon, MenuItem, Menu
from PIL import Image
import time
import threading
import schedule
import datetime
import subprocess
from pywinauto import Application
import pygetwindow as gw

class taskTray:
    def __init__(self, image):
        self.status = False

        ## アイコンの画像
        image = Image.open(image)
        ## 右クリックで表示されるメニュー
        menu = Menu(
                    MenuItem('Task', self.doTask),
                    MenuItem('Exit', self.stopProgram),
                )

        self.icon = Icon(name='nameTray', title='titleTray', icon=image, menu=menu)


    def doTask(self):
        print('実行しました。')

        # if gw.getWindowsWithTitle("Steam"):
        #     logger.debug("既に開いています")
        #     return

        app = Application(backend="uia").start("C:\Program Files (x86)\Steam\steam.exe")

        ##exitProcess = terminate(['C:\Program Files (x86)\Steam\steam.exe'])

    def runSchedule(self):
        ## 毎週授業開始時にタスクを実行する。
        schedule.every().monday.at("11:00").do(self.doTask)
        schedule.every().tuesday.at("09:15").do(self.doTask)
        schedule.every().thursday.at("09:15").do(self.doTask)
        schedule.every().friday.at("13:30").do(self.doTask)

        ##テスト用
        schedule.every().thursday.at("14:19").do(self.doTask)

        ## status が True である間実行する。
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def stopProgram(self, icon):
        self.status = False

        ## 停止
        self.icon.stop()

    def runProgram(self):
        self.status = True

        ## スケジュールの実行
        task_thread = threading.Thread(target=self.runSchedule)
        task_thread.start()

        ## 実行
        self.icon.run()


if __name__ == '__main__':
    system_tray = taskTray(image="image.jpg")
    system_tray.runProgram()