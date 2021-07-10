import json
import re


def create_lookup(fname: str, output_fname: str) -> None:
    f = open(fname, 'r')
    content = f.readlines()

    lookup = dict()
    for line in content:
        clean_line = line.strip()
        split_line = re.split('\\t\\t', clean_line)

        lookup[split_line[0]] = split_line[1]

    with open(output_fname, 'w+') as outfile:
        outfile.write(json.dumps(lookup))


def main():
    target_fname = './majors_percentage_lookup.txt'
    output_fname = '../../script_outputs/layer_3/popular_cip_lookup.json'
    create_lookup(target_fname, output_fname)


if __name__ == '__main__':
    main()
