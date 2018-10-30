"""""
Решение

Поздравляем с первой полноценной программой на Python в рамках нашего курса!
Она была заметно сложнее предыдущих и помогла вам разобраться сразу с несколькими
моментами. Хорошим подходом было бы разбить свою программу на функции — обратите внимание,
все команды вынесены в отдельные функции, а get_data мы переиспользуем в нескольких местах.
Ключевым моментом в разработке любого приложения является выбор подходящей структуры данных.
В этом примере логичным вариантом было использовать словарь, потому что он по сути и
является key-value хранилищем, а значения просто хранить в списке.

Также в этом задании мы использовали модуль argparse для считывания аргументов командной
строки и json для хранения данных в файле. Самым простым подходом было просто перечитывать
при каждом обращении файл, преобразуя его в словарь, добавляя значения при необходимости.
Модуль os помогает нам в проверке существования файла хранилища при первом запуске программы.
В Python богатая стандартная библиотека, очень важно представлять себе, какие модули помогут
нам в решении наших задач, и уметь быстро разбираться в документации к новым функциям.

Обратите внимание, в примере мы для простоты используем глобальную переменную, однако в
реальном приложении вы, скорее всего, написали бы для решения похожей задачи свой класс и
инкапсулировали бы в нём информацию о хранилище и его методы. В следующей неделе мы
разберем объектно-ориентированный подход и его плюсы.
"""""
import argparse
import json
import os
import tempfile


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def clear():
    os.remove(storage_path)


def get_data():
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as f:
        raw_data = f.read()
        if raw_data:
            return json.loads(raw_data)

        return {}


def put(key, value):
    data = get_data()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]

    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))


def get(key):
    data = get_data()
    return data.get(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    parser.add_argument('--clear', action='store_true', help='Clear')

    args = parser.parse_args()

    if args.clear:
        clear()
    elif args.key and args.val:
        put(args.key, args.val)
    elif args.key:
        print(get(args.key))
    else:
        print('Wrong command')
