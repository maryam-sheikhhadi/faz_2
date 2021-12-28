import os
import re
import pandas as pd
from hashutils import make_pw_hash
from log_handler import *


class User:
    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        logger.info(f'{self.username} registerd')

    @staticmethod
    def valid_username(username):
        regex = '^(?=.{8,20}$)[a-zA-Z0-9._]+$'
        try:
            df = pd.read_csv('info.csv')
            res = df.isin([username]).any().any()
            if (re.fullmatch(regex, username)) and not res:
                print('valid username')
                return True
        except Exception:
            print(Exception)
            return True
        return False

    @staticmethod
    def valid_password(password):
        regex = '^(?=.{8,20}$)[a-zA-Z0-9._]+$'
        if (re.fullmatch(regex, password)):
            print('valid password')
            return True
        return False

    @staticmethod
    def confirm_password(password, confirm):
        while True:
            if confirm == password:
                print("It's ok:)")
                break
            else:
                confirm = input('oh no :(\nEnter your password again:')
        return confirm

    def directory(self):
        os.chdir('users_info')
        os.mkdir(self.username)
        os.chdir(self.username)
        open('inbox.csv', mode='a+')
        open('draft.csv', mode='a+')
        open('sent.csv', mode='a+')
        print(os.getcwd())
        os.chdir('../../../update_project')

    @staticmethod
    def log_in(username, password, df_info):
        for i in range(df_info.shape[0]):
            if username == df_info.iloc[i,0] and password == df_info.iloc[i,1]:
                print(f'dear {username}! you are log in successfully:)')
                return True
            elif username == df_info.iloc[i,0] or password == df_info.iloc[i,1]:
                print('your username or password is wrong:(')
                continue
            else:
                print("this account doesn't exists! you can sign up:)")
                continue
        return False

    def __str__(self):
        return f"{self.__dict__}"

    def __repr__(self):
        return f"{self.__dict__}"
