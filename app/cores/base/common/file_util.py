import json
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
            return json_content
    except FileNotFoundError as e:
        print("文件为空")


def write_file(file_path):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            json_content = json.load(file)
            return json_content
    except FileNotFoundError as e:
        print("文件为空")