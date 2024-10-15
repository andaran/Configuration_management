import re
import sys

def parse_config(file_content):
    constants = {}
    lines = file_content.splitlines()

def main(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            yaml_output = parse_config(file_content)
            print(yaml_output)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь к файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
