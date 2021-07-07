import json
import os

target_dirname = "./layer_1"


def merge_dicts(dirname):
    dicts = {}
    for filename in os.listdir(dirname):
        relative_path = f"{dirname}/{filename}"
        ranking_source = filename.split('.')[0]
        year = filename.split('.')[1]

        # read contents of each file
        f = open(relative_path)
        data = json.load(f)

        for school in data:
            schoolname = school['Institution']
            ff_schoolname = schoolname.lower().replace(' ', '_').replace('/', '-')
            if ff_schoolname in dicts.keys():
                # access dict item and append gathered data
                for key in list(school):
                    if key != 'Institution' and key != 'Country':
                        if key in dicts[ff_schoolname] and key:
                            dicts[ff_schoolname].get(key, []).append({year: school[key]})
                        else:
                            dicts[ff_schoolname][key] = [{year: school[key]}]
                print('already exists ', ff_schoolname)
            else:
                # create new dict item
                new_dict = dict()
                new_dict['name'] = schoolname
                new_dict['country'] = school['Country']
                for key in list(school):
                    if key != 'Institution' and key != 'Country':
                        new_dict[key] = [{year: school[key]}]
                print('not yet ', ff_schoolname)
                dicts[ff_schoolname] = new_dict

    with open('layer_2_output.json', 'w+') as outfile:
        outfile.write(json.dumps(dicts))


def main():
    merge_dicts(target_dirname)


main()
