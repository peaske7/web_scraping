import json
import os

target_dirname = './layer_1'
target_filename = './forbes_university_ranking.2019.json'


def clean_rankings(fname: str) -> dict:
    f = open(fname)
    data = json.load(f)
    schools = data['organizationList']['organizationsLists']

    dicts = dict()

    for school in schools:
        # ff_schoolname === file formatted schoolname
        ff_schoolname = school['uri'].replace('-', '_')
        dicts[ff_schoolname] = dict()

        # populate
        # general information
        dicts[ff_schoolname]['name'] = school.get('organizationName')
        dicts[ff_schoolname]['forbes_rank'] = school.get('rank')

        dicts[ff_schoolname]['short_description'] = school.get('short_description') or ''
        dicts[ff_schoolname]['description'] = school.get('description') or ''

        # ranks
        dicts[ff_schoolname]['rankings_by_category'] = []

    return dicts


def merge(dicts: dict, dirname: str):
    merged_dicts = dicts.copy()

    for filename in os.listdir(dirname):
        relative_path = f"{dirname}/{filename}"
        f = open(relative_path)
        data = json.load(f)

        schoolname = data['school_name']
        ff_schoolname = schoolname.replace(' ', '_')
        merged_dicts[ff_schoolname]['rankings_by_category'] = data['rankings']
        merged_dicts[ff_schoolname]['forbes_uri'] = data['school_forbes_abs_uri']

    with open('layer_3_output.json', 'w+') as outfile:
        outfile.write(json.dumps(merged_dicts))


def main():
    merge(clean_rankings(target_filename), './layer_1')


main()
