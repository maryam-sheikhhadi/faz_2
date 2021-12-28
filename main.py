import pandas as pd

from file import FileHandler
from signup_singin import User

from user_directory import Box, Inbox, Draft, Sent
from log_handler import *

#MAKE INSTANCE FROM FileHander IN file MODULE FOR WRITE INFO USERS IN info.csv
file_info = FileHandler('info.csv')
list_info = file_info.read_file()

#MENU
while True:
    x = input("1: Don't have an account? Sign up\n2: You have an account? Sign in\n3: quit\n>>>")
    #USER REGISTER
    if x == '1':
        # GET VALID USERNAME
        while True:
            print('rules:\n1) 8-20 characters long\n2) you can use a-z and A-Z and . and _')
            username = input('According to the rules Enter an other username:\n>>>')
            a = User.valid_username(username)
            if a:
                valid_username = username
                break
            else:
                print('Violations of the law have occurred or this username already exists!\ntry again...')
                continue
        #GET VALID PASSWORD
        while True:
            print('rules:\n1) 8-20 characters long\n2) you can use a-z and A-Z and . and _')
            password = input('According to the rules Enter an other password:\n>>>')
            a = User.valid_password(password)
            if a:
                valid_password = password
                break
            else:
                print('Violations of the law have occurred\ntry again...')
                continue
        #CONFIRM PASSWORD
        confirm_password = input('comfirm your password:')
        User.confirm_password(password, confirm_password)
        #MAKE INSTANCE FROM User
        user = User(valid_username, valid_password)
        #WRITE INFO IN FILE
        info = {'username': user.username, 'password': user.pw_hash}
        c = file_info.write_file(info)
        #MAKE DIRECTORY AND INBOX SENT DRAFT FOR USER
        user.directory()
        # WRITE MASSAGE FOR USER AND WLCOME TO HIM/HER
        inbox_file = FileHandler(f'users_info\\{user.username}\inbox.csv')
        inbox_file.write({'Message': f'dear {user.username} welcome to text messanger', 'time': Box.get_time(),
                          'sender': 'massanger', 'is_seen': False})

    #USER LOGIN
    elif x == '2':
        username = input('enter your username:')
        password = input('enter your password:')
        user = User(username, password)
        df_info = pd.read_csv('info.csv')
        result = user.log_in(user.username, user.pw_hash, df_info)

        if result:
            path_inbox = f'users_info\\{user.username}\inbox.csv'
            path_draft = f'users_info\\{user.username}\draft.csv'
            path_sent = f'users_info\\{user.username}\sent.csv'

            #DISPLAY INBOX AND SENT AND DRAFT OF USER AND NUMBER OF MASSAGE IN  BOXES
            try:
                x1 = Box.number_of_massage(path_inbox)
                print(f'number of massage in inbox is: {x1}')
            except:
                print('number of massage in inbox is zero!')

            try:
                x2 = Box.display(path_inbox)
            except:
                print("nothing doesn't exists! inbox is empty!")

            try:
                x1 = Box.number_of_massage(path_draft)
                print(f'number of massage in draft box is: {x1}')
            except:
                print('number of massage in draft box is zero!')

            try:
                x2 = Box.display(path_draft)
            except:
                print("nothing doesn't exists! draft box is empty!")

            try:
                x1 = Box.number_of_massage(path_sent)
                print(f'number of massage in sent box is: {x1}')
            except:
                print('number of massage in sent box is zero!')

            try:
                x2 = Box.display(path_sent)
            except:
                print("nothing doesn't exists! sent box is empty!")

            #MENU AFTER LOG IN FOR USER
            while True:
                y = int(input("""what do you want to do?\n1: write a draft message\n2: write a massage and sent it
                                \n3: send a massage from your draft box\n4: check inbox and read a massage
                                \n5: edit a massage in your draft box\n6: edit a massage that you sent it
                                \n7: delete a massage in your draft box\n8: delete a massage that you sent it 
                                \n9: reply the massage\n10: forward a massage\n11: log out\n>>>"""))
                #1: write a draft message
                if y == 1:
                    # receiver = input('Enter username of receiver?\n>>>')
                    massage = input('write your massage:\n>>>')
                    Draft.write_draft_massage(path_draft, massage)
                    print('I saved your message in your draft box:)')
                #2: write a massage and sent it
                elif y == 2:
                    receiver = input('Enter username of receiver?\n>>>')
                    massage = input('write your massage:\n>>>')
                    Sent.write_massage_and_send(username, receiver, massage)
                    print('I sent your message:)')
                #3: send a massage from your draft box
                elif y == 3:
                    a = Box.display(path_draft)
                    index = int(input('enter number of massage that you want to sent:\n>>>'))
                    receiver = input('Enter username of receiver?\n>>>')
                    Draft.send_draft_massage(user.username, index,receiver, a)
                    print('I sent your message from your draft massage:)')
                #4: check inbox and read a massage
                elif y == 4:
                    a = Box.display(path_inbox)
                    index = int(input('which massage you want to see?\n>>>'))
                    # sender = a.get_value(index, 'sender')
                    Inbox.seen_massage(index, a,user.username)
                    print('you read selected message:)')
                #5: edit a massage in your draft box
                elif y == 5:
                    df_draft = Box.display(path_draft)
                    index = int(input('which massage you want to edit?\n>>>'))
                    new_massage = input('write new massage:\n>>>')
                    df_draft.at[index, 'Message'] = new_massage
                    print('your selected draft massage edited:)')
                #6: edit a massage that you sent it
                elif y == 6:
                    df_sent = Box.display(path_sent)
                    index = int(input('which massage you want to edit?\n>>>'))
                    new_massage = input('write new massage:\n>>>')
                    Sent.edit_sent_massage(df_sent,index,new_massage)
                    print('your massage edited:)')
                #7: delete a massage in your draft box
                elif y == 7:
                    df_draft = Box.display(path_draft)
                    index = int(input('which massage you want to delete from your draft box?\n>>>'))
                    selected = df_draft[index]
                    df_draft.drop([index])
                    df_draft.to_csv(path_draft, index=False)
                    print('your selected draft massage deleted:)')
                #8: delete a massage that you sent it
                elif y == 8:
                    df_sent = Box.display(path_sent)
                    index = int(input('which massage you want to delete?\n>>>'))
                    # receiver = df_sent.get_value(index, 'receiver')
                    Sent.delete_sent_massage(df_sent,index,path_sent)
                    print('your massage deleted:)')
                #9: reply the massage
                elif y == 9:
                    a = Box.display(path_inbox)
                    index = int(input('write index of massage you want reply it:\n>>>'))
                    answer = input('writ your answer:\n>>>')
                    # receiver = a.df.get_value(index, 'sender')
                    receiver = a.iloc[index,2]
                    Sent.write_massage_and_send(user.username, receiver,answer)
                #10: forward a massage
                elif y == 10:
                    a = Box.display(path_inbox)
                    index = int(input('write index of massage you want reply it:\n>>>'))
                    receiver = input('enter the username that forward this massage to him/her:\n>>>')
                    # massage = a.df.get_value(index, 'Message')
                    massage = a.iloc[index,0]
                    Sent.write_massage_and_send(user.username, receiver,massage)
                #log out
                elif y == 11:
                    y = input('are you sure you want to log out? Y or N:')
                    if y.upper() == 'N':
                        continue
                    elif y.upper() == 'Y':
                        logger.info(f'{user.username} loged out')
                        break
                else:
                    y = print("your input is wrong:(\nplease enter correct number")

        else:
            print('somthing is wrong!')
            logger.info(f'Unsuccessful login {user.username}')
            continue



    elif x == '3':
        break


    else:
        print('your input character is not available\nplease enter again')
        continue
