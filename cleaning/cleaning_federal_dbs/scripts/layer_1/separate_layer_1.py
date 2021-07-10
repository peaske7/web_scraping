import json
import os

from alive_progress import alive_bar

target_dirname = '../../script_outputs/layer_1'
target_fname = '../../script_outputs/layer_1_output.json'


def separate(fname: str) -> None:
    f = open(fname)
    data = json.load(f)
    total = len(data.keys())
    with alive_bar(total) as bar:
        for key in data.keys():
            new_fname = f"../../script_outputs/layer_1/{key}.json"
            item_data = data[key]

            if not os.path.exists(new_fname):
                with open(new_fname, 'w+') as outfile:
                    outfile.write(json.dumps(item_data))
                bar()
            else:
                print(f"PASS: {new_fname} already exists")
                bar()


def delete_all(dirname: str) -> None:
    for f in os.listdir(dirname):
        os.remove(os.path.join(dirname, f))


def main():
    delete_all(target_dirname)
    separate(target_fname)


if __name__ == '__main__':
    main()
