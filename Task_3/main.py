import re
import sys

def parse_array(nesting, array_str):
    array_str = array_str.strip()

    if not array_str:
        return None
    if array_str[0] != "[" or array_str[-1] != "]":
        return None
    
    array_str = array_str[1:-1]
    result = "\n"
    for elem in array_str.split():
        if not elem:
            return None
        result += f"{'  ' * (nesting + 1)}- {elem}\n"

    return result

def parse_value(value):
    pass

def parse_config(file_content):
    lines = file_content.splitlines()
    result = ""
    nesting = 0
    is_dict = False

    for num, line in enumerate(lines):
        line = line.strip()

        if nesting > 0:
            is_dict = True
        else:
            is_dict = False

        # Пустая строка
        if not line:
            continue

        # Комментарий
        if line.startswith('!'):
            result += f"{'  ' * nesting}# {line[1:].strip()}\n"

        # Константы
        const_match = re.match(r"^[a-zA-Z]+", line)
        if const_match:
            name = const_match.group()

            if not is_dict and line[len(name)] != ":":
                raise ValueError(f"Неверный формат константы: {line} (строка {num + 1})")
            if is_dict and line[len(name):len(name) + 2] != " =":
                raise ValueError(f"Неверный формат элемента словаря: {line} (строка {num + 1})")

            if is_dict:
                value = line[len(name) + 2:].strip()
            else:
                value = line[len(name) + 1:].strip()

            if value == "":
                raise ValueError(f"Пустое значение константы: {line} (строка {num + 1})")
            else:
                result += f"{'  ' * nesting}{name}:"

            if value == "{":
                result += "\n"
                nesting += 1
            elif value.startswith("["):
                array = parse_array(nesting, value)
                if array is None:
                    raise ValueError(f"Неверный формат массива: {line} (строка {num + 1})")
                result += array
            else:
                if not value.isdigit():
                    raise ValueError(f"Неверный формат числа: {line} (строка {num + 1})")
                result += f" {value}\n"
            continue

        # Закрытие словаря
        if line == "}":
            nesting -= 1
            continue

    return result


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
