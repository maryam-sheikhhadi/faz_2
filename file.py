import csv
import os


class FileHandler:
    def __init__(self, path):
        self.path = path

    def read_file(self):
        list_content = []
        try:
            with open(self.path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                list_content = [item for item in csv_reader]  # list(csv_reader)
        except Exception as ex:
            print(ex)
        return list_content

    def write_file(self, info, mode='a'):
        if isinstance(info, dict):
            if not self.check_unique_username(info['username']):
                print('this username already exists')
                return True
            fields = info.keys()
            info = [info]
        elif isinstance(info, list):
            fields = info[0].keys()
        with open(self.path, mode) as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(info)
            print('you are registerd')
        return False

    def edit_row(self, new_info):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row['username'] == str(new_info['username']):
                row = new_info
            final_rows.append(row)
        self.write_file(final_rows, mode='w')

    def check_unique_username(self, username):
        all_rows = self.read_file()
        for row in all_rows:
            if row['username'] == username:
                return False
        return True

    def delete_row(self, to_username):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row['to_username'] == to_username:
                continue
            final_rows.append(row)
        self.write(final_rows)

    def delete_row_2(self, to_username):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row['to_username'] == to_username:
                continue
            final_rows.append(row)
        for row in final_rows:
            self.write(row)

    def write(self, kwargs):

        try:
            with open(self.path, 'a', newline='') as csvfile:

                fieldnames = list(kwargs.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if len(open(self.path).readlines()) == 0:
                    writer.writeheader()
                writer.writerow(kwargs)
        except Exception as ex:
            print(ex)

        return
