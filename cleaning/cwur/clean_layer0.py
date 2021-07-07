import json
import os
import os.path

fname_2012 = './layer_0/cwur.2012.txt'


def create_dicts(fname):
    dict_template = {}
    dicts = []
    fname_components = fname.replace('/', '.').split('.')
    new_fname = f"./layer_1/{fname_components[3]}.{fname_components[4]}.json"
    with open(fname) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            string = line.strip()
            values = string.split('\t')
            if not i:
                for value in values:
                    dict_template[value] = None
            elif len(string):
                new_dict = dict_template.copy()
                for j, value in enumerate(values):
                    new_dict[list(new_dict)[j]] = value
                dicts.append(new_dict)
    if not os.path.isfile(new_fname):
        with open(new_fname, 'w+') as outf:
            outf.write(json.dumps(dicts))
        print(f"file {new_fname} successfully created!")
    else:
        print(f"file {new_fname} already exists")


def read_dir(dname):
    print(dname)
    for fname in os.listdir(dname):
        relative_path = f"{dname}/{fname}"
        create_dicts(relative_path)


def main():
    read_dir('./layer_0')


main()
