import json


def get_schoolnames(fname: str, out_fname: str) -> None:
    f = open(fname)
    data = json.load(f)

    aggregate = []
    for item in data:
        aggregate.append(item)

    with open(out_fname, 'w+') as outfile:
        outfile.write(json.dumps(aggregate))
    print(f"{out_fname} successfully created!")


def main():
    input_fname = '../../outputs/layer_2/merged.json'
    output_fname = '../../outputs/layer_2/schoolnames.json'
    get_schoolnames(input_fname, output_fname)


if __name__ == '__main__':
    main()
