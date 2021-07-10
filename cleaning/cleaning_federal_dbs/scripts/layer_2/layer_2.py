# merge with majors and e_outputs/institutionData

import json

from alive_progress import alive_bar


def merge():
    e_fname = '../../resources/institution_data_output.json'
    t_fname = '../../script_outputs/layer_1_output.json'

    e_f = open(e_fname)
    e_data = json.load(e_f)

    t_f = open(t_fname)
    t_data = json.load(t_f)

    total = len(t_data)
    invalid_items = []
    with alive_bar(total) as bar:
        for unitid in t_data:
            t_item = t_data[unitid]
            e_item = e_data.get(unitid)

            if e_item:
                t_data[unitid]['general']['opeid'] = e_item['opeid']
                t_data[unitid]['general']['opeid6'] = e_item['opeid6']
                t_data[unitid]['general']['local_url'] = e_item['local_url']
                t_data[unitid]['general']['campus']['address_short'] = e_item['address_short']
                t_data[unitid]['general']['students']['enrollment'] = e_item['students']
                bar()
            else:
                print('unitid does not exist: ', unitid)
                invalid_items.append(unitid)
                bar()

    # remove invalid children from final dict (the one to create files from)
    for invalid_item in invalid_items:
        removed = t_data.pop(invalid_item, None)
        if removed is not None:
            print(f"removed key {invalid_item} from t_data")
        else:
            print('No key removed')

    new_layer_2_output_path = '../../script_outputs/layer_2_output.json'
    with open(new_layer_2_output_path, 'w+') as outfile:
        outfile.write(json.dumps(t_data))

    new_total = len(t_data)
    with alive_bar(new_total) as bar:
        for item in t_data:
            item_data = t_data.get(item)
            new_fname = f"../../script_outputs/layer_2/{item}.json"

            with open(new_fname, 'w+') as outfile:
                outfile.write(json.dumps(item_data))
            bar()


def main():
    merge()


if __name__ == '__main__':
    main()
