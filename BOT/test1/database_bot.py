# -*- coding: utf-8 -*-
import subprocess
import os

# a = os.system('py F:/1/Documents/"Pycharm Python Project"/"Практика на Python"/BOT/test1/main_bot_test1.py"')
p = subprocess.Popen('py F:/1/Documents/"Pycharm Python Project"/"Практика на Python"/BOT/test1/main_bot_test1.py"', shell = True)
p2 = subprocess.Popen('py F:/1/Documents/"Pycharm Python Project"/"Практика на Python"/BOT/test1/main_bot_test1.py"', shell = True)
print("!!!!!!!!!!!!!!!start")
a = p2.communicate()
print(a)
print("!!!!!!!stop!!!!!!!!!!!!")
# subprocess.Popen('py F:/1/Documents/"Pycharm Python Project"/"Практика на Python"/BOT/test1/main_bot_test1.py"', shell = True)
import peewee
# with subprocess.Popen(['python', "main_bot_test1.py"]) as pros:
#     print("1")
#     pass
# with subprocess.Popen(['python', "main_bot_test1.py"]) as pros1:
#     print("2")