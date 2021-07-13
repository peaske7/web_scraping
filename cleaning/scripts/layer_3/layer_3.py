import json
import os

from alive_progress import alive_bar
from fuzzywuzzy import process as _process


def writefile_default(o_fname: str, data: dict) -> None:
    with open(o_fname, 'w+') as outfile:
        outfile.write(json.dumps(data))


def aggregate(keys_fname: str, edges_fname: str, lookup_fname: str) -> None:
    # keys_data is the bulk data that have rankings info for most major colleges, except edge cases where
    # multiple instances of colleges were found in the database
    keys_f = open(keys_fname)
    keys_data = json.load(keys_f)

    # edges_data are the colleges where the name of the college caused there to be multiple entries in
    # keys_data. In edges_data, we only one aggregated entry for each college, so once all keys_data is
    # merged with the existing colleges, overwrite them with these
    edges_f = open(edges_fname)
    edges_data = json.load(edges_f)

    # lookup_data is where keys_data and edges_data will be merged to. This data will come as a result of
    # the aggregate data from ./cleaning_federal_dbs
    lookup_f = open(lookup_fname)
    lookup_data = json.load(lookup_f)

    # 1. merge all data in keys_data with those in lookup_data
    # 2. overwrite those where edges_data apply
    def get_unitid(lookup_key: str) -> str:
        for item in lookup_data:
            if lookup_data[item]['general']['ff_name'] == lookup_key:
                return item

    def add2lookup(keys_key, lookup_key):
        # add forbes description & uri
        unitid = get_unitid(lookup_key)

        forbes_desc = keys_data[keys_key]['general']['forbes_description']
        forbes_uri = keys_data[keys_key]['general']['forbes_uri']
        lookup_data[unitid]['general']['forbes_desc'] = forbes_desc
        lookup_data[unitid]['general']['forbes_uri'] = forbes_uri

        # add rankings
        rankings = keys_data[keys_key]['rankings_by_category']
        lookup_data[unitid]['rankings'] = rankings

    def merge_and_get(keys_key, lookup_key) -> dict:
        unitid = get_unitid(lookup_key)
        merged_dict = {unitid: lookup_data[unitid]}

        forbes_desc = keys_data[keys_key]['general']['forbes_description']
        forbes_uri = keys_data[keys_key]['general']['forbes_uri']
        merged_dict[unitid]['general']['forbes_desc'] = forbes_desc
        merged_dict[unitid]['general']['forbes_uri'] = forbes_uri

        rankings = keys_data[keys_key]['rankings_by_category']
        merged_dict[unitid]['rankings'] = rankings

        return merged_dict

    def get_lookup_list(data: dict, reverse: dict) -> list:
        items_list = []
        for item in data.keys():
            name = data[item]['general']['ff_name']
            items_list.append(name)
            items_reverse_lookup[name] = name
            aliases = data[item]['general']['aliases']
            if len(aliases) > 0:
                for alias in aliases:
                    alias_ff_name = alias.lower().replace(' ', '_')
                    items_list.append(alias_ff_name)
                    items_reverse_lookup[alias_ff_name] = name

        items_list_clean = []
        for item in items_list:
            if item != '':
                items_list_clean.append(item)

        lookup_fname = '../../outputs/layer_3/lookup.json'
        writefile_default(lookup_fname, items_list_clean)

        reverse_lookup_fname = '../../outputs/layer_3/reverse_lookup.json'
        writefile_default(reverse_lookup_fname, items_reverse_lookup)

        return items_list_clean

    def writefile(data: dict, o_fname: str, refresh=False, o_dirname='../../outputs/layer_3/schools') -> None:
        output_path = f"{o_dirname}/{o_fname}.json"
        if refresh:
            if os.path.isfile(output_path):
                os.remove(output_path)
                with open(output_path, 'w+') as outfile:
                    outfile.write(json.dumps(data))
                # print(f"{o_fname} success")
        else:
            # if os.path.isfile(output_path):
            #     print(f"{o_fname} already exists")
            # else:
            try:
                with open(output_path, 'w+') as outfile:
                    outfile.write(json.dumps(data))
                    # print(f"{o_fname} success")
            except FileNotFoundError as e:
                print(e)

    items_reverse_lookup = {}
    lookup_items_list = get_lookup_list(lookup_data, items_reverse_lookup)

    not_added_yet = []
    total_length = len(keys_data.keys())
    tracker = 0
    limit = total_length
    with alive_bar(total_length) as bar:
        for item_index, key_item in enumerate(keys_data):
            output_path = f"../../outputs/layer_3/schools/{key_item}.json"
            if os.path.isfile(output_path):
                print(f"{output_path} already exists")
            else:
                ratios_raw = _process.extract(key_item, lookup_items_list)
                head_ff_name = ratios_raw[0][0]
                head_val = ratios_raw[0][1]

                # if the found value is similar enough, just merge and create file
                if head_val > 98:
                    true_head_ff_name = items_reverse_lookup[head_ff_name]
                    writefile(merge_and_get(key_item, true_head_ff_name),
                              true_head_ff_name)
                    # print(head_ff_name, true_head_ff_name)
                    lookup_items_list.remove(head_ff_name)
                    if head_ff_name != true_head_ff_name:
                        try:
                            lookup_items_list.remove(true_head_ff_name)
                        except ValueError as e:
                            print(e)
                    print(f"{item_index}/{total_length} :: +{key_item}")
                # if not, deal with it later
                else:
                    not_added_yet.append(
                        {'keys_ff_name': key_item, 'similar_items': ratios_raw})
                    print(f"{item_index}/{total_length} :: ={key_item}")
            bar()
            tracker += 1
            if tracker == limit:
                break

    not_added_yet_ff_names_fname = '../../outputs/layer_3/notyets.json'
    writefile_default(not_added_yet_ff_names_fname, not_added_yet)

    total_length = len(edges_data.keys())
    print(total_length)
    with alive_bar(total_length) as bar:
        for item_index, edge_item in enumerate(edges_data):
            ratios_raw = _process.extract(edge_item, lookup_items_list)
            head_ff_name = ratios_raw[0][0]
            head_val = ratios_raw[0][1]
            if head_val > 98:
                true_head_ff_name = items_reverse_lookup[head_ff_name]
                add2lookup(edge_item, true_head_ff_name)
                print(f"{item_index}/{total_length} :: +{edge_item}")
            else:
                not_added_yet.append(
                    {'keys_ff_name': edge_item, 'similar_items': ratios_raw})
                print(f"{item_index}/{total_length} :: ={edge_item}")
            bar()

    # output files
    # lookup_new_fname = '../../outputs/layer_3/initial_output.json'
    # writefile(lookup_new_fname, lookup_data)


def main():
    keys_fname = '../../outputs/layer_3/pruned.output.json'
    edges_fname = '../../outputs/layer_2/merged.json'
    lookup_fname = '../../cleaning_federal_dbs/script_outputs/layer_3_output.json'
    aggregate(keys_fname, edges_fname, lookup_fname)
    # test_fuzzy(keys_fname, lookup_fname)


if __name__ == '__main__':
    main()
