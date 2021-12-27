from file import FileHandler
import pandas as pd
from datetime import datetime
from IPython.display import display
from log_handler import *

class Box:
    @staticmethod
    def number_of_massage(file_path):
        list_file = FileHandler(file_path).read_file()
        return len(list_file)

    @staticmethod
    def display(file_path):

        df = pd.read_csv(file_path)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.precision', 2)
        display(df)
        return df

    @staticmethod
    def get_time():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return f"{self.__dict__}"


class Inbox(Box):
        # a is dataframe of receiver inbox
        # index is index of selected massage
        @staticmethod
        def seen_massage(index, a):
            sender = a.iloc[index, 2]
            a.at[index, 'is_seen'] = True
            df_sender_sent_box = Box.display(f'users_info\\{sender}\sent.csv')
            df_sender_sent_box.at[index, 'is_seen'] = True


class Draft(Box):

    @staticmethod
    def write_draft_massage(path_draft, receiver, massage):
        a = FileHandler(path_draft)
        a.write({'Message': massage, 'time': Box.get_time(), 'receiver': receiver, 'is_seen': False})

    @staticmethod
    def send_draft_massage(sender, index, df_draft_sender):
        selected = df_draft_sender[index]
        receiver = df_draft_sender.get_value(index, 'receiver')
        path_inbox_receiver = f'users_info\\{receiver}\inbox.csv'
        df_inbox_receiver = pd.read_csv(path_inbox_receiver)
        df_new_inbox_receiver = df_inbox_receiver.append(selected, ignore_index=True)
        df_new_inbox_receiver.to_csv(path_inbox_receiver, index=False)
        path_sent_box_sender = f'users_info\\{sender}\sent.csv'
        df_sent_box_sender = pd.read_csv(path_sent_box_sender)
        df_new_sent_box_sender = df_sent_box_sender.append(selected, ignore_index=True)
        df_new_sent_box_sender.to_csv(path_sent_box_sender, index=False)
        df_draft_sender.drop([index])
        path_draft_box_sender = f'users_info\\{sender}\draft.csv'
        df_draft_sender.to_csv(path_draft_box_sender, index=False)
        logger.info(f'{sender} sent massage')

    def __str__(self):
        return f"{self.__dict__}"


class Sent(Box):

    @staticmethod
    def write_massage_and_send(sender, receiver, massage):
        path_receiver = f'users_info\\{receiver}\inbox.csv'
        a = FileHandler(path_receiver)
        a.write({'Message': massage, 'time': Box.get_time(), 'sender': sender, 'is_seen': False})
        path_sender = f'users_info\\{sender}\sent.csv'
        b = FileHandler(path_sender)
        b.write({'Message': massage, 'time': Box.get_time(), 'receiver': receiver, 'is_seen': False})
        logger.info(f'{sender} sent massage')

    @staticmethod
    def edit_sent_massage(df_sent,index,new_massage):
        df_sent.at[index, 'Message'] = new_massage
        receiver = df_sent.iloc[index, 2]
        path_inbox_receiver = f'users_info\\{receiver}\inbox.csv'
        df_inbox_receiver = pd.read_csv(path_inbox_receiver)
        df_inbox_receiver.at[index, 'Message'] = new_massage

    @staticmethod
    def delete_sent_massage(df_sent, index, path_sent):
        receiver = df_sent.iloc[index, 2]
        inbox_receiver = f'users_info\\{receiver}\draft.csv'
        df_inbox_receiver = pd.read_csv(inbox_receiver)
        df_sent.drop([index])
        df_inbox_receiver.drop([index])
        df_sent.to_csv(path_sent, index=False)
        df_inbox_receiver.to_csv(inbox_receiver, index=False)

    def __str__(self):
        return f"{self.__dict__}"
