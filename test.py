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

        self.icon = Icon(name='nameTray', title='eroge_Destroyer', icon=image, menu=menu)

    ##時間が来たら実行される処理
    def doTask(self):
        # 終了したいアプリが起動していた場合
        if gw.getWindowsWithTitle("Steam"):
            # 終了させたい.exeファイルの名前を指定
            executable_name = "steam.exe"

            # 終了させる
            subprocess.run(["taskkill", "/IM", executable_name, "/F"], check=True)

            return

    def runSchedule(self):
        ## 毎週授業開始時にタスクを実行する。
        schedule.every().monday.at("11:00").do(self.doTask)
        schedule.every().tuesday.at("09:15").do(self.doTask)
        schedule.every().thursday.at("09:15").do(self.doTask)
        schedule.every().friday.at("13:30").do(self.doTask)

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