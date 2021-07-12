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
                    if key != 'Institution' and key != 'Country' and key != 'Score':
                        if key in dicts[ff_schoolname]['rankings'] and key:
                            # if category already exists in school dict, only add year
                            new_entry = {
                                'year': year,
                                'ranking': school[key]
                            }
                            dicts[ff_schoolname]['rankings'][key][year] = new_entry

                        else:
                            # if category does not already exist, create a new entry w/ year
                            new_entry = {
                                year: {
                                    'year': year,
                                    'ranking': school[key]
                                }
                            }
                            dicts[ff_schoolname]['rankings'][key] = new_entry
            else:
                # create new dict item
                new_dict = {
                    'name': schoolname,
                    'country': school['Country'],
                    'rankings': {}
                }
                for key in list(school):
                    if key != 'Institution' and key != 'Country' and key != 'Score':
                        new_dict['rankings'][key] = {
                            year: {'year': year,
                                   'ranking': school[key]}
                        }
                dicts[ff_schoolname] = new_dict

    with open('layer_2_output.json', 'w+') as outfile:
        outfile.write(json.dumps(dicts))


def main():
    merge_dicts(target_dirname)


main()
