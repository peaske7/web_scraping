import json
import os
import re


target_dirname = './layer_3'


def extract(dirname):
    # initialize dict
    dicts = dict()

    for filename in os.listdir(dirname):
        relative_path = f"{dirname}/{filename}"
        f = open(relative_path)
        data = json.load(f)

        # populate dict
        for ranking_item in data:
            clean_schoolname = re.sub(r"\(.+\)", '', ranking_item['name']) \
                .replace(',', '').strip()
            ff_schoolname = clean_schoolname \
                .lower().replace(' ', '_').replace('-', '_').replace('___', '_')

            category = ranking_item.get('category')
            year = ranking_item.get('year')
            rank = ranking_item.get('rank')
            country = ranking_item.get('country')
            name = clean_schoolname
            score = ranking_item.get('score')

            if ff_schoolname in dicts.keys():
                # add to existing dict
                # dicts[ff_schoolname]['rankings_by_category']
                if dicts[ff_schoolname]['rankings_by_category'].get(category):
                    dicts[ff_schoolname]['rankings_by_category'][category][year] = {
                        'rank': rank,
                        'score': score
                    }
                else:
                    dicts[ff_schoolname]['rankings_by_category'][category] = dict()
                    dicts[ff_schoolname]['rankings_by_category'][category][year] = {
                        'rank': rank,
                        'score': score
                    }
            else:
                # add new dict
                dicts[ff_schoolname] = dict()
                dicts[ff_schoolname]['name'] = name
                dicts[ff_schoolname]['country'] = country
                dicts[ff_schoolname]['rankings_by_category'] = \
                    {category: {'year': {'rank': rank, 'score': score}}}

    with open('layer_4_output.json', 'w+') as outfile:
        outfile.write(json.dumps(dicts))


def main():
    extract(target_dirname)


main()
