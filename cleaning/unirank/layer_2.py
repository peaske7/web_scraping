import json


def clean(fname: str, out_fname: str) -> None:
    f = open(fname)
    data = json.load(f)

    res = {}
    for item in data:
        name = item['name']
        year = item['year']
        ranking = item['ranking']

        ff_name = name.lower().replace(' ', '_').replace('&', 'and')

        if ranking != 'Un':
            res[ff_name] = {
                'name': name,
                'ff_name': ff_name,
                'year': year,
                'ranking': ranking
            }

    with open(out_fname, 'w+') as outfile:
        outfile.write(json.dumps(res))
    print(f"{out_fname} successfully created!")


def main():
    input_fname = './layer_1_output.json'
    output_fname = './layer_2_output.json'
    clean(input_fname, output_fname)


if __name__ == '__main__':
    main()
