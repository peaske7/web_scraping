import json
from collections.abc import Mapping

from fuzzywuzzy import process as _process


def aggregate(i_fname: str, o_fname: str) -> None:
    f = open(i_fname)
    i_data = json.load(f)

    dicts = dict()
    ff_name_list = i_data.keys()
    limit = len(ff_name_list)
    # limit = 50
    for i in range(limit):
        ff_name = list(ff_name_list)[i]
        ratios_raw = _process.extract(ff_name, ff_name_list)
        ratios = [ratio for ratio in ratios_raw if ratio[1] > 96]
        if len(ratios) > 1:
            dicts[ff_name] = {"similar": ratios}
            print(f"{i + 1}/{limit}: {ff_name}")

    with open(o_fname, "w+") as outfile:
        outfile.write(json.dumps(dicts))


def _join(default: dict, update: dict) -> dict:
    for k, v in update.items():
        if isinstance(v, Mapping):
            default[k] = _join(default.get(k, {}), v)
        elif isinstance(default, Mapping):
            default[k] = v
        else:
            default = {k: update[k]}
    return default


def merge(i_fname: str, o_fname: str, s_fname: str) -> None:
    i = open(i_fname)
    schools = json.load(i)

    s = open(s_fname)
    similar = json.load(s)

    res_dict = {}
    visited = []
    for entry in similar:
        if entry in visited:
            continue
        else:
            raw_ff_name = entry
            new_ff_name = (
                raw_ff_name.replace("\u2013", "-")
                    .replace("_-_", "-")
                    .replace(",", "")
                    .replace(".", "")
            )
            similar_schools = similar[entry]["similar"]
            res_entry = dict()
            forbes_desc = ''
            forbes_uri = ''
            for school in similar_schools:
                print(school)
                school_dict = schools[school[0]]
                cur_forbes_desc = school_dict['general']['forbes_description']
                cur_forbes_uri = school_dict['general']['forbes_uri']
                res_entry = _join(res_entry, school_dict)
                if len(cur_forbes_desc) > len(forbes_desc):
                    forbes_desc = cur_forbes_desc
                if len(cur_forbes_uri) > len(forbes_uri):
                    forbes_uri = cur_forbes_uri
                print(forbes_desc)
                visited.append(school[0])

            res_entry['general']['forbes_description'] = forbes_desc
            res_entry['general']['forbes_uri'] = forbes_uri

            res_dict.update({new_ff_name: res_entry})

    with open(o_fname, 'w+') as outfile:
        outfile.write(json.dumps(res_dict))


def main():
    input_fname = "../../outputs/layer_1/layer_1_output.json"
    output_fname = "../../outputs/layer_2/layer_2_similar_us.json"
    merge_input_fname = "../../outputs/layer_1/layer_1_output.json"
    merge_output_fname = "../../outputs/layer_2/merged.json"
    merge_similars_fname = "../../outputs/layer_2/layer_2_similar_us.json"
    aggregate(input_fname, output_fname)
    merge(merge_input_fname, merge_output_fname, merge_similars_fname)


if __name__ == "__main__":
    main()
