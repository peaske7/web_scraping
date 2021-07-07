import json
import os

target_dirname = './layer_1'


def clean(dirname):
    for filename in os.listdir(dirname):
        relative_path = f"{dirname}/{filename}"
        f = open(relative_path)
        data = json.load(f)

        new_fname = f"./layer_2/{filename}"
        new_data = []

        for school in data['data']:
            new_school = {
                'name': school['name'],
                'country': school['location'],
            }

            # rankings and scores of different categories
            ranking_categories = []
            category = {}
            tracker = 0
            for key in school.keys():
                string = key.split('_')
                if string[0] == 'scores' and string[-1] == 'rank':
                    category_rank = school[key]
                    category['category_rank'] = category_rank
                    tracker += 1
                    if not tracker % 2:
                        ranking_categories.append(category)
                        category = {}
                elif string[0] == 'scores' and string[-1] != 'rank':
                    category_name = "_".join(string[1:])
                    category_score = school[key]
                    category['category_name'] = category_name
                    category['category_score'] = category_score
                    tracker += 1

            new_school['ranking_categories'] = ranking_categories
            new_data.append(new_school)

        with open(new_fname, 'w+') as outfile:
            outfile.write(json.dumps(new_data))


def main():
    clean(target_dirname)


main()
