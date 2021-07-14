import json
import os

from alive_progress import alive_bar


def transfer(unitid_dirname: str) -> None:
    dirnames = os.listdir(unitid_dirname)
    total_length = len(dirnames)
    with alive_bar(total_length) as bar:
        for file in dirnames:
            file_path = f"{unitid_dirname}/{file}"
            if not os.path.exists(file_path):
                f = open(file_path)
                data = json.load(f)

                data['general']['rankings'] = {}
                new_file_path = f"../../outputs/layer_4/{file}"

                with open(new_file_path, 'w+') as outfile:
                    outfile.write(json.dumps(data))
            else:
                print('already exists')
            bar()
    print('transfer complete!')


def finalize(name_dirname: str) -> None:
    dirnames = os.listdir(name_dirname)
    total_length = len(dirnames)
    with alive_bar(total_length) as bar:
        for file in dirnames:
            try:
                file_path = f"{name_dirname}/{file}"
                f = open(file_path)
                data = json.load(f)

                unitid = list(data)[0]
                new_data = data[unitid]
                new_file_path = f"../../outputs/layer_4/{unitid}.json"
                print(new_file_path)
                with open(new_file_path, 'w+') as outfile:
                    outfile.write(json.dumps(new_data))

            except json.decoder.JSONDecodeError as e:
                print(file, '\n', e)
            except UnicodeDecodeError as e:
                print(file, '\n', e)
            bar()
    print('finalization complete!')


def main():
    unitid_dirname = '../../cleaning_federal_dbs/script_outputs/layer_3'
    transfer(unitid_dirname)

    name_dirname = '../../outputs/layer_3/schools'
    finalize(name_dirname)


if __name__ == '__main__':
    main()
