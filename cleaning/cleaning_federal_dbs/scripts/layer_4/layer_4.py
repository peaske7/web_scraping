import json


def translate(i_fname, o_fname, o_dirname) -> None:
    f = open(i_fname)
    schools = json.load(f)

    for unitid in schools:
        school = schools[unitid]



def main():
    input_fname = ''
    output_fname = ''
    output_dirname = ''
    translate(input_fname, output_fname, output_dirname)


if __name__ == '__main__':
    main()