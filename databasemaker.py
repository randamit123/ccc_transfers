import os
import urllib.request
import json
from collections import defaultdict
from pdfextractor import PDFExtractor


class DatabaseMaker():
    def __init__(self, school_name, major_code, id_to_key):
        self.database = defaultdict(list)
        with urllib.request.urlopen("https://assist.org/api/institutions") as url:
            data = json.loads(url.read().decode())
        self.names = {x['id']: x['names'][0]['name'] for x in list(data)}
        self.major_code = major_code
        self.school_name = school_name
        self.id_to_key = id_to_key

    def alphabetize_class_dict(self, class_dict):
        sorted_classes = sorted(class_dict.keys())
        class_dict = {key: class_dict[key] for key in sorted_classes}
        for key in class_dict.keys():
            sorted_schools = sorted(
                class_dict[key], key=lambda x: x['from_school'])
            class_dict[key] = sorted_schools
        return class_dict

    def add_classes(self):
        for file_name in os.listdir(f'agreements/{self.school_name}/'):
            print(f"Checking file: {file_name}")
            if self.major_code not in file_name or 'report' not in file_name:
                print("Condition not met.")
                continue
            info = file_name.replace('.pdf', '').split('_')
            to_school_id = info[1]
            from_school_id = int(info[2])
            extractor = PDFExtractor(
                f'agreements/{self.school_name}/{file_name}')
            print("Check 1")
            classes = extractor.dict_from_file()
            print("Check 2")
            for to_class in classes.keys():
                print("Check 3")
                from_class = {'school_id': from_school_id,
                              'from_school': self.names[from_school_id],
                              'equiv': classes[to_class],
                              'key': self.id_to_key[from_school_id]}
                self.database[to_class].append(from_class)
        print("Check 4")
        self.database = self.alphabetize_class_dict(self.database)
        print("Check 5")
        json_name = f'agreements/{self.school_name}/{self.major_code}.json'
        with open(json_name, "w") as out_file:
            json.dump(self.database, out_file, indent=4)
        print("Check 6")
