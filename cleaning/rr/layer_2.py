import json
import re


def aggregate(fname: str) -> dict:
    f = open(fname)
    data = json.load(f)

    res = {}
    for item in data:
        name_raw = item['name']
        split_name = re.split('\(|\)', name_raw)
        alias = ''
        if len(split_name) > 1:
            alias = split_name[1]

        name = split_name[0]
        ff_name = split_name[0].strip().lower().replace(' ', '_')
        year = item['year']
        ranking = item['ranking']
        score = item['score']
        is_in = res.get(ff_name)
        if is_in is None:
            # if item does not exist in res dict, add a new entry to res
            res[ff_name] = {
                'name': name,
                'ff_name': ff_name,
                'alias': alias,
                'rankings': {
                    str(year): {
                        'year': year,
                        'ranking': ranking,
                        'score': score,
                    }
                }
            }
        else:
            # if entry already exists inside the res dict
            res[ff_name]['rankings'][year] = {
                'year': year,
                'ranking': ranking,
                'score': score
            }
    return res


def write_file(data: dict, fname: str) -> None:
    with open(fname, 'w+') as outfile:
        outfile.write(json.dumps(data))


def main():
    target_fname = './layer_1_output.json'
    aggregate_output = aggregate(target_fname)
    output_fname = './layer_2_output.json'
    write_file(aggregate_output, output_fname)


if __name__ == '__main__':
    main()
