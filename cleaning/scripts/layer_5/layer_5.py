import json as _json
import locale
from os import listdir as _listdir
from re import search as _search

from alive_progress import alive_bar

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def dict_walk(input_dict):
    null = None
    try:
        for key, value in input_dict.items():
            if isinstance(value, dict):
                dict_walk(value)
            elif isinstance(value, list):
                pass
            elif isinstance(value, str) and (key != 'ipeds_unitid' and key != 'opeid' and key != 'opeid6' and key != 'zip'):
                if value.isnumeric():
                    value = int(value)
                elif value == '.' or value == '-':
                    value = null
                elif _search(r'[a-zA-Z]| - ', value) is None and len(value) > 0 and value != ' ':
                    if _search(r'\.', value) is not None:
                        value = float(value)
                    elif isinstance(locale.atoi(value), int):
                        value = locale.atoi(value)
                elif value == ' ' or value == 'None':
                    value = null

            input_dict[key] = value
    except ValueError as value_error:
        print(input_dict, value_error)


def change_types(i_dirname: str) -> None:
    i_fnames = _listdir(i_dirname)
    total = len(i_fnames)

    tracker = 0
    limit = total
    with alive_bar(total) as bar:
        for fname in i_fnames:
            path = f"{i_dirname}/{fname}"
            file = open(path)
            school = _json.load(file)

            dict_walk(school['general'])

            if school['general'].get('rankings') is not None:
                del school['general']['rankings']
                school['rankings'] = dict()

            # output the type-converted data as a new file
            new_path = f"../../outputs/layer_5/{fname}"
            with open(new_path, 'w+') as outfile:
                outfile.write(_json.dumps(school))

            bar()
            tracker += 1
            if tracker == limit:
                break


def add_null_vals(i_dirname: str) -> None:
    i_fnames = _listdir(i_dirname)
    total = len(i_fnames)

    tracker = 0
    limit = total
    with alive_bar(total) as bar:
        for fname in i_fnames:
            path = f"{i_dirname}/{fname}"
            file = open(path)
            school = _json.load(file)

            if school['general'].get('tuition') is None:
                school['general']['tuition'] = {
                    "in_state": {
                        "2017": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        },
                        "2018": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        },
                        "2019": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        }
                    },
                    "out_of_state": {
                        "2017": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        },
                        "2018": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        },
                        "2019": {
                            "tuition_and_fees": '-',
                            "tuition": '-',
                            "fees": '-'
                        }
                    },
                    "books_and_supplies": {
                        "2017": '-',
                        "2018": '-',
                        "2019": '-'
                    },
                    "on_campus": {
                        "2017": {
                            "other_expenses": '-',
                            "room_and_board_on_campus": '-'
                        },
                        "2018": {
                            "other_expenses": '-',
                            "room_and_board_on_campus": '-'
                        },
                        "2019": {
                            "other_expenses": '-',
                            "room_and_board_on_campus": '-'
                        }
                    },
                    "off_campus": {
                        "2017": {
                            "room_and_board_off_campus": '-',
                            "other_expenses_off_campus": '-'
                        },
                        "2018": {
                            "room_and_board_off_campus": '-',
                            "other_expenses_off_campus": '-'
                        },
                        "2019": {
                            "room_and_board_off_campus": '-',
                            "other_expenses_off_campus": '-'
                        }
                    }
                }

            # output the type-converted data as a new file
            new_path = f"../../outputs/layer_5/{fname}"
            with open(new_path, 'w+') as outfile:
                outfile.write(_json.dumps(school))

            bar()
            tracker += 1
            if tracker == limit:
                break


def main():
    input_dirname = '../../outputs/layer_4'
    new_input_dirname = '../../outputs/layer_5'
    change_types(input_dirname)
    add_null_vals(new_input_dirname)


if __name__ == '__main__':
    main()
